import requests
import sys
import subprocess
import os

# Attempt to download a list of public repos for a GitHub user
def list_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repositories for user {username}. Status code: {response.status_code}")
        return None

# Clone or pull updates for selected repositories into a specified directory
def clone_or_pull_repos(repos, repo_numbers, clone_directory):
    for number in repo_numbers:
        index = number - 1  # Convert number to list index
        if index < 0 or index >= len(repos):  # Check for valid index
            print(f"Invalid repository number: {number}")
            continue
        repo_url = repos[index]['clone_url']
        repo_name = repos[index]['name']
        repo_path = os.path.join(clone_directory, repo_name)

        # Separator
        print("-" * 40)  

        # Determine whether to clone a new repo or pull updates for an existing one
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            update_choice = input(f"Repository {repo_name} already exists. Do you want to check for updates? (y/n): ").strip().lower()
            # Handle updating existing repository
            if update_choice == 'y':
                try:
                    print(f"Updating {repo_name}...")
                    result = subprocess.run(["git", "pull"], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    if "Already up to date." in result.stdout:
                        print(f"{repo_name} is already up to date")
                    else:
                        print(f"{repo_name} has been updated")
                except subprocess.CalledProcessError:
                    print(f"Updating {repo_name} failed. Please check the repository status.")
            elif update_choice == 'n':
                print(f"Skipped updating {repo_name}")
            else:
                print("Invalid input. Exiting.")
                sys.exit(1)
        else:
            # Clone new repository
            try:
                print(f"Cloning {repo_name}...")
                subprocess.run(["git", "clone", repo_url], cwd=clone_directory, check=True)
                print(f"Cloned {repo_name} into {clone_directory}")
            except subprocess.CalledProcessError:
                print(f"Cloning {repo_name} failed. Please check if the repository exists and you have access to it.")

if __name__ == "__main__":
    # Validate and process command-line arguments
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        username = sys.argv[1]
    else:
        print("Error: No username provided. Exiting.")
        sys.exit(1)
    
    repos = list_github_repos(username)
    
    # Handle cloning all repositories with --all argument
    if len(sys.argv) > 3 and sys.argv[2] == "--all":
        clone_directory = sys.argv[3].strip()
        if not clone_directory:
            print("Error: No clone directory provided. Exiting.")
            sys.exit(1)
        if not os.path.exists(clone_directory):
            os.makedirs(clone_directory, exist_ok=True)
        if repos:
            repo_numbers = range(1, len(repos) + 1)  # For all repositories
            clone_or_pull_repos(repos, repo_numbers, clone_directory)
    elif repos:
        # List repositories and prompt user for selections
        print("Available repositories to clone or update:")
        for i, repo in enumerate(repos, start=1):
            print(f"{i}: {repo['name']}")
        
        selected_numbers = input("Enter number of repositories to clone or update (comma separated): ").strip()
        if not selected_numbers:
            print("Error: No repository numbers provided. Exiting.")
            sys.exit(1)
        selected_numbers = [int(number.strip()) for number in selected_numbers.split(",") if number.strip().isdigit()]
        
        clone_directory = input("Enter the directory to clone or update the repositories into: ").strip()
        if not clone_directory:
            print("Error: No clone directory provided. Exiting.")
            sys.exit(1)
        if not os.path.exists(clone_directory):
            os.makedirs(clone_directory, exist_ok=True)
        
        clone_or_pull_repos(repos, selected_numbers, clone_directory)
    else:
        print("Usage: python script.py <username> [--all <path>]")
