#!/usr/bin/env python3
##################################
#                                #
#       Created by tralph3       #
#   https://github.com/tralph3   #
#                                #
##################################

import os
import glob
import hashlib
import argparse
from urllib.request import urlopen


parser = argparse.ArgumentParser(description="Original .cue file fetcher for game roms and .m3u creator.")
parser.add_argument("directory", type=str, help="the directory for the roms")
parser.add_argument("-r", "--recursive", action="store_true", help="search sub-folders")
parser.add_argument("-g", "--generic", action="store_true", help="create generic .cue files if originals can't be found")
parser.add_argument("-m", "--m3u", action="store_true", help="create .m3u files for multiple disc games")
args = parser.parse_args()

recursive = args.recursive
genericCues = args.generic
allowM3u = args.m3u
types = ("*.bin", "*.img", "*.chd")

matchingFiles = []
cueFiles = []

m3uWriteCounter = 0
cueCreatedCounter = 0

currentGameCue = ""
currentGameCuePath = ""
currentGameTrackNumber = 0

def getSha1(file):
    hashSha1 = hashlib.sha1()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashSha1.update(chunk)
    return hashSha1.hexdigest()

def createGenericCue(cuePath, fileName, system="PlayStation"):
    global cueCreatedCounter
    if system == "PlayStation":
        number = "2"
    elif system == "Saturn":
        number = "1"

    cue = open(cuePath, "w+")
    cueText = "FILE \"" + fileName + "\" BINARY\n  TRACK 01 MODE" + number + "/2352\n    INDEX 01 00:00:00\n"
    cue.write(cueText)
    cue.close()
    print("\u001b[36mCreated: \"\u001b[1;33m" + fileName[0:len(fileName) - 4] + ".cue\u001b[36m\"\u001b[0m\n--------")
    cueCreatedCounter += 1

def fetchCue(entryName, system):
    #Creates links given an entry name
    if system == "PlayStation":
        try:
            link = 'https://raw.githubusercontent.com/tralph3/Cue-Maker/master/Sony PlayStation Cue Sheets (redump.org)/' + entryName[:len(entryName)-4] + ".cue"
            link = link.replace(" ", "%20")
            cueText = urlopen(link).read().decode("UTF-8")
        except Exception:
            return Exception
    elif system == "Saturn":
        try:
            link = 'https://raw.githubusercontent.com/tralph3/Cue-Maker/master/Sega Saturn Cue Sheets (redump.org)/' + entryName[:len(entryName)-4] + ".cue"
            link = link.replace(" ", "%20")
            cueText = urlopen(link).read().decode("UTF-8")
        except Exception:
            return Exception
    return cueText

def getTrackNumber(entryName):
    trackIndex = entryName.lower().rfind("(track ")
    spaceIndex = entryName.rfind(" ", trackIndex, len(entryName))
    parenthesisIndex = entryName.rfind(")", trackIndex, len(entryName))
    trackNumber = entryName[spaceIndex+1:parenthesisIndex]
    return str(trackNumber).zfill(2)

def replaceCueFileName(cueText, fileName):
    nameIndex = cueText.find("\"")
    lastIndex = cueText.find("\"", nameIndex + 1)
    cueText = cueText.replace(cueText[nameIndex + 1:lastIndex], fileName, 1)
    return cueText

def generateCue(file):
    global currentGameCue
    global currentGameCuePath
    global cueCreatedCounter
    global currentGameTrackNumber

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
        foundEntry = psxHashFile.find(fileHash)

        if foundEntry == -1:
            foundEntry = saturnHashFile.find(fileHash)
            system = saturnHashFile
            systemName = "Saturn"

            if foundEntry == -1:

                if fileName.lower().rfind("track") != -1:
                    print("\u001b[1;31mCouldn't find database entry, track file detected, not generating .cue...\u001b[0m")
                    return None
                else:

                    if genericCues:
                        print("\u001b[1;31mCouldn't find database entry, creating generic .cue...\u001b[0m")
                        createGenericCue(cuePath, fileName)
                        cueFiles.append(cuePath)
                        return None
                    else:
                        print("\u001b[1;31mCouldn't find database entry.\u001b[0m\n--------")
                        return None
        else:
            system = psxHashFile
            systemName = "PlayStation"

        #Create an entry name based by a fixed offset from the hash
        print("\u001b[1;33mHash \u001b[1;32m" + fileHash + "\u001b[1;33m matches database!")
        lineEnd = system.find("\n", foundEntry)
        entryName = system[int(foundEntry + len(fileHash) + 2):int(lineEnd)]
        #If the file has multiple tracks, use special conditions
        if entryName.rfind("Track ") != -1:

            #Modify entry name to get the appropiate link
            trackNumber = getTrackNumber(entryName)
            entryName = entryName.replace(" (Track " + str(int(trackNumber)) + ").bin", ".cue")

            if entryName[-4:] == ".bin":
                entryName = entryName.replace(" (Track " + trackNumber + ").bin", ".cue")

            if int(trackNumber) == 1:
                #Fetch the cue and save its entirety into the global variable "currentGameCue"
                cueText = fetchCue(entryName, systemName)

                if cueText == Exception:
                    print("\u001b[1;31mCouldn't find original cue on GitHub.\u001b[0m\n--------")
                    return None

                #Generate text to write to cue
                currentGameCue = cueText
                trackIndex = currentGameCue.find("TRACK ")
                nextFileIndex = cueText.find("FILE \"", trackIndex)
                trackCueText = cueText[:nextFileIndex]
                trackCueText = replaceCueFileName(trackCueText, fileName)
                
                #Generate path for cue
                cuePathTrackIndex = cuePath.lower().rfind(" (track")
                cuePathParenthesisIndex = cuePath.find(")", cuePathTrackIndex)
                cuePath = cuePath.replace(cuePath[cuePathTrackIndex:cuePathParenthesisIndex+1], "")
                cue = open(cuePath, "a+")
                cueFiles.append(cuePath)

                #Set data for future track files
                currentGameCuePath = cuePath
                currentGameTrackNumber = int(trackNumber) + 1
                cueCreatedCounter += 1
                cueFiles.append(cuePath)
            else:

                #If track number is other than 1, use the cue from the previous file with "track 1"
                if currentGameCue == "":
                    print("\u001b[1;31mCouldn't find original cue on GitHub.\u001b[0m\n--------")
                    return None

                #Generate text to write to cue
                trackIndex = currentGameCue.find("TRACK " + str(currentGameTrackNumber).zfill(2))
                fileIndex = currentGameCue.rfind("FILE \"", 0, trackIndex)
                nextFileIndex = currentGameCue.find("FILE \"", trackIndex)
                trackCueText = currentGameCue[fileIndex:nextFileIndex]
                trackCueText = replaceCueFileName(trackCueText, fileName)                
                cue = open(currentGameCuePath, "a+")
                currentGameTrackNumber += 1
            cue.seek(0)
            if cue.read().find(trackCueText) == -1:
                cue.write(trackCueText)
                print("\u001b[1;33mAdded track file to the .cue!\u001b[0m\n--------")
            else:
                print("\u001b[1;31mTrack file already present.\u001b[0m")
            cue.close()                        

        else:
            #Try to fetch the cue, if it fails default to generic
            cueText = fetchCue(entryName, systemName)
            if cueText == Exception:
                if genericCues:
                    print("\u001b[1;31mCouldn't find github entry, creating generic .cue...\u001b[0m")
                    createGenericCue(cuePath, fileName, systemName)
                    cueFiles.append(cuePath)
                    return None
                else:
                    print("\u001b[1;31mCouldn't find original cue on GitHub.\u001b[0m\n--------")
                return None

            cueText = replaceCueFileName(cueText, fileName)
            cue = open(cuePath, "w+")
            cue.write(cueText)
            cue.close()
            print("\u001b[36mFetched: \"\u001b[1;33m" + fileName[0:len(fileName) - 4] + ".cue\u001b[36m\"\u001b[0m\n--------")
            cueCreatedCounter += 1
            cueFiles.append(cuePath)
    else:
        print("\u001b[1;31mThis file already has a .cue\u001b[0m\n--------")
        cueFiles.append(cuePath)

def createM3u(cueFiles):
	global m3uWriteCounter
	
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
			discWordIndex = fileName.lower().rfind(" (disc")
			discClose = fileName.lower().rfind(")", discWordIndex + 2)
			m3uFilePath = fileDirectory + fileName.replace(fileName[discWordIndex:discClose + 1], "").replace(fileName[-4:], ".m3u")
			m3u = open(m3uFilePath, "a+")
			m3u.seek(0)
			if m3u.read().find(fileName) == -1:
				m3u.write(fileName + "\n")
				print("\u001b[36mWrote \"\u001b[1;34m" + fileName + "\u001b[36m\" to \"\u001b[1;33m" + fileName[0:discWordIndex] + ".m3u\u001b[36m\"\u001b[0m\n--------")
				m3uWriteCounter += 1
			else:
				print("\u001b[31m\"\u001b[1;34m" + fileName + "\u001b[31m\" is already present on \"\u001b[33m" + fileName[0:discWordIndex] + ".m3u\u001b[31m\"\u001b[0m\n--------")
			m3u.close()

try:
    link = 'https://raw.githubusercontent.com/tralph3/Cue-Maker/master/psx.hash'
    psxHashFile = urlopen(link).read().decode("UTF-8")
    link = 'https://raw.githubusercontent.com/tralph3/Cue-Maker/master/saturn.hash'
    saturnHashFile = urlopen(link).read().decode("UTF-8")
except Exception:
    try:
        print("\u001b[0;31mError: Can't connect to GitHub, defaulting to local hash file.\u001b[0m")
        psxHashFile = open("psx.hash", "r").read()
        saturnHashFile = open("saturn.hash", "r").read()
    except FileNotFoundError:
        print("\u001b[0;31mError: Can't find hash file, make sure they are on the same folder as the script.\u001b[0m")
        exit()

try:
    directory = args.directory
    os.chdir(directory)
except FileNotFoundError:
    print("\u001b[0;31mInvalid directory\u001b[0m")
    exit()

if recursive:
    for files in types:
        matchingFiles.extend(glob.glob("**/" + files, recursive=True))
        matchingFiles = sorted(matchingFiles)
else:
    for files in types:
        matchingFiles.extend(glob.glob(files))
        matchingFiles = sorted(matchingFiles)

print("\u001b[1;32mCreating .cue...\u001b[0m\n")

for file in matchingFiles:
    generateCue(file)

if allowM3u:
	createM3u(cueFiles)

print("\n\n\033[32mFinished!\nCreated \u001b[35m" + str(cueCreatedCounter) + "\u001b[32m .cue and wrote \u001b[35m" + str(m3uWriteCounter) + "\u001b[32m lines to .m3u!\u001b[0m")
