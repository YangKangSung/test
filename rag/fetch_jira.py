import os
import json
from jira import JIRA
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JiraFetcher:
    def __init__(self, server, username=None, token=None):
        self.server = server
        self.username = username
        self.token = token
        self.jira = self._connect()

    def _connect(self):
        if self.username and self.token:
            return JIRA(server=self.server, basic_auth=(self.username, self.token))
        else:
            # Anonymous access
            print(f"Connecting to {self.server} anonymously...")
            return JIRA(server=self.server)

    def fetch_issues(self, jql, max_results=100):
        print(f"Fetching issues from {self.server} with JQL: {jql}")
        try:
            issues = self.jira.search_issues(jql, maxResults=max_results)

            data = []
            for issue in issues:
                issue_data = {
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'description': issue.fields.description,
                    'status': issue.fields.status.name,
                    'priority': issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else 'None',
                    'created': issue.fields.created,
                    'updated': issue.fields.updated,
                    'comments': []
                }

                if hasattr(issue.fields, 'comment') and issue.fields.comment:
                     for comment in issue.fields.comment.comments:
                         # Handle cases where author might be missing or anonymous
                         author_name = 'Unknown'
                         if hasattr(comment, 'author') and hasattr(comment.author, 'displayName'):
                             author_name = comment.author.displayName

                         issue_data['comments'].append({
                             'author': author_name,
                             'body': comment.body,
                             'created': comment.created
                         })

                data.append(issue_data)
            return data
        except Exception as e:
            print(f"Error fetching issues: {e}")
            return []

    def save_to_json(self, data, filename='jira_data.json'):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Successfully saved {len(data)} issues to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")

def main():
    server = os.getenv('JIRA_SERVER')
    username = os.getenv('JIRA_USERNAME')
    token = os.getenv('JIRA_API_TOKEN')

    if not server:
        print("Error: JIRA_SERVER environment variable not set.")
        return

    fetcher = JiraFetcher(server, username, token)

    # Example JQL
    jql_query = 'updated >= -30d ORDER BY updated DESC'

    data = fetcher.fetch_issues(jql_query)
    if data:
        fetcher.save_to_json(data)

if __name__ == "__main__":
    main()
