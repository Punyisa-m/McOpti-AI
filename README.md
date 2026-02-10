# 🍔 McOpti-AI — Intelligent Supply Chain Manager

**McOpti-AI** is a sophisticated AI Agent designed to revolutionize fast-food supply chain management. By integrating **LangGraph** for multi-step reasoning and **Streamlit** for real-time visualization, McOpti-AI transforms raw operational data into high-level business intelligence.

## 🚀 Key Features

* **Agentic Inventory Management**: Powered by **LangGraph**, the agent performs a "Business Health Check" by cross-referencing sales trends with current stock levels.
* **Dynamic Restock Logic**: Automatically calculates restock quantities based on custom safety thresholds, preventing stockouts for 30+ SKUs.
* **Interactive Visualizations**: High-contrast, executive-level dashboards using **Plotly** to visualize sales volume by category and inventory health.
* **Robust Workflow**: Implemented a self-correction loop-breaker logic to ensure stable AI responses and efficient tool calling.

---

## 🛠️ Technical Stack

* **Logic & Workflow**: LangChain & LangGraph (Stateful Multi-Agent Orchestration).
* **LLM Engine**: Groq (Llama-3.1-8b-instant) — Chosen for ultra-low latency and high reasoning capabilities.
* **Frontend**: Streamlit (Premium Glassmorphism & Custom CSS).
* **Data Processing**: Pandas & NumPy for real-time CSV analytics.
* **Graphics**: Plotly (Express & Graph Objects) for interactive business charts.

---

## 📂 Project Structure

```text
McOpti-AI/
├── data/
│   ├── inventory.csv     # Real-time stock levels, thresholds, and units
│   └── menu_sales.csv    # Historical sales data for 30+ menu items
├── src/
│   ├── agents.py         # AI Logic, Tool definitions, and LangGraph state machine
│   └── app.py            # Streamlit Dashboard UI and custom styling
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation

```

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
```bash
git clone https://github.com/YourUsername/McOpti-AI.git
cd McOpti-AI

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Configure API Key:**:
McOpti-AI uses the Groq Llama-3.1 model. To run the agent, open src/agents.py and replace the placeholder string with your own API key:
```bash
API_KEY = "your_API"

```


4. **Run the application**:
```bash
streamlit run src/app.py
---

Would you like me to help you create a **LinkedIn post** to announce this project once you've successfully pushed it to GitHub?
