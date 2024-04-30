import requests
import os
from dotenv import load_dotenv
import json 
load_dotenv()

from urllib.parse import urlparse, parse_qs

auth = {"Authorization": f"bearer {os.getenv('GITHUB_TOKEN')}"}

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
