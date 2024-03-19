
import requests
import json

# Placeholder values for API credentials and endpoint
API_URL = "https://PLACEHOLDER/connect/api/v1/cases"
TENANT_ID = "PLACEHOLDER_TENANT_ID"
API_TOKEN = "PLACEHOLDER_API_TOKEN" 

def get_api_data(api_url, tenant_id, api_token, limit=10):
    headers = {"Authorization": f"Bearer {api_token}"}
    params = {
        "tenant_id": tenant_id,
        "limit": limit,
        "sort": "case_score",
        "order": "desc"
    }
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def fetch_top_cases():
    data = get_api_data(API_URL, TENANT_ID, API_TOKEN)
    if data:
        print("Top cases data:")
        print(json.dumps(data, indent=4))
    else:
        print("Failed to fetch data")

# Example usage
fetch_top_cases()
