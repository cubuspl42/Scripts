import subprocess
from git import Repo

def get_changed_files(repo_path='.'):
    # Initialize the repository
    repo = Repo(repo_path)
    
    # Get the index (staging area) and working directory changes
    diff_index = repo.index.diff(None)
    
    # Collect paths of modified or added files (staged or not)
    changed_files = [item.a_path for item in diff_index if item.change_type in ('A', 'M', 'R')]
    # Include untracked files
    untracked_files = repo.untracked_files
    
    return changed_files + untracked_files

def filter_source_files(files):
    # Filter files to include only C/C++ source and header files
    source_extensions = ('.cpp', '.c', '.h', '.hpp')
    return [f for f in files if f.endswith(source_extensions)]

def run_clang_tidy(files):
    for file in files:
        print(f'Running clang-tidy on: {file}')
        subprocess.run(['clang-tidy', file], check=True)

def main():
    changed_files = get_changed_files()
    source_files = filter_source_files(changed_files)
    run_clang_tidy(source_files)

if __name__ == '__main__':
    main()
