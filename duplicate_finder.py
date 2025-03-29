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
    # Parameter is passed in via command line (--user)
        self.USER:str = config.get_parameter('user')
    

    def find_duplicate_issues(self):
        issues:List[Issue] = DataLoader().get_issues()
        duplicates:int = 0  
        duplicate_issues:List[Issue] = []
        for issue in issues:        
            check:bool = False
            for e in issue.events:
                if e.comment is not None and "duplicate" in e.comment:
                    if check == False:
                        duplicates+=1
                        check = True
                        print(issue.number)
                        duplicate_issues.append(issue)
        return duplicate_issues
        
    def find_duplicate_events(self):
        issues:List[Issue] = DataLoader().get_issues()
        duplicates:int = 0  
        duplicate_events:List[Event] = []
        for issue in issues:        
            check:bool = False
            for e in issue.events:
                if e.comment is not None and "duplicate" in e.comment:
                    if check == False:
                        duplicates+=1
                        check = True
                        print(issue.number)
                        duplicate_events.append(e)
        return duplicate_events

