from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from duplicates_finder import DuplicateFinder
from model import Issue,Event
import config
from datetime import datetime, timedelta


class DuplicateTime:
    
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

        print("\nThe percent of issues created in each hour increment in a day between Duplicate Issues vs All Issues:")
        for hour in range(len(hour_percent_delta)):
            print("Hour", hour+1, ":", hour_percent_delta[hour], "|" , end=" ")
        print("\nThere does not appear to be any timespan where duplicates are made more frequently than the average issue")

        """
        Reports the time taken to mark issues as duplicates.
        """
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

        sumval = sum(time_list,timedelta())
        avg_time = sumval/len(time_list)


        time_list_bug:List[datetime] = []
        time_list_triage:List[datetime] = []
        time_list_feature:List[datetime] = []
        for i in range(len(issues)):
            if "kind/bug" in issues[i].labels:
                time_list_bug.append(events[i].event_date-issues[i].created_date)
            if "status/triage" in issues[i].labels:
                 time_list_triage.append(events[i].event_date-issues[i].created_date)
            if "kind/feature" in issues[i].labels:
                time_list_feature.append(events[i].event_date-issues[i].created_date)
        
        sumval_bug = sum(time_list_bug,timedelta())
        avg_time_bug = sumval_bug/len(time_list_bug)
        sumval_triage = sum(time_list_triage,timedelta())
        avg_time_triage = sumval_triage/len(time_list_triage)
        sumval_feature = sum(time_list_feature,timedelta())
        avg_time_feature = sumval_feature/len(time_list_feature)



        print("\nNumber of days between when the issue is reported, and then labeled as a duplicate:")
        print("Days 0-1:", days_0_1, "| Days 1-5:", days_1_5, "| Days 5-30:", days_5_30, "| Days 30+:", days_30plus)
        print("\nAverage time between when a duplicate issue created and when it is reported", avg_time)
        print("\nAverage time for an duplicate issue with 'kind/bug' label to be reported:",avg_time_bug)
        print("Average time for an duplicate issue with 'status/triage' label to be reported:",avg_time_triage)
        print("Average time for an duplicate issue with 'kind/feature' label to be reported:",avg_time_feature,"\n")
        print("It might make sense for the feature labeled issues take the longest because some features may not be implementable until someone tries to implement something similar.")
        print("This then produces a situation where solving the original issue becomes easier in the process, and the issue is marked as duplicate")




if __name__ == '__main__':
    # Invoke run method when running this module directly
    DuplicateTime().run()