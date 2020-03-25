import os
import glob

directory = input("Input the absolute path to the folder where the bin files are located: ")
os.chdir(directory)

types = ("*.bin","*.img")

matchingFiles = []

for files in types:
    matchingFiles.extend(glob.glob("**/" + files, recursive=True))

for file in matchingFiles:
    if file.rfind("/") != -1:
        fileDirectory = file[0:file.rfind("/") + 1]
        fileName = file[file.rfind("/") + 1:len(file)]
    else:
        fileDirectory = ""
        fileName = file

    cue = open(fileDirectory + fileName[0:len(fileName) - 4] + ".cue", "w+")
    cueText = "FILE \"" + fileName + "\" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n"
    cue.write(cueText)
