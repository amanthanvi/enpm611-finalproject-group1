from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from .duplicates_finder import DuplicateFinder
from model import Issue,Event
import config
from datetime import datetime


def find_original_issues():
    """
    Finds and prints the original issues referenced in duplicate comments.
    """
    DUP_issues: List[Issue] = DuplicateFinder().get_duplicate_issues()

    for issue in DUP_issues:
        check: bool = False
        for e in issue.events:
            if e.comment is not None and "duplicate" in e.comment and check == False:
                post_dup: str = e.comment.split("duplicate")[1]
                if "#" in post_dup:
                    post_hash: str = post_dup.split("#")[1]
                    num_unstripped: str = post_hash.split(" ")[0]
                    print(num_unstripped)
                    num_str: str = ""
                    for letter in num_unstripped:
                        if letter.isdigit():
                            num_str += letter
                        else:
                            break
                    if num_str != "":
                        number = int(num_str)
                        check = True
                        print(issue.number, number)
                    else:
                        print(issue.number, "failed")
