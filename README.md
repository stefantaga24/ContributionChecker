# Collaboration Analyser

# 1. Introduction

Contribution checker is a streamlit powered app that given a GitHub repository either outputs a heatmap showing the level of collaboration between developers or the top five pairs 
of developers that have the highest level of collaboration. The user can also select the dates between which they want to see the repository activity.

# 2. Solution description

- While the app may be slow if a large number of commits are trying to be evaluated (>5000), this is due to the fact that it uses the GitHub graphQL API and only asks for 
50 commits at a time. This is done to prevent the github API from blocking our requests.
- The level of collaboration is calculated as follows: if two developers A and B have A_X, respectively B_X commits on the same file X, then their level of collaboration ,
  Col(A,B) increases with A_X+B_X.

# 3. Installation
- Clone the repository locally
- Run `install -r requirements.txt` in the console 
- Then move to the githubAnalyser folder by running `cd githubAnalyser` in the console
- Then to start the app write `streamlit run app.py`
- The app will be running in the url given by streamlit in the console
# 4. App example
- This is how the front panel looks like:
![grafik](https://github.com/stefantaga24/ContributionChecker/assets/145774127/97c1ce32-acc1-454f-8af2-72cdd02a0639)

- This is a heatmap example after being run on almost 5000 commits
![grafik](https://github.com/stefantaga24/ContributionChecker/assets/145774127/cf176c7d-568d-4a9e-a038-3ae52630b7f2)
- Another heatmap example on a smaller sample size
![grafik](https://github.com/stefantaga24/ContributionChecker/assets/145774127/c988daad-8b16-4194-9542-b79644ab0f90)
