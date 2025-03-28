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
        duplicate_reporter = []
        for issue in issues:        
            check = False
            for e in issue.events:
                if e.comment is not None and "duplicate" in e.comment:
                    if check == False:
                        duplicates+=1
                        check = True
                        print(issue.number)
                        duplicate_owner.append(issue.creator)
                        duplicate_reporter.append(e.author)
                
        print('\n\n'+str(duplicates)+'\n\n')
        
                ### BAR CHART
        top_n:int = 50
        title1:string = f"Top {top_n} duplicate issue creators"
        df = pd.DataFrame(duplicate_owner)
        df_hist = df.value_counts().nlargest(top_n).plot(kind="bar", figsize=(14,8), title=title1)
        df_hist.set_xlabel("Creator Names")
        df_hist.set_ylabel("# of issues created that were duplicates")
        plt.show() 

        title2:string = f"Top {top_n} duplicate issue reporters"
        df = pd.DataFrame(duplicate_reporter)
        df_hist = df.value_counts().nlargest(top_n).plot(kind="bar", figsize=(14,8), title = title2)
        df_hist.set_xlabel("Creator Names")
        df_hist.set_ylabel("# of issues that author reported as duplicate")
        plt.show() 
    

if __name__ == '__main__':
    # Invoke run method when running this module directly
    Duplicates().run()