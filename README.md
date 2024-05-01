# Collaboration Analyser

# 1. Introduction

Contribution checker is a streamlit powered app that given a GitHub repository either outputs a heatmap showing the level of collaboration between developers or the top five pairs 
of developers that have the highest level of collaboration. The user can also select the dates between which they want to see the repository activity.

# 2. Solution description

- While the app may be slow if a large number of commits are trying to be evaluated (>5000), this is due to the fact that it uses the GitHub graphQL API and only asks for 
50 commits at a time. This is done to prevent the github API from blocking our requests.
- The level of collaboration is calculated as follows: if two developers A and B have A_X, respectively B_X commits on the same file X, then their level of collaboration ,
  Col(A,B) increases with A_X+B_X. 
![grafik](https://github.com/stefantaga24/ContributionChecker/assets/145774127/cf176c7d-568d-4a9e-a038-3ae52630b7f2)

![grafik](https://github.com/stefantaga24/ContributionChecker/assets/145774127/c988daad-8b16-4194-9542-b79644ab0f90)
