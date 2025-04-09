from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from model import Issue,Event
import config

class DuplicateFinder:
    """
    Loads the issue data into a runtime object.
    """
    
    def __init__(self):
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

