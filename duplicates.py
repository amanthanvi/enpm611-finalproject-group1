from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from model import Issue,Event
import config

class Duplicates:
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
 
        issues:List[Issue] = DataLoader().get_issues()
        
        duplicates:int = 0  
        duplicate_owner = []
        for issue in issues:        
            check = False
            for e in issue.events:
                if e.comment is not None and "duplicate" in e.comment:
                    if check == False:
                        duplicates+=1
                        check = True
                        print(issue.number)
                        duplicate_owner.append(issue.creator)
                
        print('\n\n'+str(duplicates)+'\n\n')
        
    

if __name__ == '__main__':
    # Invoke run method when running this module directly
    Duplicates().run()