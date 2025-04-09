from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from duplicates_finder import DuplicateFinder
from model import Issue,Event
import config

ALL_issues:List[Issue] = DataLoader().get_issues()
ALL_hourlist:List[float] = [0.0] * 24
for issue in ALL_issues:
    ALL_hourlist[issue.created_date.hour] +=1

DUP_issues:List[Issue] = DuplicateFinder().get_duplicate_issues()
DUP_hourlist:List[float] = [0.0] * 24
for issue in DUP_issues:
    DUP_hourlist[issue.created_date.hour] +=1


ALL_hours_percent = [float(format(x*100/len(ALL_issues), '.2f')) for x in ALL_hourlist]
DUP_hours_percent = [float(format(x*100/len(DUP_issues), '.2f')) for x in DUP_hourlist]
hour_percent_delta = [float(format(a - b, '.2f')) for a, b in zip(DUP_hours_percent, ALL_hours_percent)]

print(ALL_hours_percent)
print(DUP_hours_percent)
print(hour_percent_delta)