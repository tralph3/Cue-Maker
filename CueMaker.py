#!/usr/bin/env python3
##################################
#                                #
#       Created by tralph3       #
#   https://github.com/tralph3   #
#                                #
##################################


import os
import glob

while True:
    try:
        directory = input("Input the absolute path to the folder where the roms are located: ")
        os.chdir(directory)
        break
    except FileNotFoundError:
        print("Invalid directory")

recursive = input("Search sub-folders? (y|n): ")

types = ("*.bin","*.img", "*.chd")

matchingFiles = []
cueFiles = []

if recursive == "y" or recursive == "Y":
    for files in types:
        matchingFiles.extend(glob.glob("**/" + files, recursive=True))
elif recursive == "n" or recursive == "N":
    for files in types:
        matchingFiles.extend(glob.glob(files))

print("Creating .cue...\n")

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
    print("Found file: \"" + fileName + "\"")
    if not os.path.isfile(cuePath):
        cue = open(cuePath, "w+")
        cueText = "FILE \"" + fileName + "\" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n"
        cue.write(cueText)
        cue.close()
        print("Created: \"" + fileName[0:len(fileName) - 4] + ".cue\"\n--------")
    else:
        print("This file already has a .cue\n--------")
    cueFiles.append(cuePath)

print("\nCreating .m3u...\n")

for file in cueFiles:
    if file.rfind("/") != -1:
        fileDirectory = file[0:file.rfind("/") + 1]
        fileName = file[file.rfind("/") + 1:len(file)]
    else:
        fileDirectory = ""
        fileName = file

    if fileName.lower().find(" (disc") != -1 or fileName.lower().find("_(disc") != -1:
        print("Found file: \"" + fileName + "\"")
        try:
            discWordIndex = fileName.lower().index(" (disc")
        except ValueError:
            discWordIndex = fileName.lower().index("_(disc")
        m3uFilePath = fileDirectory + fileName[0:discWordIndex] + ".m3u"
        m3u = open(m3uFilePath, "a+")
        m3u.seek(0)
        if m3u.read().find(fileName) == -1:
            m3u.write(fileName + "\n")
            print("Wrote \"" + fileName + "\" to \"" + fileName[0:discWordIndex] + ".m3u\"\n--------")
        else:
            print("\"" + fileName + " is already present on \"" + fileName[0:discWordIndex] + ".m3u\"\n--------")
        m3u.close()

print("\n\nFinished.")
