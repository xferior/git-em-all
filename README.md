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

```
$ python3 script.py <username> [--all | repo1,repo2,repo3] <path_to_directory>
```

### Clone All Repositories
To clone all repositories of a user into a specific directory:
```
$ python3 clone-pull-repo.py xferior --all /opt/git
```
### Selectively Clone or Update Repositories

To list all repositories and then choose specific ones to clone or update:

```
$ python3 clone-pull-repo.py xferior
Available repositories to clone or update:
1: acetone
2: BatchTools
3: git-em-all
4: gnosissh-deb
5: linux-kexec
6: lvm-snapshot
7: ssh-browser-proxy
Enter the number of repositories to clone or update (comma-separated): 5,7
Enter the directory to clone or update the repositories into: /opt/git
----------------------------------------
Cloning linux-kexec...
Cloning into 'linux-kexec'...
remote: Enumerating objects: 40, done.
remote: Counting objects: 100% (40/40), done.
remote: Compressing objects: 100% (40/40), done.
remote: Total 40 (delta 19), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (40/40), 12.74 KiB | 2.12 MiB/s, done.
Resolving deltas: 100% (19/19), done.
Cloned linux-kexec into /opt/git
----------------------------------------
Cloning ssh-browser-proxy...
Cloning into 'ssh-browser-proxy'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 12 (delta 1), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (12/12), 7.75 KiB | 7.75 MiB/s, done.
Resolving deltas: 100% (1/1), done.
Cloned ssh-browser-proxy into /opt/git
```
Attempt Update (pull) (with pending updates):
```
$ python3 clone-pull-repo3.py xferior git-em-all /opt/git
----------------------------------------
Repository git-em-all already exists. Checking for updates...
git-em-all has been updated
```
Attempt Update (pull) (no pending updates):
```
$ python3 clone-pull-repo3.py xferior git-em-all /opt/git
----------------------------------------
Repository git-em-all already exists. Checking for updates...
git-em-all is already up to date
```
