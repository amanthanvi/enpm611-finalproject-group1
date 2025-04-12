from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from duplicates_finder import DuplicateFinder
from model import Issue,Event
import config


def compare_origin():
  

    """
    """
    DUP_issues:List[Issue] = DuplicateFinder().get_duplicate_issues()
    found_original:List[Issue] = []
    original_number:List[int] = []
    number_delta:list[int] = []

    not_found_original:List[Issue] = []
    for issue in DUP_issues:
        check: bool = False
        for e in issue.events:
            if e.comment is not None and "duplicate" in e.comment and check == False:
                post_dup: str = e.comment.split("duplicate")[1]
                if "#" in post_dup:
                    post_hash: str = post_dup.split("#")[1]
                    num_unstripped: str = post_hash.split(" ")[0]
                    num_str: str = ""
                    for letter in num_unstripped:
                        if letter.isdigit():
                            num_str += letter
                        else:
                            break
                    if num_str != "":
                        number = int(num_str)
                        check = True
                        found_original.append(issue)
                        original_number.append(number)
                        number_delta.append(issue.number-number)
        if check == False:
            not_found_original.append(issue)

    within_5:int = 0
    backwards_dup:float = 0
    pos_avg:int = 0
    for x in number_delta:
        if x < 0:
            backwards_dup += 1
        else:
            pos_avg += x
        if abs(x) < 5:
            within_5 += 1

    pos_avg = float(format(pos_avg/(len(number_delta)-backwards_dup), '.0f'))
    
    
    seen = set()
    repeats:dict = {}
    for item in original_number:
        if item in seen:
            if "Issue "+str(item) not in repeats:
                repeats["Issue "+str(item)] = 2
            else:
                repeats["Issue "+str(item)] += 1
        else:
            seen.add(item)

    sorted_repeats = sorted(repeats, key=repeats.get, reverse=True)
    sorted_counts = sorted(list(repeats.values()),reverse=True)

    print("Out of", len(DUP_issues), "issues, there are", len(found_original), "issues that specify the issue they are duplicating.")
    print("There are", within_5, "issues that duplicate an issue within 5 of them (forward or backward). ")
    print("These are going to be issues that get brought up at the same time and resolved with the issue they refer to. ")
    print("Considering how few of these there are, that means that the programmers rarely solve issues together (or at least report that they do).")
    print("There are", backwards_dup, "issues that are commented as duplicating an issue made after them. ")
    print("This means the programmers are not staying consistant with who is actually the duplicate when classifying issues")
    print("Not including those that refer to an issue after them, the average amount of issues between the original and duplicate is:", pos_avg, "issues")
    print("Number of issues that are duplicated more than once:", len(repeats))

    plt.figure(1)
    plt.bar(sorted_repeats[:25], sorted_counts[:25])
    plt.xlabel('Issues')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Times Duplicated')
    plt.title('Top 25 Most Duplicated Issues')
    plt.show() 

compare_origin()