import argparse
import json
import github_api as hubAPI
import time
import tqdm
import streamlit as st
import datetime
import pandas as pd
from matplotlib import pyplot as plt 
import seaborn as sns

def update_author_pairs(author_pairs,data):
    file_authors = {} 
    for node in data["data"]["repository"]["defaultBranchRef"]["target"]["history"]["nodes"]:
        associatedPullRequests = node["associatedPullRequests"]
        for fileNode in associatedPullRequests["nodes"]:
                author = fileNode['author']['login']
                for file in fileNode["files"]["nodes"]:
                    if not (file["path"] in file_authors):
                        file_authors[file["path"]] = {}
                    if not (author in file_authors[file["path"]]):
                        file_authors[file["path"]][author] = 0
                    file_authors[file["path"]][author] = file_authors[file["path"]][author] + 1
    for file in file_authors:
        for author1 in file_authors[file]:
            for author2 in file_authors[file]:
                if (author1 < author2):
                    if not ((author1,author2) in author_pairs):
                        author_pairs[(author1,author2)] = 0
                    author_pairs[(author1,author2)] = author_pairs[(author1,author2)] + file_authors[file][author1] + file_authors[file][author2]


def analyze_command_graphQL_API(repository,start,end,outputOption):

    isoFormatStart = datetime.datetime(start.year,start.month,start.day,0,0,0).isoformat()
    isoFormatEnd = datetime.datetime(end.year,end.month,end.day,0,0,0).isoformat()
    no_pages = 1
    commit_number = hubAPI.get_number_of_commits_with_graphQLAPI(repository
                                                                 ,isoFormatStart
                                                                 ,isoFormatEnd)
    st.write(f"Total number of commits to be evaluated : {commit_number}")
    progress_bar = st.progress(0, text= "Current commits status")
    data = hubAPI.get_commits_with_graphQLAPI(repository,isoFormatStart
                                                        ,isoFormatEnd)
    author_pairs = {}
    update_author_pairs(author_pairs,data)
    dataHistory = data["data"]["repository"]["defaultBranchRef"]["target"]["history"]
    end_cursor = dataHistory['pageInfo']['endCursor']
    has_next_page = dataHistory['pageInfo']['hasNextPage']
    progress_bar.progress(min(no_pages*50,commit_number)/commit_number , text = "Current commits status")
    time.sleep(1)
    no_pages = no_pages+1
    while has_next_page:
        data = hubAPI.get_commits_with_graphQLAPI_with_cursor(repository,end_cursor
                                                                ,isoFormatStart
                                                                ,isoFormatEnd)
        update_author_pairs(author_pairs,data)
        dataHistory = data["data"]["repository"]["defaultBranchRef"]["target"]["history"]
        end_cursor = dataHistory['pageInfo']['endCursor']
        has_next_page = dataHistory['pageInfo']['hasNextPage']
        no_pages = no_pages + 1
        progress_bar.progress(min(no_pages*50,commit_number)/commit_number 
                              , text = "Current commits status")
        time.sleep(1) 

    if (len(author_pairs)!=0):
        if (outputOption == "Heatmap"):
            st.title("Number of common commits between developers")

            values = [author_pairs.get(pair) for pair in author_pairs.keys()]

            df = pd.DataFrame({'Developer 1': [pair[0] for pair in author_pairs.keys()],
                            'Developer 2': [pair[1] for pair in author_pairs.keys()],
                            'Value': values})

            pivot_table = df.pivot_table(values='Value', index='Developer 1', columns='Developer 2', fill_value=0)

            fig, ax = plt.subplots()
            sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt='g', ax=ax)

            ax.set_title('Common commits')
            ax.set_xlabel('Developer 2')
            ax.set_ylabel('Developer 1')

            st.pyplot(fig)
        else:
            st.title("Top 5 most collaborative developer pairs")
            sorted_author_pairs = sorted(author_pairs.items(), key=lambda x:x[1])
            sorted_author_pairs.reverse()
            print(sorted_author_pairs)
            i=0
            for author_pair in sorted_author_pairs:
                if (i==5):
                    break
                i=i+1
                st.write("Author 1: " + str(author_pair[0][0]) + " and Author 2: "+ str(author_pair[0][1]) + " have contributed together with " + str(author_pair[1]) + " commits on common files")

    else :
        st.write("No developers have worked on the same files :(")
def main():
    st.title("Github analyser for finding most collaborative pairs of developers in a repository")
    st.text(f"""
    To use the application , add the github repository in the format used below. 
    For example, you can insert electron/electron on the period 1st January to 
    30th April 2024.
    Disclaimers :
        1. The application is evaluating 50 commits at a time such that it does not 
           get blocked by the GitHub API
        2. Do not forget to create a .env environment in the githubAnalyser folder 
           and add your git hub key correspondingly, otherwise the graphQL API is 
           not reachable
    """) 
    user_input = st.text_input("Enter a github repository in the form 'owner/repository_name':", "")
    today = datetime.datetime.now()
    jan_1 = datetime.date(2000, 1, 1)
    dec_31 = datetime.date(today.year, 12, 31)

    d = st.date_input(
        "Select interval to evaluate the repository on",
        (datetime.date(2024, 4, 16), datetime.date(2024, 4, 30)),
        jan_1,
        dec_31,
        format="MM.DD.YYYY",
    )
    option = st.selectbox(
    'How would you like the results to be shown?',
    ('Heatmap', 'Top 5 pairs'))
    if st.button("Submit"):
        analyze_command_graphQL_API(user_input,d[0],d[1],option)

if __name__ == "__main__":
    main()
