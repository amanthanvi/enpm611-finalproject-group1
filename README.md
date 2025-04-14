# ENPM611 Project 

# Project Theme: Duplicates
This Project intends to examine duplicate issues by investigating when they were made, what labels they have, and what issues they duplicate.
What defines a duplicate issue in this project are those which have event comments suggesting so. While there is a duplicate label that is often attached to issues, we will show as part of our analysis that is not as useful.

# How to Run:
Simply run the file "run.py" and add "--feature #" where the number is 0-3.
When you run a feature, you get to choose which data set you use. entering 1 or 2 for the associated data set will use the one selected. 

Feature 0 is the example analysis given in the project template. 

# Feature 1:
This feature examines what % of duplicate issues certain labels make up (will total over 100% as many issues have multiple labels). It then compares that % spread to the average issue and sees which labels are more common for duplicates. 
The feature then looks into what issues are labeled duplicates, and which of those thought to be duplicates actually reference the issue they are duplicating. Finally, it will show how many issues are thought to be duplicates, how many reference being a duplicate, how many reference the original issue, how many do not, and how many are both identified as duplicates in the event comments as well as the issue label.

# Feature 2:
This feature also looks at what issues reference the issues they are duplicating. It also displays how many issues duplicate an issue with a number within 5 of them. Some issues also reference issues that were made after them, so the feature looks into what labels those issues tend to have. Finally, the feature looks at which issues are most duplicated.

# Feature 3:
This feature is a bit more general than the previous 2 but focuses a bit more on timing. The first thing it does is shows which user is most likely to make a duplicate issue, and who is the most likely to identify the issue as a duplicate. It then investigates if duplicate issues are more frequently made at certain times of day than the average issue. Finally it looks at how long it takes for the average duplicate to be identified as one, and how that compares between issues with certain labels.
