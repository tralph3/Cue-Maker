import os
import glob

directory = input("Input the absolute path to the folder where the bin files are located: ")
os.chdir(directory)

binFiles = glob.glob("*.bin")

def makeCue():
    for file in binFiles:
        cue = open(file[0:len(file) - 4] + ".cue", "w+")
        cueText = "FILE \"" + file + "\" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n"
        cue.write(cueText)

makeCue()
