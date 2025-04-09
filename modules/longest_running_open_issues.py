from typing import List
from datetime import datetime, timezone
from data_loader import DataLoader
from model import Issue

def longest_running_open_issues_run():
    """
    Displays the 20 longest-running open issues.
    """
    issues: List[Issue] = DataLoader().get_issues()
    
    # Filter open issues and calculate their age
    open_issues = [
        (issue.number, issue.title, (datetime.now(timezone.utc) - issue.created_date).days)
        for issue in issues if issue.state == "open" and issue.created_date is not None
    ]
    
    # Sort by age in descending order
    sorted_issues = sorted(open_issues, key=lambda x: x[2], reverse=True)
    
    # Display the top 20 longest-running open issues
    print("\nLongest Running Open Issues (Top 20):")
    print(f"{'Issue ID':<10} {'Title':<50} {'Age (days)':<10}")
    print("-" * 70)
    for issue_id, title, age in sorted_issues[:20]:
        print(f"{issue_id:<10} {title[:47] + '...' if len(title) > 50 else title:<50} {age:<10}")
