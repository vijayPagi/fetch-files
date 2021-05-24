import urllib.request
import sys
import requests
import json
from collections import defaultdict
import datetime
from config import *
import re

class FetchData:

    # Default constructor with declaration of global static variables
    def __init__(self):
        self.repositorylistURL = sys.argv[1]
        self.fromSearchDockerFile = fromSearchDockerFile
        self.genericGitHubUrl = genericGitHubUrl
        self.githubRegEx = githubRegEx
        self.commitRegEx = commitRegEx

    # Transforms the passing parameter git Url to return a repository path
    def repoValue(self, url):
        return url.replace(".git", "").replace("https://github.com/", "")

    # Validates the commitId with the repository
    def validateSHA(self, repo, commitId):
        response = urllib.request.urlopen(str(repo).replace(".git","/commit/")+str(commitId))
        if response:
            return True
        else:
            return False

    # The function intends to utilize the repository list text path url and executes sequence of logical operations and prints out a Json response of data,
    # repository, docker file path and images used
    def readText(self):
        errordict = defaultdict()
        try:
            repositoryListContent = urllib.request.urlopen(self.repositorylistURL)
            imagelist = []
            resultDict = defaultdict(self.nested_dict)
            # looping input list of repositories and its commits
            for repoCommit in repositoryListContent:
                commitResponse= self.validateSHA(str(repoCommit.decode("utf-8")).split(" ", 1)[0],str(repoCommit.decode("utf-8")).split(" ", 1)[1])
                # Validating input repository url's
                if re.match(self.githubRegEx, str(repoCommit.decode("utf-8")).split(" ", 1)[0]) and re.match(self.commitRegEx, str(repoCommit.decode("utf-8")).split(" ", 1)[1]) and commitResponse:
                    decodedrepoCommit= str(repoCommit.decode("utf-8")).split(" ", 1)
                    gitRepoUrl=decodedrepoCommit[0].replace("/n", "")
                    commitId= decodedrepoCommit[1].replace("/n", "")
                    repoPath = self.repoValue(gitRepoUrl)
                    dockerFilesWithFROM = requests.get(self.fromSearchDockerFile + repoPath)
                    dockerFilesWithFROM_json = json.loads(dockerFilesWithFROM.content)
                    finalUrl = (gitRepoUrl + ":" + commitId).replace("\n", "")
                    # Looping and fetching all docker files
                    for value in dockerFilesWithFROM_json['items']:
                        contentStreamDockerFile = urllib.request.urlopen(rawGitContentUrl + repoPath + "/master/" + str(value['path']))
                        for line in contentStreamDockerFile:
                            decodedLine = line.decode("utf-8")
                            if "FROM" in decodedLine:
                                imageName = str(decodedLine).split(" ")[1].replace("\n", "")
                                imagelist.append(imageName)
                        resultDict['data'][finalUrl][value['path']] = imagelist
                        imagelist = []
                else:
                    continue
            # Converting final result to json
            resultJson = json.dumps(resultDict)
            print(resultJson)
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


if __name__ == '__main__':
    fData = FetchData()
    fData.readText()