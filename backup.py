#!/usr/bin/env python3.9
import os
import git
import requests
import yaml
import logging

# setup env vars
TARGET_DIR = os.getenv("TARGET_DIR", os.path.join(os.getcwd(), "./data"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR
)
logger = logging.getLogger("backup")
logger.setLevel(LOG_LEVEL)

# setup secrets
SECRETS_FILE = "secrets.yaml"
with open(SECRETS_FILE) as f:
    secrets_data = yaml.load(f, Loader=yaml.FullLoader)
access_token = secrets_data.get('PERSONAL_ACCESS_TOKEN')
username = secrets_data.get('USERNAME')

# github api endpoint
endpoint = "https://api.github.com/user/repos"

# setup header with token for requests + gitpython
headers = {"Authorization": f"Token {access_token}"}
os.environ['GIT_PYTHON_GITHUB_ACCESS_TOKEN'] = access_token

# fetch all repos of the user
repos = []
page = 1
while True:
    response = requests.get(endpoint, headers=headers, params={"page": page})
    response_repos = response.json()
    if not response_repos:
        break
    repos.extend(response_repos)
    page += 1

# extract json data from response
logger.info("Found %i repos to mirror" % len(repos))

# mirror each repo
for repo in repos:
    logger.info(repo["full_name"])
    repo_path = os.path.join(TARGET_DIR, repo['name'])
    logger.info("  %s", repo_path)
    # clone if non existing
    if not os.path.exists(repo_path):
        # clone repo
        repo_name = repo['full_name']
        logger.info("  Cloning %s", repo_name)
        git.Repo.clone_from(f'https://{username}:{access_token}@github.com/{repo_name}.git', repo_path)
    # pull if existing
    else:
        g = git.Git(repo_path)
        try:
            logger.info("  Pulling..")
            g.pull()
            logger.info("  Pulling done")
        except git.exc.GitCommandError as e:
            if "no such ref was fetched" in str(e):
                logger.info("  empty repo")
            else:
                logger.error("  An unexpected Git error occurred:", e)
