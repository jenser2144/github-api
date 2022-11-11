from os import environ

from github_api import GitHubApi

github_token_filepath = f"{environ.get('HOME')}/code/github-api/github_personal_token.txt"
user_name = "jenser2144"

gha = GitHubApi(
    user_name=user_name,
    github_token_file_path=github_token_filepath
)

# Get repo data
repo_data = gha.get_repo_data()

# Parse repo_data into a list
headers = [
    "id",
    "name",
    "full_name",
    "owner_id",
    "owner_login",
    "html_url",
    "description",
    "url",
    "created_at",
    "updated_at",
    "pushed_at",
    "ssh_url",
    "stargazers_count",
    "watchers_count",
    "language",
    "forks_count"
]
repo_data_list = [headers]
for repo in repo_data:
    repo_data_list.append(gha.parse_repo_dict(input_dict=repo))

# Write repo data to csv file
output_filepath = f"{environ.get('HOME')}/code/github-api/repo_data.csv"
gha.write_data_to_csv(
    input_list=repo_data_list,
    outfile_path=output_filepath
)

# Get list of repo names
repo_list = gha.get_repo_names(input_list=repo_data)

# Get repo commits for all repos
# repo_commits = gha.get_commit_data(
#     repo_name="airflow-etl"
# )
repo_commits = []
for repo in repo_list:
    repo_commits_temp = gha.get_commit_data(
        repo_name=repo
    )    
    repo_commits += repo_commits_temp

# Parse commit dict
commit_headers = [
    "repo_name",
    "sha",
    "commit_author",
    "commit_email",
    "commit_date",
    "committer_author",
    "committer_author",
    "committer_date",
    "commit_mesage",
    "commit_tree_sha",
    "commit_tree_url",
    "commit_comment_count",
    "url",
    "html_url",
    "comments_url",
    "author",
    "committer",
    "parent_sha",
    "parent_url",
    "parent_html_url"
]
commit_data_list = [commit_headers]
for commit in repo_commits:
    commit_data_list.append(gha.parse_commit_dict(input_dict=commit))

# Write commit data to csv file
commit_output_filepath = f"{environ.get('HOME')}/code/github-api/commit_data.csv"
gha.write_data_to_csv(
    input_list=commit_data_list,
    outfile_path=commit_output_filepath
)
