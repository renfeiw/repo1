import autoModifier
import argparse
import re

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--message", required=True, help="exclude message")
    ap.add_argument("-d", "--directory", required=True, help="directory to modify")
    ap.add_argument("-i", "--issue", required=True, help="issue URL")
    args = vars(ap.parse_args())

    newArgs = {
        "directory": args["directory"]
    }
    match = re.match(r"auto ([A-Za-z]+) test ([a-zA-Z0-9]+)( in ([\.a-zA-Z0-9]+))?", args["message"])
    if match:
        print(f"{args['message']}\n")
        mode = match.group(1)
        test = match.group(2)
        file = "playlist.xml"
        if match.group(3):
            file = match.group(4)
        newArgs.update({
            "file": file
        })
        if (mode == "exclude") and (file == "playlist.xml"):
            excludeTestInPlaylist(test, args["issue"], newArgs)
        else:
            print("function not supported for now")
    else:
        print(f"unrecognized message: {args['message']}")

def excludeTestInPlaylist(test, issue, args):
    args.update({
        "find" : fr"(([ \t]*)<\s*testCaseName\s*>\s*{test}\s*<\s*/testCaseName\s*>)",
        "replace": fr"\1\n\2<disabled>{issue}</disabled>"
    })
    autoModifier.run(args)


if __name__ == "__main__":
    main()
    
