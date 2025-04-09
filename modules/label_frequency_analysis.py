from typing import List
from collections import Counter

from data_loader import DataLoader
from model import Issue

def label_frequency_analysis_run():
    """
    Analyzes the frequency of labels across all issues.
    """
    issues: List[Issue] = DataLoader().get_issues()
    
    # Collect all labels from all issues
    all_labels = [label for issue in issues for label in issue.labels]
    
    # Count the frequency of each label
    label_counts = Counter(all_labels)
    
    # Offer sorting options
    print("\nHow would you like to sort the labels?")
    print("1: By quantity (descending)")
    print("2: Alphabetically (ascending)")
    while True:
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice == 1:
                sorted_labels = label_counts.most_common()
                break
            elif choice == 2:
                sorted_labels = sorted(label_counts.items())
                break
            else:
                print("Invalid choice. Please select 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Print the results
    print("\nLabel Frequency Analysis:")
    for label, count in sorted_labels:
        print(f"{label}: {count}")
