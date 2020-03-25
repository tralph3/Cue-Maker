import os
import glob

directory = input("Input the absolute path to the folder where the bin files are located: ")
os.chdir(directory)

binFiles = glob.glob("**/*.bin", recursive=True)

def makeCue():
    for file in binFiles:
        fileDirectory = file[0:file.rfind("/") + 1]
        cue = open(fileDirectory + file[file.rfind("/"):len(file) - 4] + ".cue", "w+")
        cueText = "FILE \"" + file[file.rfind("/") + 1:len(file)] + "\" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n"
        cue.write(cueText)

makeCue()
