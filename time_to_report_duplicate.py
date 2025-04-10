from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from duplicates_finder import DuplicateFinder
from model import Issue,Event
import config
from datetime import datetime


issues:List[Issue] = DuplicateFinder().get_duplicate_issues()
events:list[Event] = DuplicateFinder().get_duplicate_events()
time_list:List[datetime] = [events[i].event_date-issues[i].created_date for i in range(len(issues))]
days_0_1:int = 0
days_1_5:int = 0
days_5_30:int = 0
days_30plus:int = 0
for time in time_list:
    if time.days == 0:
        days_0_1 +=1
    elif time.days > 0 and time.days < 8:
        days_1_5 +=1
    elif time.days > 7 and time.days < 30:
        days_5_30 +=1  
    elif time.days > 30:
        days_30plus +=1 
    else:
        print(time)

print(days_0_1, days_1_5, days_5_30, days_30plus)
