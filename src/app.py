import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agents import app, sales_df, inv_df
from langchain_core.messages import HumanMessage

# 1. Page Configuration
st.set_page_config(page_title="McOpti Pro Dashboard", layout="wide", page_icon="🍔")

# 2. Professional Dashboard CSS
st.markdown("""
<style>
    /* ===== FONTS & GLOBAL ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main, .stMarkdown, p, span, label {
        color: #1a1a1a !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ===== BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
    
    .main {
        background-color: transparent !important;
    }

    /* ===== METRIC CARDS - Premium Glass Effect ===== */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 16px !important;
        padding: 24px 20px !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        border-color: #4CAF50 !important;
    }

    /* Metric Values - Bold & Clear */
    [data-testid="stMetricValue"] {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #1a1a1a !important;
        line-height: 1.2 !important;
        background: linear-gradient(135deg, #1a1a1a 0%, #4CAF50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Metric Labels */
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #666666 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        margin-bottom: 8px !important;
    }
    
    /* Metric Delta */
    [data-testid="stMetricDelta"] {
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* ===== HEADERS ===== */
    h1 {
        color: #1a1a1a !important;
        font-weight: 900 !important;
        font-size: 42px !important;
        letter-spacing: -1px !important;
        margin-bottom: 8px !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    
    h2, h3 {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }

    /* ===== TABS - Modern Style ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 6px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px !important;
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 0 24px !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f5f5f5 !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"] p {
        color: #666666 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] p {
        color: #ffffff !important;
    }

    /* ===== CHAT INTERFACE - Modern Messaging ===== */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #e8e8e8 !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        border: none !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: #f8f9fa !important;
        border-left: 4px solid #4CAF50 !important;
    }
    
    /* Chat Input */
    .stChatInputContainer {
        border-top: 2px solid #e0e0e0 !important;
        padding-top: 16px !important;
    }
    
    .stChatInputContainer textarea {
        color: #1a1a1a !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease !important;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1) !important;
    }

    /* ===== CONTAINER STYLING ===== */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* ===== BUTTON STYLING ===== */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(76, 175, 80, 0.4) !important;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1 !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #45a049 0%, #4CAF50 100%) !important;
    }

    /* ===== SPINNER ===== */
    .stSpinner > div {
        border-top-color: #4CAF50 !important;
    }

    /* ===== STATUS BAR ===== */
    .main > div:first-child {
        background: linear-gradient(90deg, rgba(76, 175, 80, 0.1) 0%, rgba(69, 160, 73, 0.05) 100%) !important;
        border-bottom: 2px solid #4CAF50 !important;
        padding: 12px 20px !important;
        margin-bottom: 20px !important;
        border-radius: 12px !important;
    }

    /* ===== CHAT INTERFACE - PREMIUM DESIGN ===== */
    
    /* Chat Container Background */
    [data-testid="stVerticalBlock"] > div:has([data-testid="stChatMessage"]) {
        background: linear-gradient(to bottom, #ffffff 0%, #f8f9fa 100%) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 
            inset 0 2px 8px rgba(0, 0, 0, 0.05),
            0 4px 20px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* User Message - Gradient Green Bubble */
    [data-testid="stChatMessage"]:has([data-testid="stMarkdownContainer"]):nth-of-type(odd) {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%) !important;
        border: none !important;
        border-radius: 18px 18px 4px 18px !important;
        padding: 16px 20px !important;
        margin: 8px 0 8px 40px !important;
        box-shadow: 
            0 4px 12px rgba(76, 175, 80, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        animation: slideInRight 0.3s ease-out !important;
    }
    
    [data-testid="stChatMessage"]:has([data-testid="stMarkdownContainer"]):nth-of-type(odd) * {
        color: #ffffff !important;
    }
    
    /* Assistant Message - Clean White Bubble */
    [data-testid="stChatMessage"]:has([data-testid="stMarkdownContainer"]):nth-of-type(even) {
        background: #ffffff !important;
        border: 2px solid #e8e8e8 !important;
        border-radius: 18px 18px 18px 4px !important;
        padding: 16px 20px !important;
        margin: 8px 40px 8px 0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        animation: slideInLeft 0.3s ease-out !important;
    }
    
    [data-testid="stChatMessage"]:has([data-testid="stMarkdownContainer"]):nth-of-type(even) * {
        color: #1a1a1a !important;
    }
    
    /* Avatar Styling */
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon"] {
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%) !important;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 20px !important;
    }
    
    /* Chat Input Area - Modern Style */
    .stChatInputContainer {
        background: #ffffff !important;
        border-top: 2px solid #e8e8e8 !important;
        padding: 16px 20px !important;
        margin-top: 12px !important;
        border-radius: 16px !important;
        box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stChatInputContainer textarea {
        color: #1a1a1a !important;
        background: #f8f9fa !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 14px !important;
        font-size: 15px !important;
        padding: 14px 20px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        resize: none !important;
    }
    
    .stChatInputContainer textarea:focus {
        background: #ffffff !important;
        border-color: #4CAF50 !important;
        box-shadow: 
            0 0 0 4px rgba(76, 175, 80, 0.12),
            0 4px 12px rgba(76, 175, 80, 0.15) !important;
        outline: none !important;
    }
    
    .stChatInputContainer textarea::placeholder {
        color: #999999 !important;
        font-style: italic !important;
    }
    
    /* Send Button */
    .stChatInputContainer button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    .stChatInputContainer button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4) !important;
    }
    
    .stChatInputContainer button:active {
        transform: scale(0.98) !important;
    }
    
    /* Spinner in Chat */
    [data-testid="stChatMessage"] .stSpinner {
        border-top-color: #4CAF50 !important;
    }
    
    /* Animation Keyframes */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Markdown Content in Chat */
    [data-testid="stChatMessage"] .stMarkdown {
        font-size: 15px !important;
        line-height: 1.6 !important;
    }
    
    [data-testid="stChatMessage"] .stMarkdown p {
        margin-bottom: 8px !important;
    }
    
    [data-testid="stChatMessage"] .stMarkdown strong {
        font-weight: 700 !important;
    }
    
    [data-testid="stChatMessage"] .stMarkdown code {
        background: rgba(0, 0, 0, 0.1) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-size: 13px !important;
    }
    
    /* User message code blocks */
    [data-testid="stChatMessage"]:nth-of-type(odd) .stMarkdown code {
        background: rgba(255, 255, 255, 0.2) !important;
    }

</style>
""", unsafe_allow_html=True)

# --- UI Content ---

st.title("🍔 McOpti AI — Supply Chain Intelligence")
st.write(f"**Operator:** Punyisa | **Status:** Online | **Database:** {len(sales_df)} SKUs")

# --- Metrics Section ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("TOTAL REVENUE", f"฿{(sales_df['price'] * sales_df['sales_volume']).sum():,.0f}")
with m2:
    st.metric("TOTAL ORDERS", f"{sales_df['sales_volume'].sum():,.0f}")
with m3:
    critical = len(inv_df[inv_df['stock_level'] < inv_df['min_threshold']])
    st.metric("STOCK ALERTS", critical, delta=f"{critical} Items Low", delta_color="inverse")
with m4:
    best_item = sales_df.loc[sales_df['sales_volume'].idxmax(), 'menu_item']
    st.metric("STAR PRODUCT", best_item)

st.markdown("<br>", unsafe_allow_html=True)

# --- Analysis & Assistant ---
c1, c2 = st.columns([1.3, 0.7])

with c1:
    tab1, tab2 = st.tabs(["📊 SALES PERFORMANCE", "🛡️ INVENTORY HEALTH"])
    
    with tab1:
        # Plotly with HIGH CONTRAST Text
        fig1 = px.bar(sales_df, x='menu_item', y='sales_volume', color='category', 
                     template="plotly_white", 
                     title="<b>Volume by Menu Item</b>", 
                     text_auto=True,
                     color_discrete_sequence=['#4CAF50', '#45a049', '#66BB6A'])
        
        fig1.update_layout(
            # ===== TEXT SIZE & COLOR =====
            font=dict(
                color="#000000",
                size=14, 
                family="Inter, Arial Black"
            ),
            
            # ===== TITLE =====
            title=dict(
                font=dict(size=20, color="#000000", family="Inter"),
                x=0.5,
                xanchor='center'
            ),
            
            # ===== AXES =====
            xaxis=dict(
                title=dict(text="<b>Menu Items</b>", font=dict(size=15, color="#000000")),
                tickfont=dict(size=13, color="#000000", family="Arial Black"),
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text="<b>Sales Volume</b>", font=dict(size=15, color="#000000")),
                tickfont=dict(size=13, color="#000000", family="Arial Black"),
                gridcolor='#E0E0E0'
            ),
            
            # ===== LEGEND =====
            legend=dict(
                font=dict(size=13, color="#000000", family="Arial Black"),
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#000000",
                borderwidth=1
            ),
            
            # ===== BACKGROUND =====
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#F8F9FA',
            
            # ===== HOVER =====
            hoverlabel=dict(
                bgcolor="white", 
                font_size=14,
                font_family="Arial Black",
                font_color="#000000"
            )
        )
        
        # ===== BAR TEXT =====
        fig1.update_traces(
            textfont=dict(size=14, color="#000000", family="Arial Black"),
            textposition='outside',
            marker_line_width=1,
            marker_line_color='#000000'
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
    with tab2:
        fig2 = go.Figure()
        
        # Bar Chart
        fig2.add_trace(go.Bar(
            name='Current Stock', 
            x=inv_df['ingredient'], 
            y=inv_df['stock_level'], 
            marker=dict(
                color='#4CAF50',
                line=dict(color='#000000', width=1)
            ),
            text=inv_df['stock_level'],
            textposition='outside',
            textfont=dict(size=14, color="#000000", family="Arial Black")
        ))
        
        # Threshold Line
        fig2.add_trace(go.Scatter(
            name='Min Threshold', 
            x=inv_df['ingredient'], 
            y=inv_df['min_threshold'], 
            line=dict(color='#FF5252', width=4),
            mode='lines+markers+text',
            marker=dict(size=10, color='#FF5252', line=dict(color='#000000', width=1)),
            text=inv_df['min_threshold'],
            textposition='top center',
            textfont=dict(size=13, color="#000000", family="Arial Black")
        ))
        
        fig2.update_layout(
            # ===== TEXT SIZE & COLOR =====
            font=dict(
                color="#000000",
                size=14,
                family="Inter, Arial Black"
            ),
            
            # ===== TITLE =====
            title=dict(
                text="<b>Stock Levels vs Required Minimum</b>",
                font=dict(size=20, color="#000000", family="Inter"),
                x=0.5,
                xanchor='center'
            ),
            
            # ===== AXES =====
            xaxis=dict(
                title=dict(text="<b>Ingredients</b>", font=dict(size=15, color="#000000")),
                tickfont=dict(size=13, color="#000000", family="Arial Black"),
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text="<b>Quantity</b>", font=dict(size=15, color="#000000")),
                tickfont=dict(size=13, color="#000000", family="Arial Black"),
                gridcolor='#E0E0E0'
            ),
            
            # ===== LEGEND =====
            legend=dict(
                font=dict(size=13, color="#000000", family="Arial Black"),
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#000000",
                borderwidth=1,
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            
            # ===== BACKGROUND =====
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#F8F9FA',
            
            # ===== HOVER =====
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Arial Black",
                font_color="#000000"
            ),
            
            # ===== SPACING =====
            margin=dict(t=80, b=60, l=60, r=40)
        )
        
        st.plotly_chart(fig2, use_container_width=True)

with c2:
    st.subheader("🤖 McOpti Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ===== CHAT CONTAINER WITH CUSTOM STYLING =====
    chat_box = st.container(height=520)
    
    with chat_box:
        # Welcome Message
        if len(st.session_state.messages) == 0:
            st.markdown("""
            <div style="
                text-align: center; 
                padding: 60px 20px;
                color: #666;
            ">
                <div style="font-size: 48px; margin-bottom: 16px;">🤖</div>
                <div style="font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 8px;">
                    McOpti Assistant Ready
                </div>
                <div style="font-size: 14px; color: #999;">
                    Ask me about inventory, sales, or order suggestions
                </div>
                <div style="
                    margin-top: 24px;
                    padding: 12px 20px;
                    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                    border-left: 4px solid #4CAF50;
                    border-radius: 8px;
                    text-align: left;
                    font-size: 13px;
                    color: #1a1a1a;
                ">
                    <b>💡 Try asking:</b><br>
                    • "Which items are low in stock?"<br>
                    • "What should I order today?"<br>
                    • "Show me best selling products"
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Chat Messages
            for i, m in enumerate(st.session_state.messages):
                with st.chat_message(m["role"], avatar="👤" if m["role"] == "user" else "🤖"):
                    st.markdown(m["content"])

    # ===== CHAT INPUT WITH STYLING =====
    if prompt := st.chat_input("💬 Type your question here...", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_box:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

        with chat_box:
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🔄 Analyzing data..."):
                    final_res = ""
                    for output in app.stream({"messages": [HumanMessage(content=prompt)]}):
                        for key, val in output.items():
                            if key == "agent":
                                final_res = val["messages"][-1].content
                    
                    # typing effect
                    st.markdown(final_res)
                    st.session_state.messages.append({"role": "assistant", "content": final_res})
        
        st.rerun()