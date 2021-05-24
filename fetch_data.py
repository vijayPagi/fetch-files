import urllib.request
import os
import requests
import json
from collections import defaultdict
from config import *
import re


class FetchData:

    # Default constructor with declaration of global static variables
    def __init__(self):
        self.repositorylist_url = os.environ['REPOSITORY_LIST_URL']
        self.from_search_dockerfile = from_search_dockerfile
        self.github_regex = github_regex
        self.commit_regex = commit_regex

    # Transforms the passing parameter git Url to return a repository path
    def repo_value(self, url):
        return url.replace(".git", "").replace("https://github.com/", "")

    # Validates the commitId with the repository
    def validate_sha(self, repo, commit_id):
        response = urllib.request.urlopen(str(repo).replace(".git", "/commit/") + str(commit_id))
        if response:
            return True
        else:
            return False

    # The function intends to utilize the repository list text path url and executes sequence of logical operations and prints out a Json response of data,
    # repository, docker file path and images used
    def readText(self):
        errordict = defaultdict()
        try:
            repository_list_content = urllib.request.urlopen(self.repositorylist_url)
            imagelist = []
            result_dict = defaultdict(self.nested_dict)
            # looping input list of repositories and its commits
            for repo_commit in repository_list_content:
                commit_response = self.validate_sha(str(repo_commit.decode("utf-8")).split(" ", 1)[0],
                                                    str(repo_commit.decode("utf-8")).split(" ", 1)[1])
                # Validating input repository url's
                if re.match(self.github_regex, str(repo_commit.decode("utf-8")).split(" ", 1)[0]) and re.match(
                        self.commit_regex, str(repo_commit.decode("utf-8")).split(" ", 1)[1]) and commit_response:
                    decodedrepo_commit = str(repo_commit.decode("utf-8")).split(" ", 1)
                    git_repo_url = decodedrepo_commit[0].replace("/n", "")
                    commit_id = decodedrepo_commit[1].replace("/n", "")
                    repo_path = self.repo_value(git_repo_url)
                    docker_files_with_from = requests.get(self.from_search_dockerfile + repo_path)
                    docker_files_with_from_json = json.loads(docker_files_with_from.content)
                    final_url = (git_repo_url + ":" + commit_id).replace("\n", "")
                    # Looping and fetching all docker files
                    for value in docker_files_with_from_json['items']:
                        content_stream_docker_file = urllib.request.urlopen(
                            raw_git_content_Url + repo_path + "/master/" + str(value['path']))
                        for line in content_stream_docker_file:
                            decoded_line = line.decode("utf-8")
                            if "FROM" in decoded_line:
                                image_name = str(decoded_line).split(" ")[1].replace("\n", "")
                                imagelist.append(image_name)
                        result_dict['data'][final_url][value['path']] = imagelist
                        imagelist = []
                else:
                    continue
            # Converting final result to json
            result_json = json.dumps(result_dict)
            print(result_json)
        except Exception as ex:
            errordict['Error'] = str(ex)
            # Converting error result to json
            error_json = json.dumps(errordict)
            print(error_json)

    # Creates a dictionary property with the library: defaultdict
    def dict(self):
        return defaultdict(str)

    # Per the need of creating a nested dictionary, this property used the custom dict property to cascade
    def nested_dict(self):
        return defaultdict(self.dict)
