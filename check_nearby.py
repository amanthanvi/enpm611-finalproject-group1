from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from duplicates_finder import DuplicateFinder
from model import Issue,Event
import config
from datetime import datetime

DUP_issues:List[Issue] = DuplicateFinder().get_duplicate_issues()


sorted_issues = sorted(DUP_issues,key=lambda x: x.number)
next_to_list:List[Issue] = []
for i in range(1,len(sorted_issues)):
    if sorted_issues[i].number-sorted_issues[i-1].number == 1:
        next_to_list.append(sorted_issues[i])

[print(issue.number) for issue in sorted_issues]
[print(issue.number) for issue in next_to_list]



