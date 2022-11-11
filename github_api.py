import csv
import json
import re

import requests


class GitHubApi:
    """Class to interact with the GitHub API to pull information on repos, commit, etc
       GitHub API Documentation: https://docs.github.com/en/rest
       Create GitHub Personal Access Token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
    """

    def __init__(self, user_name, github_token_file_path):
        """Initialize the GitHubApi class

        Args:
            user_name (str): GitHub user name
            github_token_file_path (str): Path to file containing GitHub access token

        Returns:

        """

        self.user_name = user_name
        self.github_token_file_path = github_token_file_path
        self.github_token = self._get_github_token_from_file()
        self.base_url = "https://api.github.com"

    def _get_github_token_from_file(self):
        """Read in the GitHub token file to retrive the token value

        Args:

        Returns:
            github_token (str): String containing GitHub acess token

        """

        with open(self.github_token_file_path, "r") as token_file:
            github_token = token_file.read().strip()

        return github_token

    def get_repo_data(self):
        """Retrieve information on repos for a user

        Args:

        Returns:
            list: List containing information on user's repos

        """

        api_url = f"{self.base_url}/user/repos"
        response = requests.get(api_url, auth=(self.user_name, self.github_token))

        return response.json()

    def get_commit_data(self, repo_name):
        """Retrieve commit information on a specific user's repo

        Args:

        Returns:
            list: List containing commit information for a user's repo

        """

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.github_token}"
        }

        # Iterate through each page - break once there are no results
        output_data_list = []
        for i in range(1, 100):
            commit_url = f"{self.base_url}/repos/{self.user_name}/{repo_name}/commits?per_page=100&page={i}"
            response = requests.get(commit_url, headers=headers)
            if len(response.json()) > 0:
                output_data_list += response.json()
            else:
                break

        return output_data_list

    def parse_repo_dict(self, input_dict):
        """Parse the dictionary to retrieve data for the repository

        Args:
            input_dict (dict): Dictionary containing information on a repository

        Returns:
            output_list (list): List containing the key/value pairs that are useful

        """

        output_list = [
            input_dict.get("id"),
            input_dict.get("name"),
            input_dict.get("full_name"),
            input_dict.get("owner").get("id"),
            input_dict.get("owner").get("login"),
            input_dict.get("html_url"),
            input_dict.get("description"),
            input_dict.get("url"),
            input_dict.get("created_at"),
            input_dict.get("updated_at"),
            input_dict.get("pushed_at"),
            input_dict.get("ssh_url"),
            input_dict.get("stargazers_count"),
            input_dict.get("watchers_count"),
            input_dict.get("language"),
            input_dict.get("forks_count")
        ]
        return output_list

    def parse_commit_dict(self, input_dict):
        """Parse the dictionary to retrieve data for the commits of the repository

        Args:
            input_dict (dict): Dictionary containing information on the commits of the repository

        Returns:
            output_list (list): List containing the key/value pairs that are useful

        """

        pattern = rf"https://api.github.com/repos/{self.user_name}/(.*)/commits.*"
        repo_name = re.match(pattern=pattern, string=input_dict.get("url")).group(1)

        try:
            parent_sha = input_dict.get("parents")[0].get("sha")
            parent_url = input_dict.get("parents")[0].get("url")
            parent_html_url = input_dict.get("parents")[0].get("html_url")

        except IndexError:
            parent_sha = None
            parent_url = None
            parent_html_url = None

        output_list = [
            repo_name,
            input_dict.get("sha"),
            input_dict.get("commit").get("author").get("name"),
            input_dict.get("commit").get("author").get("email"),
            input_dict.get("commit").get("author").get("date"),
            input_dict.get("commit").get("author").get("name"),
            input_dict.get("commit").get("author").get("email"),
            input_dict.get("commit").get("author").get("date"),
            input_dict.get("commit").get("message"),
            input_dict.get("commit").get("tree").get("sha"),
            input_dict.get("commit").get("tree").get("url"),
            input_dict.get("commit").get("comment_count"),
            input_dict.get("url"),
            input_dict.get("html_url"),
            input_dict.get("comments_url"),
            input_dict.get("author"),
            input_dict.get("committer"),
            # input_dict.get("parents")[0].get("sha"),
            parent_sha,
            # input_dict.get("parents")[0].get("url"),
            parent_url,
            # input_dict.get("parents")[0].get("html_url"),
            parent_html_url
        ]
        return output_list

    def write_data_to_csv(self, input_list, outfile_path, headers=None):
        """Write data to csv file

        Args:
            input_list (list): List containing data
            outfile_path (str): Path to outfile
            headers(list, optional): List containing headers

        Returns:

        """

        with open(outfile_path, "w", newline="") as output_file:
            writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
            if headers:
                writer.writerow(headers)
            writer.writerows(input_list)

    def get_repo_names(self, input_list):
        """Iterate through response list and get name of each repo

        Args:
            input_list (list): List containing each dictionary response

        Returns:
            repo_list (list): List containing the names of each repo

        """

        repo_list = [l.get("name") for l in input_list]
        return repo_list
