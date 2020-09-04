import autoCommitter
import argparse
import re


ORIGIN_OPENJ9 = "github.com/renfeiw/myrepo.git"


"""
ORIGIN_ADOPTOPENJDK = "https://github.com/renfeiw/openjdk-tests.git"
UPSTREAM_ADOPTOPENJDK = "https://github.com/AdoptOpenJDK/openjdk-tests.git"
UPSTREAM_ADOPTOPENJDK_BRANCH = "master"

ORIGIN_OPENJ9 = "https://github.com/renfeiw/openj9.git"
UPSTREAM_OPENJ9 = "https://github.com/eclipse/openj9.git"
UPSTREAM_OPENJ9_BRANCH = "master"
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--mode", required=True, help="operation on test, supported mode: disable")
    ap.add_argument("-t", "--test", required=True, help="test name")
    ap.add_argument("-i", "--issue", required=True, help="issue URL")
    ap.add_argument("-f", "--file", default="playlist.xml", help="regex file name to modify")
    ap.add_argument("-u", "--user", required=True, help="git user id")
    ap.add_argument("-e", "--email", required=True, help="git user email")
    ap.add_argument("-a", "--authentication", required=True, help="git authentication token")
    args = vars(ap.parse_args())
    
    newArgs = {
        "file": args["file"],
        "user": args["user"],
        "email": args["email"],
        "authentication": args["authentication"]
    }

    if (args["mode"] == "disable"):
        if (re.match(args["file"], r"playlist.xml")):
            disableTestInPlaylist(args["test"], args["issue"], newArgs)


def disableTestInPlaylist(test, issue, args):
    print(f"Creating auto PR to disable {test} in {args['file']}\n")

    args.update({
        "find" : fr"(([ \t]*)<\s*testCaseName\s*>\s*{test}\s*<\s*/testCaseName\s*>)",
        "replace": fr"\1\n\2<disabled>{issue}</disabled>",
        "message": f"Auto: disable {test}\n- related issue: {issue}"})
    
    rt = False
    args.update({
        "originURL": f"https://{args['user']}:{args['authentication']}@{ORIGIN_OPENJ9}"})
    rt = autoCommitter.run(args)
"""
    args.update({
        "originURL": ORIGIN_ADOPTOPENJDK,
        "upstreamURL": UPSTREAM_ADOPTOPENJDK,
        "upstreamBranch": UPSTREAM_ADOPTOPENJDK_BRANCH})
    rt or autoCommitter.run(args)
"""

if __name__ == "__main__":
    main()
    
