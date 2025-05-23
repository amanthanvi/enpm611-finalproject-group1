from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from model import Issue,Event
import config

class DuplicateFinder:
    """
    This loads in all of the issues and finds which ones have comments refering to duplicates. It then stores those related issues and comments in their own lists
    """
    
    def __init__(self):

        # this finds the duplicate issues and events and stores them
        issues:List[Issue] = DataLoader().get_issues()
        duplicate_issues:List[Issue] = []
        duplicate_events:List[Event] = []
        for issue in issues:        
            check:bool = False
            for e in issue.events:
                if e.comment is not None and "duplicate" in e.comment:
                    if check == False:
                        check = True
                        duplicate_issues.append(issue)
                        duplicate_events.append(e)

        self.duplicate_issues = duplicate_issues
        self.duplicate_events = duplicate_events
    

    def get_duplicate_issues(self):
        return self.duplicate_issues
        
    def get_duplicate_events(self):
        return self.duplicate_events
    
    def get_label_count(self):
        # this function creates a dictionary which goes through the duplicate issues and counts how many of each labels appears, then returns the dictionary
        DUP_labels_dict:dict = {"none":0}
        for issue in self.duplicate_issues:
            if not issue.labels:
                DUP_labels_dict["none"] += 1
            else:
                for label in issue.labels:
                    if label not in DUP_labels_dict:
                        DUP_labels_dict[label] = 1
                    else:
                        DUP_labels_dict[label] += 1
        return DUP_labels_dict

def find_duplicates():
    """
    Finds and returns duplicate issues and events.
    """
    finder = DuplicateFinder()
    print("Duplicate issues:", finder.get_duplicate_issues())
    print("Duplicate events:", finder.get_duplicate_events())

