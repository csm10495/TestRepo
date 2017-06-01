import subprocess
import os

def hasChanges():
    '''
    Brief:
        Returns True if changes are staged locally
    '''
    output = subprocess.check_output('git status -s -uno', shell=True)
    return bool(output.strip()) # True if output from this command
    
def getCurrentBranch():
    '''
    Brief:
        Returns the name of the current branch
    '''
    output = subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True)
    return output.strip().decode()
    
def getListOfCommits(branch='master'):
    '''
    Brief:
        Returns list of commits on given branch. 0th is most recent.
    '''
    outputLines = subprocess.check_output('git log --full-history --pretty=oneline %s' % branch, shell=True).decode().splitlines()
    commits = []
    for i in outputLines:
        if i.strip() != '':
            commits.append(i.split(' ')[0])
    
    return commits
    
def getCurrentCommitId(branch='master'):
    '''
    Brief:
        Gets the hash of the current commit and appenda a "+" if there are staged changes
    '''
    commit = getListOfCommits(branch)[0] # first is newest
    if hasChanges():
        return commit + "+"
    return commit
    
def getHgStyleIdNum(branch='master'):
    '''
    Brief:
        Gets an hg-style id number for the current commit
    '''
    commits = getListOfCommits(branch)
    start = str(len(commits))
    if hasChanges():
        return start + "+"
    return start
    
def getRepoNameFromCurrentFolder():
    '''
    Brief:
        Gets the name of the repo from the current folder. Assumes the folder name was not changed
    '''
    return os.path.basename(os.getcwd())
    
def getRepoRevisionSetInfo(repoPath='.'):
    '''
    Brief:
        Returns a string of information about the current repository commits/changesets
    '''
    oldCwd = os.getcwd()
    os.chdir(repoPath)
    try:
        branch = getCurrentBranch()
        hgIdNum = getHgStyleIdNum(branch)
        commitId = getCurrentCommitId(branch)
        repoName = getRepoNameFromCurrentFolder()
        return "%s %s (hg:%s) - %s" % (repoName, commitId, hgIdNum, branch)
    finally:
        os.chdir(oldCwd)
    