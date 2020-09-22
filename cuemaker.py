#!/usr/bin/env python3
#
#Create .cue and .m3u files for your roms
#Copyright (C) 2020  Tomás Ralph
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##################################
#                                #
#       Created by tralph3       #
#   https://github.com/tralph3   #
#                                #
##################################

import os, glob, hashlib, argparse, configparser, platform, ssl
from zipfile import ZipFile, ZIP_DEFLATED
from urllib.request import urlopen
from shutil import rmtree


# create SSL certificates
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
	ssl._create_default_https_context = ssl._create_unverified_context

# stats to display at the end
m3uWriteCounter = 0
cueCreatedCounter = 0
zipCreatedCounter = 0

# variables used for multi-track roms
currentGameCue = ""
currentGameCuePath = ""
currentGameTrackNumber = 0

def getSha1(file):
	hashSha1 = hashlib.sha1()
	with open(file, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hashSha1.update(chunk)
	return hashSha1.hexdigest()

def createGenericCue(cuePath, fileName):
	global cueCreatedCounter

	cue = open(cuePath, "w+")
	cueText = "FILE \"" + fileName + "\" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n"
	cue.write(cueText)
	cue.close()
	print("\u001b[36mCreated: \"\u001b[1;33m" + fileName[0:len(fileName) - 4] + ".cue\u001b[36m\"\u001b[0m\n--------")
	cueCreatedCounter += 1

def fetchCue(entryName):
	# creates links given an entry name
	if args.system == "playstation":
		link = "{}{}.cue".format(configParser.get('Links', 'psxCueBase'), entryName[:-4]).replace(" ", "%20")
		cueText = urlopen(link).read().decode("UTF-8")
	elif args.system == "saturn":
		link = "{}{}.cue".format(configParser.get('Links', 'saturnCueBase'), entryName[:-4]).replace(" ", "%20")
		cueText = urlopen(link).read().decode("UTF-8")
	elif args.system == "playstation2":
		link = "{}{}.cue".format(configParser.get('Links', 'ps2CueBase'), entryName[:-4]).replace(" ", "%20")
		cueText = urlopen(link).read().decode("UTF-8")
	elif args.system == "3do":
		link = "{}{}.cue".format(configParser.get('Links', '3doCueBase'), entryName[:-4]).replace(" ", "%20")
		cueText = urlopen(link).read().decode("UTF-8")
	return cueText

def getTrackNumber(entryName):
	trackIndex = entryName.lower().rfind("(track ")
	spaceIndex = entryName.rfind(" ", trackIndex, len(entryName))
	parenthesisIndex = entryName.rfind(")", trackIndex, len(entryName))
	trackNumber = entryName[spaceIndex+1:parenthesisIndex]
	return str(trackNumber).zfill(2)

def replaceCueFileName(cueText, fileName):
	# replaces the "FILE" entry in the cue with the provided file name
	nameIndex = cueText.find("\"")
	lastIndex = cueText.find("\"", nameIndex + 1)
	cueText = cueText.replace(cueText[nameIndex + 1:lastIndex], fileName, 1)
	return cueText

def zipFiles(folderPath):
	global zipCreatedCounter
	print("Compressing files in \"\u001b[1;33m" + folderPath + "\u001b[0m\"...")
	with ZipFile(folderPath + ".zip", 'a') as currentZip:
		files = []
		files.extend(glob.glob(folderPath + "/*"))
		for file in files:
			if not os.path.basename(file) in currentZip.namelist():
				currentZip.write(file, arcname=os.path.basename(file), compress_type=ZIP_DEFLATED)
		zipCreatedCounter += 1
	print("Deleting \"\u001b[1;33m" + folderPath + "\u001b[0m\"...\n--------")
	rmtree(folderPath)

def generateCue(file):
	global currentGameCue
	global currentGameCuePath
	global cueCreatedCounter
	global currentGameTrackNumber

	# ignore .chd files
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
	# only attempt to create cues if there's none
	if not os.path.isfile(cuePath):
		print("\u001b[1;32mGenerating SHA-1 hash...\u001b[0m\n")
		fileHash = getSha1(file)
		foundEntry = hashFile.find(fileHash)

		if foundEntry == -1:

			if fileName.lower().rfind("track") != -1:
				print("\u001b[1;31mCouldn't find database entry, track file detected, not generating .cue...\u001b[0m")
				return None
			else:

				if args.generic:
					print("\u001b[1;31mCouldn't find database entry, creating generic .cue...\u001b[0m")
					createGenericCue(cuePath, fileName)
					cueFiles.append(cuePath)
					return None
				else:
					print("\u001b[1;31mCouldn't find database entry.\u001b[0m\n--------")
					return None

		# create an entry name based by a fixed offset from the hash
		print("\u001b[1;33mHash \u001b[1;32m" + fileHash + "\u001b[1;33m matches database!")
		lineEnd = hashFile.find("\n", foundEntry)
		entryName = hashFile[int(foundEntry + len(fileHash) + 2):int(lineEnd)]

		# if the file has multiple tracks, use special conditions
		if entryName.rfind("Track ") != -1:

			# modify entry name to get the appropiate link
			trackNumber = getTrackNumber(entryName)
			entryName = entryName.replace(entryName[entryName.lower().index(" (track"):], ".cue")

			if int(trackNumber) == 1:
				# fetch the cue and save its entirety into the global variable "currentGameCue" for later use
				try:
					cueText = fetchCue(entryName)
				except Exception:
					print("\u001b[1;31mCouldn't find original cue on GitHub.\u001b[0m\n--------")
					return None

				# generate text to write to cue
				currentGameCue = cueText
				trackIndex = currentGameCue.find("TRACK ")
				nextFileIndex = cueText.find("FILE \"", trackIndex)
				trackCueText = cueText[:nextFileIndex]
				trackCueText = replaceCueFileName(trackCueText, fileName)

				# generate path for cue
				cuePathTrackIndex = cuePath.lower().rfind(" (track")
				cuePathParenthesisIndex = cuePath.find(")", cuePathTrackIndex)
				cuePath = cuePath.replace(cuePath[cuePathTrackIndex:cuePathParenthesisIndex+1], "")
				cue = open(cuePath, "a+")

				# set data for future track files
				currentGameCuePath = cuePath
				currentGameTrackNumber = int(trackNumber) + 1
				cueCreatedCounter += 1
				cueFiles.append(cuePath)
			else:
				# if track number is other than 1, use the cue from the previous file with "track 1"

				# if there's no set "current cue" this means there was no "track 1" rom
				if currentGameCue == "":
					print("\u001b[1;31mERROR: ROM doesn't have a TRACK 1\u001b[0m\n--------")
					return None

				# generate text to write to cue
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

		# for single file roms
		else:
			# try to fetch the cue, if it fails default to generic
			try:
				cueText = fetchCue(entryName)
			except Exception:
				if args.generic:
					print("\u001b[1;31mCouldn't find github entry, creating generic .cue...\u001b[0m")
					createGenericCue(cuePath, fileName)
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
			discWordIndex = fileName.lower().index(" (disc")
			discEndIndex = fileName.find(")", discWordIndex) + 1
			m3uFilePath = fileDirectory + fileName.replace(fileName[discWordIndex:discEndIndex], "").replace(fileName[-4:], ".m3u")
			m3u = open(m3uFilePath, "a+")
			m3u.seek(0)
			if m3u.read().find(fileName) == -1:
				m3u.write(fileName + "\n")
				print("\u001b[36mWrote \"\u001b[1;34m" + fileName + "\u001b[36m\" to \"\u001b[1;33m" + fileName[0:discWordIndex] + ".m3u\u001b[36m\"\u001b[0m\n--------")
				m3uWriteCounter += 1
			else:
				print("\u001b[31m\"\u001b[1;34m" + fileName + "\u001b[31m\" is already present on \"\u001b[33m" + fileName[0:discWordIndex] + ".m3u\u001b[31m\"\u001b[0m\n--------")
			m3u.close()

if __name__ == "__main__":

	scriptDirectory = os.path.dirname(os.path.realpath(__file__)) + "/"

	configParser = configparser.RawConfigParser()

	# windows uses local folder for the links.cfg
	if platform.system() == "Windows":
		configFilePath = "links.cfg"
	else:
		configFilePath = "/usr/share/cuemaker/links.cfg"

	configParser.read(configFilePath)

	parser = argparse.ArgumentParser(description="Original .cue file fetcher for game roms and .m3u creator.", prog="cuemaker")
	parser.add_argument("system", type=str, help="the system (console) the roms belong to", choices=["playstation", "playstation2", "saturn", "3do"])
	parser.add_argument("directory", type=str, help="the directory for the roms")
	parser.add_argument("-r", "--recursive", action="store_true", help="search sub-folders")
	parser.add_argument("-g", "--generic", action="store_true", help="create generic .cue files if originals can't be found")
	parser.add_argument("-m", "--m3u", action="store_true", help="create .m3u files for multiple disc games")
	parser.add_argument("-z", "--zips", action="store_true", help="extracts zip files containing roms, processes them and re-zips them in a single one (-r needs to be activated)")
	args = parser.parse_args()

	types = ("*.bin", "*.img", "*.chd")

	matchingFiles = []
	cueFiles = []
	zipsFolders = []

	if args.system == "playstation":
		try:
			link = configParser.get("Links", "psxHash")
			hashFile = urlopen(link).read().decode("UTF-8")
		except Exception:
			print("\u001b[0;31mError: Can't connect to GitHub, defaulting to local hash file.\u001b[0m")
			try:
				hashFile = open(scriptDirectory + "psx.hash", "r").read()
			except FileNotFoundError:
				print("\u001b[0;31mError: Can't find hash file, make sure they are on the same folder as the script.\u001b[0m")
				exit()

	elif args.system == "saturn":
		try:
			link = configParser.get("Links", "saturnHash")
			hashFile = urlopen(link).read().decode("UTF-8")
		except Exception:
			print("\u001b[0;31mError: Can't connect to GitHub, defaulting to local hash file.\u001b[0m")
			try:
				hashFile = open(scriptDirectory + "saturn.hash", "r").read()
			except FileNotFoundError:
				print("\u001b[0;31mError: Can't find hash file, make sure they are on the same folder as the script.\u001b[0m")
				exit()

	elif args.system == "playstation2":
		try:
			link = configParser.get("Links", "ps2Hash")
			hashFile = urlopen(link).read().decode("UTF-8")
		except Exception:
			print("\u001b[0;31mError: Can't connect to GitHub, defaulting to local hash file.\u001b[0m")
			try:
				hashFile = open(scriptDirectory + "ps2.hash", "r").read()
			except FileNotFoundError:
				print("\u001b[0;31mError: Can't find hash file, make sure they are on the same folder as the script.\u001b[0m")
				exit()

	elif args.system == "3do":
		try:
			link = configParser.get("Links", "3doHash")
			hashFile = urlopen(link).read().decode("UTF-8")
		except Exception:
			print("\u001b[0;31mError: Can't connect to GitHub, defaulting to local hash file.\u001b[0m")
			try:
				hashFile = open(scriptDirectory + "3do.hash", "r").read()
			except FileNotFoundError:
				print("\u001b[0;31mError: Can't find hash file, make sure they are on the same folder as the script.\u001b[0m")
				exit()

	try:
		directory = args.directory
		os.chdir(directory)
	except FileNotFoundError:
		print("\u001b[0;31mInvalid directory\u001b[0m")
		exit()

	while(True):
		if args.zips:
			if not args.recursive:
				print("\u001b[0;31mError: Recursive needs to be on to unzip files. Ommiting.\u001b[0m")
				break

			matchingZips = []
			matchingZips.extend(glob.glob("**/*.zip", recursive=True))
			matchingZips = sorted(matchingZips)

			print("\n\u001b[1;32mExtracting .zip...\u001b[0m\n")

			for zip in matchingZips:
				with ZipFile(zip, 'r') as currentZip:
					try:
						discWordIndex = zip.lower().index(" (disc")
						discEndIndex = zip.find(")", discWordIndex) + 1
						tmpZipFolder = zip.replace(zip[discWordIndex:discEndIndex], "")
					except ValueError:
						tmpZipFolder = zip

					print("Extracting: \"\u001b[1;33m" + zip + "...\u001b[0m\"\n--------")
					tmpZipFolder = tmpZipFolder[:-4]
					currentZip.extractall(tmpZipFolder)
					if not tmpZipFolder in zipsFolders:
						zipsFolders.append(tmpZipFolder)
		break

	if args.recursive:
		for files in types:
			matchingFiles.extend(glob.glob("**/" + files, recursive=True))
			matchingFiles = sorted(matchingFiles)
	else:
		for files in types:
			matchingFiles.extend(glob.glob(files))
			matchingFiles = sorted(matchingFiles)

	print("\n\u001b[1;32mCreating .cue...\u001b[0m\n")

	for file in matchingFiles:
		generateCue(file)

	if args.m3u:
		createM3u(cueFiles)

	if args.zips:
		print("\n\u001b[1;32mCompressing and deleting temporary folders...\u001b[0m\n")
		for folder in zipsFolders:
			zipFiles(folder)

	print("\n\n\033[32mFinished!\nCreated \u001b[35m" + str(cueCreatedCounter) + "\u001b[32m .cue, \u001b[35m" + str(zipCreatedCounter) + "\u001b[32m .zip and wrote \u001b[35m" + str(m3uWriteCounter) + "\u001b[32m lines to .m3u!\u001b[0m")
