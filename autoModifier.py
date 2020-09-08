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
    ap.add_argument("-d", "--directory", required=True, help="directory to modify")
    run(vars(ap.parse_args()))


def run(args):
    print(f"- searching file {args['file']} in {args['directory']}")
    files = find_files(args["file"], args['directory'])
    print(f"- updating file(s)")
    isUpdated = updateFiles(files, args["find"], args["replace"])


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
 
if __name__ == "__main__":
    main()
