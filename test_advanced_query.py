import requests
import json

API_URL = "http://localhost:8000/query"

payload = {
    "query": "Show me the latest sales report.",
    "collection": "Weekly_Sales_Report_June_Week3_2024",
    "optimize_query": True,
    "context": {"previous_query": "Show me Q1 2024 sales."},
    "sources": ["Weekly_Sales_Report_June_Week3_2024", "Q2_2024_Business_Report"],
    "generate_insights": True
}

headers = {"Authorization": "Bearer <YOUR_TOKEN>", "Content-Type": "application/json"}

# If you don't use auth, remove the Authorization header

response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
print("Status:", response.status_code)
print("Response:", response.json()) 