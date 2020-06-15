#!/usr/bin/env python3
##################################
#                                #
#       Created by tralph3       #
#   https://github.com/tralph3   #
#                                #
##################################

import os
import glob
import sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("\u001b[1;31mUsage:\n----------\u001b[0m\n\n")
    print("\u001b[0;32;40m$ python3 CueMaker.py <directory> <y|n>\u001b[0m <--recursive\n")
    print("Go to \"\u001b[2;34mgithub.com/tralph3/psx-cue-maker\u001b[0m\" for detailed usage instructions.")
    exit()

try:
    directory = sys.argv[1]
    os.chdir(directory)
except FileNotFoundError:
    print("\033[0;33;47m Invalid directory")
    exit()

try:
    recursive = sys.argv[2]
except IndexError:
    recursive = "n"

types = ("*.bin", "*.img", "*.chd")

matchingFiles = []
cueFiles = []
m3uWriteCounter = 0
cueCreatedCounter = 0

if recursive == "y" or recursive == "Y":
    for files in types:
        matchingFiles.extend(glob.glob("**/" + files, recursive=True))
elif recursive == "n" or recursive == "N":
    for files in types:
        matchingFiles.extend(glob.glob(files))
else:
    print("\u001b[0;31mError: Bad argument, only \"y\" or \"n\" accepted\u001b[0m")
    exit()

print("\u001b[1;32mCreating .cue...\u001b[0m\n")

for file in matchingFiles:
    if file.rfind(".chd") != -1:
        cueFiles.append(file)
        continue

    if file.rfind("/") != -1:
        fileDirectory = file[0:file.rfind("/") + 1]
        fileName = file[file.rfind("/") + 1:len(file)]
    else:
        fileDirectory = ""
        fileName = file

    cuePath = fileDirectory + fileName[0:len(fileName) - 4] + ".cue"
    print("Found file: \"\u001b[1;33m" + fileName + "\u001b[0m\"")
    if not os.path.isfile(cuePath):
        cue = open(cuePath, "w+")
        cueText = "FILE \"" + fileName + "\" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n"
        cue.write(cueText)
        cue.close()
        print("\u001b[36mCreated: \"\u001b[1;33m" + fileName[0:len(fileName) - 4] + ".cue\u001b[36m\"\u001b[0m\n--------")
        cueCreatedCounter += 1
    else:
        print("\u001b[1;31mThis file already has a .cue\u001b[0m\n--------")
    cueFiles.append(cuePath)

print("\n\u001b[1;32mCreating .m3u...\u001b[0m\n")

for file in cueFiles:
    if file.rfind("/") != -1:
        fileDirectory = file[0:file.rfind("/") + 1]
        fileName = file[file.rfind("/") + 1:len(file)]
    else:
        fileDirectory = ""
        fileName = file

    if fileName.lower().find(" (disc") != -1 or fileName.lower().find("_(disc") != -1:
        print("Found file: \"\u001b[1;33m" + fileName + "\u001b[0m\"")
        try:
            discWordIndex = fileName.lower().index(" (disc")
        except ValueError:
            discWordIndex = fileName.lower().index("_(disc")
        m3uFilePath = fileDirectory + fileName[0:discWordIndex] + ".m3u"
        m3u = open(m3uFilePath, "a+")
        m3u.seek(0)
        if m3u.read().find(fileName) == -1:
            m3u.write(fileName + "\n")
            print("\u001b[36mWrote \"\u001b[1;34m" + fileName + "\u001b[36m\" to \"\u001b[1;33m" + fileName[0:discWordIndex] + ".m3u\u001b[36m\"\u001b[0m\n--------")
            m3uWriteCounter += 1
        else:
            print("\u001b[31m\"\u001b[1;34m" + fileName + "\u001b[31m\" is already present on \"\u001b[33m" + fileName[0:discWordIndex] + ".m3u\u001b[31m\"\u001b[0m\n--------")
        m3u.close()

print("\n\n\033[32mFinished!\nCreated \u001b[35m" + str(cueCreatedCounter) + "\u001b[32m .cue and wrote \u001b[35m" + str(m3uWriteCounter) + "\u001b[32m lines to .m3u!\u001b[0m")
