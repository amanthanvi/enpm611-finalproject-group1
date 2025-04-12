from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from duplicates_finder import DuplicateFinder
from model import Issue,Event
import config

def compare_labels():
    """
    Compares the distribution of issue creation times by hour.
    """
    labels_dict:dict = {"none":0}
    DUP_status_list:List[Issue] = []
    ALL_issues:List[Issue] = DataLoader().get_issues()
    ALL_hourlist:List[float] = [0.0] * 24
    for issue in ALL_issues:
        if not issue.labels:
            labels_dict["none"] += 1
        else:
            for label in issue.labels:
                if label not in labels_dict:
                    labels_dict[label] = 1
                else:
                    labels_dict[label] += 1
            
                if "duplicate" in label:
                    DUP_status_list.append(issue)


    print(labels_dict)

    
    DUP_labels_dict:dict = {"none":0}
    DUP_issues:List[Issue] = DuplicateFinder().get_duplicate_issues()
    for issue in DUP_issues:
        if not issue.labels:
            DUP_labels_dict["none"] += 1
        else:
            for label in issue.labels:
                if label not in DUP_labels_dict:
                    DUP_labels_dict[label] = 1
                else:
                    DUP_labels_dict[label] += 1

    print(DUP_labels_dict)

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

    print("Of", len(DUP_issues), "issues with comments suggesting it as duplicate, only", len(found_original), "issues mentioned the orignial they were duplicating")

    possible_dups:int = not_counted+not_labeled+correct
    print("Number of issues with duplicate label but lack comments mentioning a duplicate: ", not_counted, "/", possible_dups)
    print("Number of issues with comments pointing to a duplicate number but no label: ", not_labeled_found, "/", possible_dups)
    print("Number of issues with comments suggesting duplicate but no label: ", not_labeled_not_found, "/", possible_dups)
    print("Number of issues that were identified as duplicates in both comments and label: ", correct, "/", possible_dups)


compare_labels()