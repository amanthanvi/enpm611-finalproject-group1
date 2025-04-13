from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from duplicates_finder import DuplicateFinder
from model import Issue,Event
import config

class Duplicates:
    
    def __init__(self):
        pass
    
    def run(self):

        duplicate_issues:List[Issue] = DuplicateFinder().get_duplicate_issues()
        duplicate_events:List[Event] = DuplicateFinder().get_duplicate_events()
                       
        top_n:int = 50
        title1:str = f"Top {top_n} duplicate issue creators"
        df = pd.DataFrame.from_records([{'creator':issue.creator} for issue in duplicate_issues])
        df_hist = df.groupby(df["creator"]).value_counts().nlargest(top_n).plot(kind="bar", figsize=(14,8), title=title1)
        df_hist.set_xlabel("Creator Names")
        df_hist.set_ylabel("# of issues created")
        plt.show() 

        title2:str = f"Top {top_n} duplicate issue reporters"
        df = pd.DataFrame.from_records([{'author':e.author} for e in duplicate_events])
        df_hist = df.groupby(df["author"]).value_counts().nlargest(top_n).plot(kind="bar", figsize=(14,8), title=title2)
        df_hist.set_xlabel("Creator Names")
        df_hist.set_ylabel("# of issues that author reported as duplicates")
        plt.show() 

def analyze_creators():
    """
    Analyzes duplicate issue creators and reporters.
    """
    Duplicates().run()
    

if __name__ == '__main__':
    # Invoke run method when running this module directly
    Duplicates().run()