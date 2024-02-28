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
def clone_or_pull_repos(repos, selection, clone_directory):
    if selection == "--all":
        selected_repos = repos
    else:
        # Splitting the selection string into individual repo names
        repo_names = selection.split(",")
        # Filtering the list of repos to only those specified by the user
        selected_repos = [repo for repo in repos if repo['name'] in repo_names]

    for repo in selected_repos:
        repo_url = repo['clone_url']
        repo_name = repo['name']
        repo_path = os.path.join(clone_directory, repo_name)

        # Separator
        print("-" * 40)

        # Check if repo already exists
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            print(f"Repository {repo_name} already exists. Checking for updates...")
            # Attempt to pull updates from the remote
            try:
                result = subprocess.run(["git", "pull"], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                if "Already up to date." in result.stdout:
                    print(f"{repo_name} is already up to date")
                else:
                    print(f"{repo_name} has been updated")
            except subprocess.CalledProcessError:
                print(f"Updating {repo_name} failed. Please check the repository status.")
        else:
            # If the repo does not exist locally, clone it
            try:
                print(f"Cloning {repo_name}...")
                subprocess.run(["git", "clone", repo_url], cwd=clone_directory, check=True)
                print(f"Cloned {repo_name} into {clone_directory}")
            except subprocess.CalledProcessError:
                print(f"Cloning {repo_name} failed. Please check if the repository exists and you have access to it.")

# Select specific repositories to clone or update
def interactive_mode(repos):
    print("Available repositories to clone or update:")
    for i, repo in enumerate(repos, start=1):
        print(f"{i}: {repo['name']}")

    selected_numbers = input("Enter the number of repositories to clone or update (comma-separated): ").strip()
    if not selected_numbers:
        print("Error: No repository numbers provided. Exiting.")
        sys.exit(1)

    # Convert input number(s) to list of numbers, adjusting for zero-based indexing
    selected_numbers = [int(number.strip()) - 1 for number in selected_numbers.split(",") if number.strip().isdigit()]
    
    clone_directory = input("Enter the directory to clone or update the repositories into: ").strip()
    if not clone_directory:
        print("Error: No clone directory provided. Exiting.")
        sys.exit(1)
    
    if not os.path.exists(clone_directory):
        os.makedirs(clone_directory, exist_ok=True)

    # Filter the selected repositories by number(s) and clone or pull them
    repo_names = [repos[num]['name'] for num in selected_numbers if 0 <= num < len(repos)]
    clone_or_pull_repos(repos, ",".join(repo_names), clone_directory)

if __name__ == "__main__":
    # Validate and process command-line arguments
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        username = sys.argv[1]
    else:
        print("Error: No username provided. Exiting.")
        sys.exit(1)
    
    repos = list_github_repos(username)
    if not repos:
        print("No repositories found or error fetching repositories.")
        sys.exit(1)
    
    # Decide mode based on the number of command-line arguments
    if len(sys.argv) == 2:
        # Enter interactive mode if only the username is provided
        interactive_mode(repos)
    elif len(sys.argv) == 4:
        # Clone or update specified repositories or all
        selection = sys.argv[2]
        clone_directory = sys.argv[3].strip()
        
        if not os.path.exists(clone_directory):
            os.makedirs(clone_directory, exist_ok=True)
        
        clone_or_pull_repos(repos, selection, clone_directory)
    else:
        print("Invalid usage.")
        sys.exit(1)
