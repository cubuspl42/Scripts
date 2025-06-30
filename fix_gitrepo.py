import argparse
import configparser
import git
import gitdb
import itertools

# Code style:
# Prefer named arguments

parser = argparse.ArgumentParser(description="Update the .gitrepo parent pointer")
parser.add_argument("config_file_path", help="Path to the .gitrepo file")


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

    config_path = args.config_file_path

    # Create a ConfigParser instance
    config = configparser.ConfigParser()

    with open(config_path, 'r') as configfile:
        config.read_file(configfile)

    # Accessing values from the 'subrepo' section
    parent_sha = config.get('subrepo', 'parent')

    # Use GitPython to get the commit message of the parent commit
    repo = git.Repo('.')  # Assumes script is run from the repo root

    try:
        parent_commit = repo.commit(parent_sha)
    except gitdb.exc.BadName:
        print(f"Invalid commit hash: {parent_sha}. Please check the .gitrepo file.")
        return
    except ValueError as e:
        print(f"Error resolving SHA: {e}. The commit might be missing or corrupted.")
        return

    if not parent_commit:
        print(f"Commit {parent_sha} not found in the repository.")
        return

    # Resolve HEAD programmatically
    head_commit = repo.head.commit

    # Check if the original parent is an ancestor of HEAD
    if not is_ancestor(repo, parent_commit, head_commit):
        parent_commit_sibling = find_ancestor_with_message(
            repo=repo,
            ref=head_commit,
            message=parent_commit.message,
        )

        if parent_commit_sibling:
            print(f"Found ancestor with matching message and differences: {parent_commit_sibling.hexsha}")

            if not has_diff(commit=parent_commit, reference_commit=parent_commit_sibling):
                # Update the parent in the config file
                config.set('subrepo', 'parent', parent_commit_sibling.hexsha)

                with open(config_path, 'w') as configfile:
                    config.write(configfile)

                print(f"Updated .gitrepo parent to {parent_commit_sibling.hexsha} in {config_path}")
            else:
                print(f"There are differences between the commit {parent_sha} and the ancestor {parent_commit_sibling.hexsha}. No update made.")
        else:
            print("No ancestor with the same commit message found within the specified depth.")

    else:
        print(f"The parent {parent_sha} is an ancestor of HEAD. No fixup required.")


if __name__ == "__main__":
    main()
