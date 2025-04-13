from typing import List
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from data_loader import DataLoader
from model import Issue

def longest_running_open_issues_run():
    """
    Displays the user-specified number of longest-running open issues.
    """
    issues: List[Issue] = DataLoader().get_issues()
    
    # Ask the user how many issues to display
    try:
        num_issues = int(input("Enter the number of longest-running open issues to display: "))
        if num_issues <= 0:
            raise ValueError("The number must be greater than 0.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
    
    # Filter open issues and calculate their age
    open_issues = [
        (issue.number, issue.title, relativedelta(datetime.now(timezone.utc), issue.created_date))
        for issue in issues if issue.state == "open" and issue.created_date is not None
    ]
    
    # Sort by age in descending order
    sorted_issues = sorted(open_issues, key=lambda x: (x[2].years, x[2].months, x[2].days), reverse=True)
    
    # Display the specified number of longest-running open issues
    print(f"\nLongest Running Open Issues (Top {num_issues}):")
    print(f"{'Issue ID':<10} {'Title':<50} {'Age':<15}")
    print("-" * 75)
    for issue_id, title, age in sorted_issues[:num_issues]:
        age_str = f"{age.years}y, {age.months}m, {age.days}d"
        print(f"{issue_id:<10} {title[:47] + '...' if len(title) > 50 else title:<50} {age_str:<15}")
