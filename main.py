import json
import os

import github

from src.add_reviewers import add_reviewers
from src.block_merge import block_merge_no_verify
from src.block_offensive_lanague import block_offensive_language
from src.labels_by_user_input import labels_by_user_input, remove_verified_label
from src.size_label_prs import size_label_prs


if __name__ == "__main__":
    token = os.environ["INPUT_TOKEN"]
    action = os.environ["INPUT_ACTION"]
    github = github.Github(token)
    repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
    commit = repo.get_commit(os.environ["GITHUB_SHA"])
    with open(os.environ["GITHUB_EVENT_PATH"], "r") as fd:
        data = json.load(fd)

    try:
        pull = repo.get_pull(data["number"])
    except KeyError:
        pull = repo.get_pull(data["issue"]["number"])

    if action == "remove_verified_label":
        remove_verified_label(pull=pull)
        block_merge_no_verify(pull=pull)

    if action == "labels_by_user_input":
        labels_by_user_input(data=data, pull=pull)

    if action == "add_reviewers":
        reviewers = os.environ["INPUT_REVIEWERS"]
        add_reviewers(data=data, pull=pull, reviewers=reviewers)

    if action == "size_label_prs":
        size_label_prs(data=data, pull=pull)

    if action == "block_offensive_language":
        block_offensive_language(pull=pull)
