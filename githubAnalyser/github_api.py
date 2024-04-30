import requests
import os
from dotenv import load_dotenv
load_dotenv

def fetch_repository_data(repository):
    url = f"https://api.github.com/repos/{repository}/commits"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(url, headers=headers)
    return response.json()