import unittest
from fetch_jira import JiraFetcher
import os

class TestJiraFetcher(unittest.TestCase):
    def test_apache_jira_public_access(self):
        # Use Apache Jira which allows anonymous read access for some projects
        server = 'https://issues.apache.org/jira'

        print(f"\nTesting connection to {server}...")
        fetcher = JiraFetcher(server) # Anonymous

        # Query for a stable project like HADOOP
        jql = 'project = HADOOP AND status = Resolved ORDER BY created DESC'

        print(f"Running JQL: {jql}")
        issues = fetcher.fetch_issues(jql, max_results=5)

        self.assertIsNotNone(issues)
        self.assertTrue(len(issues) > 0, "Should fetch at least one issue")

        print(f"Fetched {len(issues)} issues.")
        first_issue = issues[0]
        print(f"Sample Issue: {first_issue['key']} - {first_issue['summary']}")

        self.assertIn('key', first_issue)
        self.assertIn('summary', first_issue)
        self.assertTrue(first_issue['key'].startswith('HADOOP-'))

        # Test saving
        output_file = 'test_jira_data.json'
        fetcher.save_to_json(issues, output_file)
        self.assertTrue(os.path.exists(output_file))

        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
