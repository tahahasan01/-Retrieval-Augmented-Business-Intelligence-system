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

# --- Ingest Data Page ---
elif page == "Ingest Data":
    st.title("Ingest Unstructured Data 📄")
    uploaded_files = st.file_uploader("Upload files (PDF, DOCX, TXT, HTML)", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write(f"File uploaded: {uploaded_file.name}")
            if st.button(f"Ingest {uploaded_file.name}", key=uploaded_file.name):
                with st.spinner(f"Uploading and ingesting {uploaded_file.name}..."):
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    try:
                        response = requests.post(f"{API_URL}/ingestion/ingest_unstructured", files=files)
                        if response.ok:
                            st.success(f"{uploaded_file.name} ingested successfully!")
                        else:
                            st.error("Error: " + response.text)
                    except Exception as e:
                        st.error(f"Failed to upload {uploaded_file.name}: {e}")
        st.info("You can upload and ingest multiple files.")
    # Show previously ingested files (if backend supports it)
    st.subheader("Previously Ingested Files")
    try:
        response = requests.get(f"{API_URL}/ingestion/ingested_files")
        if response.ok:
            files = response.json().get("files", [])
            if files:
                st.table(pd.DataFrame(files, columns=["File Name", "Ingested At"]))
            else:
                st.info("No files ingested yet.")
        else:
            st.warning("Could not fetch ingested files list.")
    except Exception:
        st.warning("File listing not available.") 