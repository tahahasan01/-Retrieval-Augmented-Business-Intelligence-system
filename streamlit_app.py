import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="RAG Intelligence System", layout="wide", page_icon="🤖")

# --- Custom CSS for dark theme and improved readability ---
st.markdown(
    """
    <style>
    body, .main, .stApp {
        background-color: #18191A !important;
        color: #F5F6FA !important;
    }
    .stButton>button {
        background-color: #4F8BF9 !important;
        color: #F5F6FA !important;
        border-radius: 8px;
    }
    .st-bb {border-radius: 8px;}
    .st-expanderHeader {font-weight: bold; color: #F5F6FA !important;}
    .stTextInput>div>div>input {
        background-color: #242526 !important;
        color: #F5F6FA !important;
    }
    .stDataFrame, .stTable, .stMetric, .stCaption, .stMarkdown, .stJson {
        background-color: #242526 !important;
        color: #F5F6FA !important;
    }
    .stSidebar {
        background-color: #242526 !important;
        color: #F5F6FA !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

API_URL = "http://localhost:8000"

# --- Session State for Query History ---
if 'query_history' not in st.session_state:
    st.session_state['query_history'] = []

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/4F8BF9/artificial-intelligence.png", width=80)
    st.title("RAG Intelligence")
    page = st.radio("Navigation", ["Query", "Analytics", "Ingest Data"])
    st.markdown("---")
    st.caption("Built with Streamlit | v1.0")

# --- Query Page ---
if page == "Query":
    st.title("Ask Your Data 🤖")
    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input("Ask a business question:", help="Type your question about your data.")
        optimize = st.checkbox("Optimize Query", value=True, help="Enable query optimization for better results.")
        insights = st.checkbox("Generate Insights", value=True, help="Summarize and extract key points.")
        collection = st.selectbox("Select Collection", ["default", "structured", "unstructured"], help="Choose which data collection to query.")
        summary_length = st.selectbox("Summary Length", ["brief", "detailed"], index=0)
        submit = st.button("Submit", use_container_width=True)
    with col2:
        st.markdown("#### Query History")
        for q in st.session_state['query_history'][-5:][::-1]:
            st.write(f"{q['time']} - {q['query']}")

    if submit and query:
        with st.spinner("Querying..."):
            response = requests.post(
                f"{API_URL}/query",
                json={
                    "query": query,
                    "collection": collection,
                    "optimize_query": optimize,
                    "generate_insights": insights,
                    "summary_length": summary_length
                },
            )
            if response.ok:
                data = response.json()
                st.session_state['query_history'].append({
                    "query": query,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                st.success("Answer received!")
                with st.expander("Answer", expanded=True):
                    st.write(data.get("answer", "No answer returned."))
                    st.button("Copy Answer", on_click=st.write, args=("Copied!",), key=f"copy_{time.time()}")
                with st.expander("Context & Lineage", expanded=False):
                    st.json(data.get("lineage", {}))
            else:
                st.error("Error: " + response.text)

# --- Analytics Page ---
elif page == "Analytics":
    st.title("Analytics Dashboard 📊")
    with st.spinner("Fetching analytics..."):
        try:
            response = requests.get(f"{API_URL}/analytics")
            if response.ok:
                analytics = response.json()
                st.metric("Total Queries", analytics.get("total_queries", 0))
                st.subheader("Recent Queries")
                df = pd.DataFrame(analytics.get("recent_queries", []))
                if not df.empty:
                    st.dataframe(df)
                else:
                    st.info("No recent queries.")
                # Example: Add a bar chart for queries per day
                if 'queries_per_day' in analytics:
                    st.bar_chart(pd.DataFrame(analytics['queries_per_day']))
            else:
                st.error("Error: " + response.text)
        except Exception as e:
            st.error(f"Failed to fetch analytics: {e}")

def ingest_batch(endpoint, label):
    if st.button(label):
        try:
            resp = requests.post(f"http://localhost:8000/{endpoint}")
            if resp.status_code == 200:
                st.success(f"Batch ingestion successful: {resp.json()}")
            else:
                st.error(f"Batch ingestion failed: {resp.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")

# Ingest Data Page
if st.sidebar.radio("Navigation", ["Query", "Analytics", "Ingest Data"]) == "Ingest Data":
    st.header("Ingest Data")
    st.subheader("Batch Ingestion")
    ingest_batch("ingest_all_structured", "Ingest All Structured Files (CSV)")
    ingest_batch("ingest_all_unstructured", "Ingest All Unstructured Files (PDF, DOCX, TXT, HTML)")
    st.markdown("---")
    st.subheader("Upload Structured Data (CSV)")
    uploaded_csv = st.file_uploader("Upload CSV File", type=["csv"])
    collection_name = st.text_input("Collection Name (optional)")
    if st.button("Upload CSV") and uploaded_csv is not None:
        files = {"file": (uploaded_csv.name, uploaded_csv.getvalue())}
        data = {"collection_name": collection_name or uploaded_csv.name.replace('.csv','')}
        try:
            resp = requests.post("http://localhost:8000/ingest/structured/csv", files=files, data=data)
            if resp.status_code == 200:
                st.success(f"CSV Ingested: {resp.json()}")
            else:
                st.error(f"CSV Ingestion failed: {resp.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")

# Add debug section to list documents in the selected collection
st.markdown("---")
st.subheader("Debug: List Documents in Collection")
if st.button("List Documents in Collection"):
    collection = st.session_state.get("selected_collection", "default")
    try:
        resp = requests.get(f"http://localhost:8000/debug/list_documents?collection={collection}")
        if resp.status_code == 200:
            docs = resp.json().get("documents", [])
            with st.expander(f"Documents in '{collection}' collection ({len(docs)})"):
                for i, doc in enumerate(docs):
                    st.write(f"{i+1}. {doc[:200]}{'...' if len(doc) > 200 else ''}")
        else:
            st.error(f"Error: {resp.text}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}") 