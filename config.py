raw_git_content_Url = "https://raw.githubusercontent.com/"
from_search_dockerfile = "https://api.github.com/search/code?q=FROM+filename:Dockerfile+repo:"
github_regex = "(http(s)?)(:(//)?)(github.com)(/)([a-zA-Z0-9-/_]+)(\.git)$"
commit_regex = "^[0-9a-z]{5,40}$"