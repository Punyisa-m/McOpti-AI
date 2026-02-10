import os
import pandas as pd
from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# --- 1. Load Data ---
def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sales = pd.read_csv(os.path.join(base_path, "data", "menu_sales.csv"))
    inventory = pd.read_csv(os.path.join(base_path, "data", "inventory.csv"))
    return sales, inventory

sales_df, inv_df = load_data()

# --- 2. AI Tools ---
@tool
def get_sales_report():
    """Analyze sales figures and rank menu items."""
    df = sales_df.sort_values(by='sales_volume', ascending=False)
    top_3 = df.head(3)
    bottom_3 = df.tail(3)
    
    report = "📈 **Sales Performance Analysis**\n"
    report += "### Top Sellers\n"
    for _, r in top_3.iterrows():
        report += f"- {r['menu_item']} ({r['sales_volume']} units)\n"
    
    report += "\n### Low Performers\n"
    for _, r in bottom_3.iterrows():
        report += f"- {r['menu_item']} ({r['sales_volume']} units)\n"
    return report

@tool
def check_inventory_and_restock():
    """Analyze stock and calculate order priority"""
    low_stock = inv_df[inv_df['stock_level'] < inv_df['min_threshold']].copy()
    if low_stock.empty:
        return "Everything is fine. We have sufficient stock."

    low_stock['shortage_pct'] = (low_stock['stock_level'] / low_stock['min_threshold']) * 100
    low_stock = low_stock.sort_values(by='shortage_pct')

    plan = "🚨 **Critical Restock Plan (Prioritized)**\n"
    plan += "| staple | status | recomment | Level of importance |\n"
    plan += "| :--- | :--- | :--- | :--- |\n"
    
    for _, row in low_stock.iterrows():
        order_qty = (row['min_threshold'] * 2) - row['stock_level']
        priority = "🔴 risky" if row['shortage_pct'] < 30 else "🟡 medium"
        plan += f"| {row['ingredient']} | {row['stock_level']}/{row['min_threshold']} {row['unit']} | **+{order_qty}** | {priority} |\n"
    return plan

tools = [get_sales_report, check_inventory_and_restock]
tool_node = ToolNode(tools)

# --- 3. Model Logic ---
API_KEY = "Your_API"
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=API_KEY).bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], "History"]

def call_model(state: AgentState):
    messages = state['messages']
    if isinstance(messages[-1], ToolMessage):
        system_msg = "Analyze the tool output and provide a professional, executive summary in Thai. Use markdown tables where appropriate."
    else:
        system_msg = "You are 'McOpti', a smart supply chain expert. Help the manager analyze sales and restock. Answer in Thai."
    
    response = llm.invoke([SystemMessage(content=system_msg)] + messages)
    return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", lambda x: "tools" if x["messages"][-1].tool_calls else END)
workflow.add_edge("tools", "agent")
app = workflow.compile()
