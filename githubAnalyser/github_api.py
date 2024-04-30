import requests
import os
from dotenv import load_dotenv
import json 
load_dotenv()

from urllib.parse import urlparse, parse_qs

auth = {"Authorization": f"bearer {os.getenv('GITHUB_TOKEN')}"}

def get_top_five_contributors(repository):
    url = f"https://api.github.com/repos/{repository}/contributors?per_page=5"
    headers = auth
    response = requests.get(url,headers = headers)
    return response.json()

def get_repository_tree(repository,treeSHA):
    url = f"https://api.github.com/repos/{repository}/git/trees/{treeSHA}?recursive=true"
    headers = auth
    response = requests.get(url,headers = headers)
    return response.json()

def get_repository_file_paths(repository):
    url = f"https://api.github.com/repos/{repository}/contents"
    headers = auth
    response = requests.get(url,headers = headers)
    return response.json()

def fetch_all_repository_data(repository,page_number):
    url = f"https://api.github.com/repos/{repository}/commits?per_page=50&page={str(page_number)}"
    headers = auth
    response = requests.get(url, headers=headers)
    print(response.links)
    last_page_number = 1
    if (response.links):
        parsed_url_last = urlparse(response.links['last']['url'])
        last_page_number  = parse_qs(parsed_url_last.query)['page'][0]
    return {"response": response.json(), "last_page" : last_page_number}

def get_specific_commit_info(repository,commitRef):
    url = f"https://api.github.com/repos/{repository}/commits/{commitRef}"
    headers = auth
    response = requests.get(url,headers = headers)
    return response.json()
def commits_in_a_given_period(repository,page_number,start,end):
    url = f"https://api.github.com/repos/{repository}/commits?per_page=100&page={str(page_number)}&since={str(start)}&until={str(end)}"
    headers = auth
    response = requests.get(url,headers = headers)
    last_page_number = 1
    if (response.links):
        parsed_url_last = urlparse(response.links['last']['url'])
        last_page_number  = parse_qs(parsed_url_last.query)['page'][0]
    return {"response": response.json(), "last_page" : last_page_number}
def get_author_file_impact(repository,page_number,filePath,start,end,author):
    url = f"https://api.github.com/repos/{repository}/commits?per_page=1&page={str(page_number)}&path={str(filePath)}&since={str(start)}&until={str(end)}&author={str(author)}"
    headers = auth
    response = requests.get(url, headers=headers)
    last_page_number = 1
    if (response.links):
        parsed_url_last = urlparse(response.links['last']['url'])
        last_page_number  = parse_qs(parsed_url_last.query)['page'][0]
    return int(last_page_number)

def get_number_of_commits_with_graphQLAPI(repository,start,end):
    query = """
    {
  repository(owner: "owner_username", name: "repository_name") {
    defaultBranchRef {
      target {
        ... on Commit {
          history(since: "start", until: "end") {
            totalCount
          }
        }
      }
    }
  }
}

    """
    query = query.replace("owner_username",repository.split('/')[0])
    query = query.replace("repository_name", repository.split('/')[1])
    query = query.replace("start",str(start))
    query = query.replace("end", str(end))
    print(query)
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=auth)

    return response.json()["data"]["repository"]["defaultBranchRef"]["target"]["history"]["totalCount"]

def get_commits_with_graphQLAPI(repository,start,end):
    query = """
    {
  repository(owner: "owner_username", name: "repository_name") {
    defaultBranchRef {
      target {
        ... on Commit {
          history(since: "startTT", until: "endTT", first: 50) {
            pageInfo {
            endCursor
            hasNextPage
            }
            nodes{
                associatedPullRequests(first:25){
                    nodes{
                        files(first:25){
                            nodes{
                                path
                            }
                        }
                        author{
                            login
                        }
                    }
                }
            }
          }
        }
      }
    }
  }
}

    """
    
    query = query.replace("owner_username",repository.split('/')[0])
    query = query.replace("repository_name", repository.split('/')[1])
    query = query.replace("startTT",str(start))
    query = query.replace("endTT", str(end))
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=auth)

    return response.json()


def get_commits_with_graphQLAPI_with_cursor(repository,after_cursor,start,end):
    query = """
    {
  repository(owner: "owner_username", name: "repository_name") {
    defaultBranchRef {
      target {
        ... on Commit {
          history(since: "startTT", until: "endTT", first: 50 , after:"after_cursor") {
            pageInfo {
            endCursor
            hasNextPage
            }
            nodes{
                associatedPullRequests(first:25){
                    nodes{
                        files(first:25){
                            nodes{
                                path
                            }
                        }
                        author{
                            login
                        }
                    }
                }
            }
          }
        }
      }
    }
  }
}

    """
    
    query = query.replace("owner_username",repository.split('/')[0])
    query = query.replace("repository_name", repository.split('/')[1])
    query = query.replace("after_cursor", after_cursor)
    query = query.replace("startTT",str(start))
    query = query.replace("endTT", str(end))

    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=auth)
    return response.json()
