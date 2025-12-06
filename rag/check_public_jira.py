import requests
try:
    response = requests.get('https://issues.apache.org/jira/rest/api/2/search?jql=project=HADOOP&maxResults=1')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success")
except Exception as e:
    print(f"Error: {e}")
