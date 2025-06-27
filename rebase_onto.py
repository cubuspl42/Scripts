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

    target_string = args.configtarget_file_path
    force = args.force

    repo = git.Repo('.')  # Assumes script is run from the repo root

    target_commit = repo.commit(target_string)

    if not target_commit:
        print(f"{target_string} not found in the repository.")
        return

    # Resolve HEAD programmatically
    head_commit = repo.head.commit

    # Check if the original parent is an ancestor of HEAD
    if not is_ancestor(repo=repo, ancestor_commit=target_commit, descendant_commit=head_commit):
        target_commit_equivalent = find_ancestor_with_message(
            repo=repo,
            ref=head_commit,
            message=target_commit.message,
        )

        if target_commit_equivalent:
            print(f"Found ancestor with matching message: {target_commit_equivalent.hexsha}")

            if force or not has_diff(commit=target_commit, reference_commit=target_commit_equivalent):
                # TODO: Rebase

                print(f"Rebased {target_commit_equivalent.hexsha} onto {target_string}")
            else:
                print(
                    f"There are differences between the commit {target_string} and the ancestor {target_commit_equivalent.hexsha}. No update made.")
        else:
            print("No ancestor with the same commit message found within the specified depth.")

    else:
        print(f"The parent {target_string} is an ancestor of HEAD. No rebase required.")


if __name__ == "__main__":
    main()
