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
import hashlib
from urllib.request import urlopen

def getSha1(file):
    hashSha1 = hashlib.sha1()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashSha1.update(chunk)
    return hashSha1.hexdigest()

try:
    hashFile = open("disk.hash", "r").read()
except FileNotFoundError:
    print("\u001b[0;31mError: Can't find \"disk.hash\", make sure it's on the same folder as the script\u001b[0m")
    exit()

if len(sys.argv) < 2 or len(sys.argv) > 4:
    print("\u001b[1;31mUsage:\n----------\u001b[0m\n\n")
    print("\u001b[0;32;40m$ python3 CueMaker.py <directory> <recursive> <generic-cues>\u001b[0m\n")
    print("Go to \"\u001b[2;36mgithub.com/tralph3/psx-cue-maker\u001b[0m\" for detailed usage instructions.")
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

try:
    genericCues = sys.argv[3]
    if genericCues.lower() == "y":
        genericCues = True
    elif genericCues.lower() == "n":
        genericCues = False
    else:
        print("\u001b[0;31mError: Bad argument, only \"y\" or \"n\" accepted\u001b[0m")
        exit()
except IndexError:
    genericCues = True

types = ("*.bin", "*.img", "*.chd")

matchingFiles = []
cueFiles = []
m3uWriteCounter = 0
cueCreatedCounter = 0

if recursive.lower() == "y":
    for files in types:
        matchingFiles.extend(glob.glob("**/" + files, recursive=True))
elif recursive.lower() == "n":
    for files in types:
        matchingFiles.extend(glob.glob(files))
else:
    print("\u001b[0;31mError: Bad argument, only \"y\" or \"n\" accepted\u001b[0m")
    exit()

print("\u001b[1;32mCreating .cue...\u001b[0m\n")

def createGenericCue(cuePath, fileName):
    cue = open(cuePath, "w+")
    cueText = "FILE \"" + fileName + "\" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n"
    cue.write(cueText)
    cue.close()
    print("\u001b[36mCreated: \"\u001b[1;33m" + fileName[0:len(fileName) - 4] + ".cue\u001b[36m\"\u001b[0m\n--------")
    global cueCreatedCounter
    cueCreatedCounter += 1

def fetchCue(entryName):
    #Creates links given an entry name
    try:
        link = 'https://raw.githubusercontent.com/opsxcq/psx-cue-sbi-collection/master/redump.org/' + entryName[:len(entryName)-4] + ".cue"
        link = link.replace(" ", "%20")
        cueText = urlopen(link).read().decode("UTF-8")
    except Exception:
        link = 'https://raw.githubusercontent.com/opsxcq/psx-cue-sbi-collection/master/emuparadise.me/' + entryName[:len(entryName)-4] + "/" + entryName[:len(entryName)-4] + ".cue"
        link = link.replace(" ", "%20")
        cueText = urlopen(link).read().decode("UTF-8")
    return cueText

def getTrackNumber(entryName):
    trackIndex = entryName.rfind("(Track ")
    spaceIndex = entryName.rfind(" ", trackIndex, len(entryName))
    parenthesisIndex = entryName.rfind(")", trackIndex, len(entryName))
    trackNumber = entryName[spaceIndex+1:parenthesisIndex]
    return str(trackNumber.zfill(1))

def replaceCueFileName(cueText, fileName):
    nameIndex = cueText.find("\"")
    lastIndex = cueText.find("\"", nameIndex + 1)
    cueText = cueText.replace(cueText[nameIndex + 1:lastIndex], fileName, 1)
    return cueText

def generateCue(file):
    #Ignore .chd files
    if file.rfind(".chd") != -1:
        cueFiles.append(file)
        return None

    if file.rfind("/") != -1:
        fileDirectory = file[0:file.rfind("/") + 1]
        fileName = file[file.rfind("/") + 1:len(file)]
    else:
        fileDirectory = ""
        fileName = file

    cuePath = fileDirectory + fileName[0:len(fileName) - 4] + ".cue"
    print("Found file: \"\u001b[1;33m" + fileName + "\u001b[0m\"")
    #Only attempt to create cues if there's none
    if not os.path.isfile(cuePath):
        print("\u001b[1;32mGenerating SHA-1 hash...\u001b[0m\n")
        fileHash = getSha1(file)
        foundEntry = hashFile.find(fileHash)
        if foundEntry == -1:
            if fileName.rfind("Track") != -1:
                print("\u001b[1;31mCouldn't find database entry, track file detected, not generating .cue...\u001b[0m")
                return None
            else:
                if genericCues:
                    print("\u001b[1;31mCouldn't find database entry, creating generic .cue...\u001b[0m")
                    createGenericCue(cuePath, fileName)
                    cueFiles.append(cuePath)
                else:
                    print("\u001b[1;31mCouldn't find database entry.\u001b[0m\n--------")
        else:
            #Create an entry name based by a fixed offset from the hash
            print("\u001b[1;33mHash \u001b[1;32m" + fileHash + "\u001b[1;33m matches database!")
            lineEnd = hashFile.find("\n", foundEntry)
            entryName = hashFile[int(foundEntry + len(fileHash) + 2):int(lineEnd)]
            #If the file has multiple tracks, use special conditions
            if entryName.rfind("Track ") != -1:
                trackNumber = getTrackNumber(entryName)
                index = entryName.rfind("(Track ")
                entryName = entryName.replace(entryName[index-1:], ".cue")
                try:
                    cueText = fetchCue(entryName)
                    trackIndex = cueText.find("TRACK " + trackNumber)
                    fileIndex = cueText.rfind("FILE \"", 0, trackIndex)
                    nextFileIndex = cueText.find("FILE \"", trackIndex)
                    trackCueText = cueText[fileIndex:nextFileIndex]
                    trackCueText = replaceCueFileName(trackCueText, fileName)
                    cuePathTrackIndex = cuePath.rfind(" (Track")
                    cuePathParenthesisIndex = cuePath.rfind(")")
                    cuePath = cuePath.replace(cuePath[cuePathTrackIndex:cuePathParenthesisIndex+1], "")
                    cue = open(cuePath, "a+")
                    if cue.read().find(trackCueText) == -1:
                        cue.write(trackCueText)
                        print("\u001b[1;33mAdded track file to the .cue!\u001b[0m\n--------")
                    else:
                        print("\u001b[1;33mTrack file already present.\u001b[0m")
                    cue.close()
                except Exception:
                    if genericCues:
                        print("\u001b[1;31mCouldn't find github entry, creating generic .cue...\u001b[0m")
                        createGenericCue(cuePath, fileName)
                        cueFiles.append(cuePath)
                    else:
                        print("\u001b[1;31mCouldn't find database entry.\u001b[0m\n--------")
                    return None


            else:
                #Try to fetch it from two sources, if both fail default to generic
                try:
                    cueText = fetchCue(entryName)
                except Exception:
                    if genericCues:
                        print("\u001b[1;31mCouldn't find github entry, creating generic .cue...\u001b[0m")
                        createGenericCue(cuePath, fileName)
                        cueFiles.append(cuePath)
                    else:
                        print("\u001b[1;31mCouldn't find database entry.\u001b[0m\n--------")
                    return None

                cueText = replaceCueFileName(cueText, fileName)
                cue = open(cuePath, "w+")
                cue.write(cueText)
                cue.close()
                print("\u001b[36mFetched: \"\u001b[1;33m" + fileName[0:len(fileName) - 4] + ".cue\u001b[36m\"\u001b[0m\n--------")
                global cueCreatedCounter
                cueCreatedCounter += 1
    else:
        print("\u001b[1;31mThis file already has a .cue\u001b[0m\n--------")
    cueFiles.append(cuePath)

for file in matchingFiles:
    generateCue(file)
    

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
