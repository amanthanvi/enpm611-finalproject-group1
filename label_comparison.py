from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from duplicates_finder import DuplicateFinder
from model import Issue,Event
import config



class DuplicateLabelAnalysis:
    """
    Implements an example analysis of GitHub
    issues and outputs the result of that analysis.
    """
    
    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.USER:str = config.get_parameter('user')
    
    def run(self):
        """
        This feature focuses on labels for duplicate issues and what we can learn about them
        """

        # grabbing all issues and duplicate issues for comparison, and the dictionary list for how many of each label appears in duplicate issues
        ALL_issues:List[Issue] = DataLoader().get_issues()
        DUP_issues:List[Issue] = DuplicateFinder().get_duplicate_issues()
        DUP_labels_dict:dict = DuplicateFinder().get_label_count()

        # this for loop creates a dictionary entry for each label and sets its value to the number of appearances that label has
        # this also stores all of the issues with the duplicate label, which is different than how we decide what is a duplicate
        ALL_labels_dict:dict = {"none":0}
        DUP_status_list:List[Issue] = []
        for issue in ALL_issues:
            if not issue.labels:
                ALL_labels_dict["none"] += 1
            else:
                for label in issue.labels:
                    if label not in ALL_labels_dict:
                        ALL_labels_dict[label] = 1
                    else:
                        ALL_labels_dict[label] += 1
                
                    if "duplicate" in label:
                        DUP_status_list.append(issue)


        # sorting the labels by number of appearances
        ALL_sorted_labels = sorted(ALL_labels_dict, key=ALL_labels_dict.get, reverse=True)
        # making the following list of number of appearances
        ALL_sorted_vals = sorted(list(ALL_labels_dict.values()),reverse=True)
        # converting the number of appearances of each label to a % of issues they are in
        ALL_label_percent = [float(format(x*100/len(ALL_issues), '.2f')) for x in ALL_sorted_vals]

        # this does the same as the above 3 lines of code except for duplicate issues instead of all issues
        DUP_sorted_labels = sorted(DUP_labels_dict, key=DUP_labels_dict.get, reverse=True)
        DUP_sorted_vals = sorted(list(DUP_labels_dict.values()),reverse=True)
        DUP_label_percent = [float(format(x*100/len(DUP_issues), '.2f')) for x in DUP_sorted_vals]
    
        # this then compares the percentages of appearances per issue for the duplicates list and all issues list and finds the difference
        comparison_vals:List[float] = []
        for label in ALL_sorted_labels[:10]:
            percent_val = float(format(DUP_labels_dict[label]*100/len(DUP_issues), '.2f'))
            comparison_vals.append(percent_val)
        
        label_percent_delta = [float(format(a - b, '.2f')) for a, b in zip(comparison_vals, ALL_label_percent)]
        

        # these 3 plots present the top labels for each issue grouping, and the delta between then for the most common labels
        plt.figure(1)
        plt.bar(ALL_sorted_labels[:10], ALL_label_percent[:10])
        plt.xlabel('Label Name')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Percent of Issues')
        plt.title('Top 10 Labels for All Issues')
        
        plt.figure(2)
        plt.bar(DUP_sorted_labels[:10], DUP_label_percent[:10])
        plt.xlabel('Label Name')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Percent of Issues')
        plt.title('Top 10 Labels for Duplicate Issues')
        plt.show() 

        plt.figure(3)
        plt.bar(ALL_sorted_labels[:10], label_percent_delta)
        plt.xlabel('Label Name')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Percent of Issues Difference')
        plt.title('Percent of Labels for Duplicate Issues vs All Issues')
        plt.show() 

        # this for loop parses through the event comments for duplicate issues and finds whenever a number is mentioned after the word "duplicate"
        # finding the word help determine if the comments suggest an original issue for this one to be copying
        # this also compiles all of the issues that do not refer to the issues they are supposedly duplicating
        found_original:List[Issue] = []
        not_found_original:List[Issue] = []
        for issue in DUP_issues:
            check: bool = False
            for e in issue.events:
                if e.comment is not None and "duplicate" in e.comment and check == False:
                    post_dup: str = e.comment.split("duplicate")[1]
                    if "#" in post_dup:
                        post_hash: str = post_dup.split("#")[1]
                        num_unstripped: str = post_hash.split(" ")[0]
                        num_str: str = ""
                        for letter in num_unstripped:
                            if letter.isdigit():
                                num_str += letter
                            else:
                                break
                        if num_str != "":
                            number = int(num_str)
                            check = True
                            found_original.append(issue)
            if check == False:
                not_found_original.append(issue)
        
        # this counts all of the issues that are both labeled duplicates and refer to duplicates, determining them as correct
        # this also counts for when the label is not included, or the label is included but the word duplicate is never mentioned in the events
        not_counted:int = 0
        not_labeled:int = 0
        not_labeled_found:int = 0
        not_labeled_not_found:int = 0
        correct:int = 0
        for issue in ALL_issues:
            if issue in DUP_status_list and issue in DUP_issues:
                correct += 1
            elif issue in DUP_status_list and issue not in DUP_issues:
                not_counted += 1
            elif issue in DUP_issues and issue not in DUP_status_list:
                not_labeled += 1
                if issue in found_original:
                    not_labeled_found += 1
                elif issue in not_found_original:
                    not_labeled_not_found += 1
                else: 
                    print("uh oh")
        
        possible_dups:int = not_counted+not_labeled+correct

        print("\nOf", len(DUP_issues), "issues with comments suggesting it as duplicate, only", len(found_original), "issues mentioned the orignial they were duplicating")
        print("Number of issues with duplicate label but lack comments mentioning a duplicate: ", not_counted, "/", possible_dups)
        print("Number of issues with comments pointing to a duplicate number but no label: ", not_labeled_found, "/", possible_dups)
        print("Number of issues with comments suggesting duplicate but no label: ", not_labeled_not_found, "/", possible_dups)
        print("Number of issues that were identified as duplicates in both comments and label: ", correct, "/", possible_dups, "\n")


if __name__ == '__main__':
    # Invoke run method when running this module directly
    DuplicateLabelAnalysis().run()