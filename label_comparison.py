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
        Compares labels between all issues and duplicate issues, seeing which label is more frequent for duplicate issues
        Also looks at what are considered duplicate issues, by label or by mention in comment
        """
        ALL_labels_dict:dict = {"none":0}
        DUP_status_list:List[Issue] = []
        ALL_issues:List[Issue] = DataLoader().get_issues()
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

        ALL_sorted_labels = sorted(ALL_labels_dict, key=ALL_labels_dict.get, reverse=True)
        ALL_sorted_vals = sorted(list(ALL_labels_dict.values()),reverse=True)
        ALL_label_percent = [float(format(x*100/len(ALL_issues), '.2f')) for x in ALL_sorted_vals]
        # Create the plot
        
        
        DUP_issues:List[Issue] = DuplicateFinder().get_duplicate_issues()
        DUP_labels_dict:dict = DuplicateFinder().get_label_count()


        DUP_sorted_labels = sorted(DUP_labels_dict, key=DUP_labels_dict.get, reverse=True)
        DUP_sorted_vals = sorted(list(DUP_labels_dict.values()),reverse=True)
        DUP_label_percent = [float(format(x*100/len(DUP_issues), '.2f')) for x in DUP_sorted_vals]
    

        comparison_vals:List[float] = []
        for label in ALL_sorted_labels[:10]:
            percent_val = float(format(DUP_labels_dict[label]*100/len(DUP_issues), '.2f'))
            comparison_vals.append(percent_val)
        
        label_percent_delta = [float(format(a - b, '.2f')) for a, b in zip(comparison_vals, ALL_label_percent)]
        
        # Create the plot
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

        print("\nOf", len(DUP_issues), "issues with comments suggesting it as duplicate, only", len(found_original), "issues mentioned the orignial they were duplicating")

        possible_dups:int = not_counted+not_labeled+correct
        print("Number of issues with duplicate label but lack comments mentioning a duplicate: ", not_counted, "/", possible_dups)
        print("Number of issues with comments pointing to a duplicate number but no label: ", not_labeled_found, "/", possible_dups)
        print("Number of issues with comments suggesting duplicate but no label: ", not_labeled_not_found, "/", possible_dups)
        print("Number of issues that were identified as duplicates in both comments and label: ", correct, "/", possible_dups, "\n")


if __name__ == '__main__':
    # Invoke run method when running this module directly
    DuplicateLabelAnalysis().run()