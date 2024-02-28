# Git-Em-All

## Overview
This script enumerates all public repos for a GitHub user. It can clone all repos at once or select specific ones for cloning into a directory. If a repo is already cloned, the script can pull updates to ensure the local copies of repos are current.

## Features
- Enumerate all public repositories of a given GitHub user.
- Clone selected or all repositories to a local directory.
- Pull updates for already cloned repositories to keep them up-to-date.

## Prerequisites
- python 3.x
- git 

## Usage

### Clone All Repositories
To clone all repositories of a user into a specific directory:
```
python script.py <username> --all <path_to_clone_directory>
```
### Selectively Clone or Update Repositories
To list all repositories and then choose specific ones to clone or update:

python script.py <username>

Follow the prompts to select repositories and specify the clone directory

*TODO*

