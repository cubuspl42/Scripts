import argparse
import itertools

import git

# Code style:
# Prefer named arguments

parser = argparse.ArgumentParser(description="Git rebase-onto with a heuristic")
parser.add_argument("target", help="The commit we want to rebase onto")
parser.add_argument(
    "--force",
    action="store_true",
    help="Force the rebase even if there is a diff between the target and the ancestor",
)


def find_ancestor_with_message(repo, ref, message, max_depth=512):
    """Find the ancestor of ref with the same commit message, up to max_depth."""
    for ancestor in itertools.islice(repo.iter_commits(ref), max_depth):
        if ancestor.message == message:
            return ancestor
    return None


def is_ancestor(repo, ancestor_commit, descendant_commit):
    """Check if ancestor_commit is an ancestor of descendant_commit."""
    for commit in repo.iter_commits(descendant_commit):
        if commit == ancestor_commit:
            return True
    return False


def has_diff(commit, reference_commit):
    """Check if there are differences between two commits."""
    diff = commit.diff(reference_commit, create_patch=True)
    return bool(diff)  # Returns True if there are differences, False otherwise


def main():
    args = parser.parse_args()

    target = args.target
    force = args.force

    repo = git.Repo('.')  # Assumes script is run from the repo root

    target_commit = repo.commit(target)

    if not target_commit:
        print(f"{target} not found in the repository")
        print("Exiting")
        return

    # Resolve HEAD programmatically
    head_commit = repo.head.commit

    merge_base_commits = repo.merge_base(head_commit, target_commit)

    if len(merge_base_commits) != 1:
        print("Multiple merge base commits found. Cannot proceed with rebase")
        print("Exiting")
        return

    merge_base_commit = merge_base_commits[0]

    target_diverged_commits = repo.iter_commits(f'{target_commit.hexsha}...{merge_base_commit.hexsha}')
    head_diverged_commits = repo.iter_commits(f'{head_commit.hexsha}...{merge_base_commit.hexsha}')

    target_diverged_commit_by_message = {
        commit.message: commit for commit in target_diverged_commits
    }

    # Find the first commit in the head that has a message matching one of the target's diverged commits
    rebase_base_commit = next(
        (commit for commit in head_diverged_commits if commit.message in target_diverged_commit_by_message),
        None,
    )

    if not rebase_base_commit:
        print("No similar commit found in HEAD that matches one of the target's diverged commits")
        print("Exiting")
        return

    print("Found rebase base commit:", rebase_base_commit.hexsha)
    print(rebase_base_commit.message.strip())

    target_similar_commit = target_diverged_commit_by_message.get(rebase_base_commit.message)

    if not force and has_diff(commit=target_similar_commit, reference_commit=rebase_base_commit):
        print(f"There are differences between the commit {rebase_base_commit.hexsha} and the target's similar commit {target_similar_commit.hexsha}")
        print("Exiting")
        return

    try:
        repo.git.rebase(rebase_base_commit.hexsha, onto=target_commit.hexsha)

        print(f"Rebased onto {target} (base: {rebase_base_commit.hexsha})")
    except git.exc.GitCommandError as e:
        print(f"Rebase failed: {e}")


if __name__ == "__main__":
    main()
