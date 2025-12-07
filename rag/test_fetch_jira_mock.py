
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add current directory to path so we can import fetch_jira
sys.path.append(os.path.join(os.getcwd(), 'rag'))

from fetch_jira import JiraFetcher

class TestJiraFetcher(unittest.TestCase):
    def setUp(self):
        # Mock the JIRA connection in __init__
        with patch('fetch_jira.JIRA'):
            self.fetcher = JiraFetcher('http://jira.example.com', 'user', 'token')

    def test_format_content_for_rag(self):
        # Create a mock issue
        mock_issue = MagicMock()
        mock_issue.key = 'TEST-123'
        mock_issue.fields.summary = 'Test Summary'
        mock_issue.fields.description = 'Test Description'
        mock_issue.fields.status.name = 'Open'
        mock_issue.fields.priority.name = 'High'

        # Mock comments
        mock_comment1 = MagicMock()
        mock_comment1.author.displayName = 'Alice'
        mock_comment1.body = 'First comment'
        mock_comment1.created = '2023-01-01T10:00:00.000+0000'

        mock_comment2 = MagicMock()
        mock_comment2.author.displayName = 'Bob'
        mock_comment2.body = 'Second comment'
        mock_comment2.created = '2023-01-02T10:00:00.000+0000'

        mock_issue.fields.comment.comments = [mock_comment1, mock_comment2]

        formatted_content = self.fetcher._format_content_for_rag(mock_issue)

        print("Formatted Content:\n", formatted_content)

        self.assertIn("Title: Test Summary", formatted_content)
        self.assertIn("Status: Open", formatted_content)
        self.assertIn("Priority: High", formatted_content)
        self.assertIn("Description:\nTest Description", formatted_content)
        self.assertIn("Comments:", formatted_content)
        self.assertIn("Alice: First comment", formatted_content)
        self.assertIn("Bob: Second comment", formatted_content)

    def test_fetch_issues_structure(self):
        # Mock search_issues return value
        mock_issue = MagicMock()
        mock_issue.key = 'TEST-123'
        mock_issue.fields.summary = 'Test Summary'
        mock_issue.fields.description = 'Test Description'
        mock_issue.fields.status.name = 'Open'
        mock_issue.fields.priority.name = 'High'
        mock_issue.fields.created = '2023-01-01'
        mock_issue.fields.comment.comments = []

        self.fetcher.jira.search_issues.return_value = [mock_issue]

        data = self.fetcher.fetch_issues('some jql')

        self.assertEqual(len(data), 1)
        item = data[0]

        self.assertEqual(item['id'], 'TEST-123')
        self.assertEqual(item['title'], 'Test Summary')
        self.assertIn('Title: Test Summary', item['content'])
        self.assertEqual(item['link'], 'http://jira.example.com/browse/TEST-123')
        self.assertEqual(item['create_date'], '2023-01-01')

if __name__ == '__main__':
    unittest.main()
