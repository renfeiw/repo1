import git
import re
import os
import argparse
from pathlib import Path
import shutil
import random

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="regex file name to modify")
    ap.add_argument("-s", "--find", required=True, help="regex string to search in file")
    ap.add_argument("-r", "--replace", required=True, help="regex string to replace found")
    ap.add_argument("-m", "--message", required=True, help="commit message")
    ap.add_argument("-o", "--originURL", required=True, help="git origin repo")
    ap.add_argument("-u", "--user", required=True, help="git user id")
    ap.add_argument("-e", "--email", required=True, help="git user email")
    ap.add_argument("-a", "--authentication", required=True, help="git authentication token")
    run(vars(ap.parse_args()))


def run(args):
    print(f"Attempting to create auto PR against {args['originURL']}\n")
    workingPath = os.path.join(os.getcwd(), "tempRepo")
    removeDir(workingPath)
    originBranch = "autoBranch" + str(random.randint(0,10000))
#    print("- getting material from remote")
#    repo = setupRepo(workingPath, args["originURL"], originBranch, args["email"], args["user"], args["authentication"])
    print(f"- searching file {args['file']} in working branch")
    files = find_files(args["file"], ".")
    print(f"- updating file(s)")
    isUpdated = updateFiles(files, args["find"], args["replace"])
#    if isUpdated:
#        print(f"- commit and push change to remote")
#        gitCommitPush(repo, originBranch, args["message"])
#        print(f"- creating PR")
#        return True
#    else:
#        print("abort: nothing to update\n")
#        return False
#    removeDir(workingPath)


def removeDir(workingPath):
    path = Path(workingPath)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)


def find_files(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if re.match(name, filename):
                result.append(os.path.join(root, filename))
                print(".", end="")
    print("\n")
    return result


def updateFiles(files, find, replace):
    for file in files:
        pattern = re.compile(find)
        with open(file) as inFile:
            input = inFile.read()
            search = re.search(find, input)
            if search is not None:
                output = re.sub(find, replace, input)
                temp = file + ".temp"
                with open(temp, "w") as outFile:
                    outFile.write(output)
                    os.remove(file)
                    os.rename(temp, file)
                    print(f"updated {file}\n")
                    return True
    return False


def setupRepo(path, originURL, originBranch, email, user, token):
    repo = git.Repo.clone_from(originURL, path)
    print(f"cloned from origin {originURL}")

    with repo.config_writer() as git_config:
        git_config.set_value("user", "email", email)
        git_config.set_value("user", "name", user)
        git_config.set_value("user", "token", token)

    repo.git.branch(originBranch)
    repo.git.checkout(originBranch)
    print(f"created working branch {originBranch}")

#    upstream = repo.create_remote("upstream", url=upstreamURL)
#    upstream.fetch()
#    repo.git.reset("--hard", f"upstream/{upstreamBranch}")
#    print(f"reset based on upstream {upstreamURL}/{upstreamBranch}\n")
    return repo


def gitCommitPush(repo, originBranch, disableMsg):
    changed = [ item.a_path for item in repo.index.diff(None) ]
    print(changed)
    if changed:
        repo.git.add(".")
        print(repo.git.commit("-s", "-m", disableMsg))
        origin = repo.remote(name="origin")
        result = origin.push(refspec=f"{originBranch}:{originBranch}")
        print(f"change pushed from {result[0].local_ref} to {result[0].remote_ref}\n")

        
"""
curl \
  -X POST \
  -H "Authorization: token <git token>" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/llxia/openj9/pulls \
  -d "{"title":"my test PR","head":"asm","base":"master"}"  
"""
 
if __name__ == "__main__":
    main()
