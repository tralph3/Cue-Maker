#!/usr/bin/env python3
##################################
#                                #
#       Created by tralph3       #
#   https://github.com/tralph3   #
#                                #
##################################

import tkinter as tk
from tkinter import filedialog
import subprocess
import shlex
import os
import sys

def askDirectory():
	selectedDirectory = filedialog.askdirectory()
	if selectedDirectory != "":
		directoryEntry.delete(0, "end")
		directoryEntry.insert(0, selectedDirectory)
	return
	
def callCueMaker():
	if os.path.isfile("CueMaker.py"):
		command = [sys.executable, "CueMaker.py"]
		if recursiveVar.get():
			command.append("-r")
		if genericVar.get():
			command.append("-g")
		command.append(directoryEntry.get())
		
		process = subprocess.Popen(command)
		while True:
			if(process.poll() != None):
				generatingText.config(text="Done!")
				break
	else:
		generatingText.config(text="Can't find CueMaker.py, make sure it's in the same directory as the gui.")
	return

window = tk.Tk()
window.title("tralph3's Cue Maker")

topFrame = tk.Frame(window, padx = 20, pady = 20)
middleFrame = tk.Frame(window, padx = 20)
bottomFrame = tk.Frame(window, padx = 20, pady = 10)

recursiveVar = tk.IntVar()
recursiveCheck = tk.Checkbutton(topFrame, text="Search sub-folders", font=40, variable=recursiveVar)

genericVar = tk.IntVar()
genericCheck = tk.Checkbutton(topFrame, text="Create generic cues*", font=40, variable=genericVar)
genericExplanation = tk.Label(bottomFrame, text="*Only creates generic cues if the original can't be found", font=("Monospace", 8))

directoryEntry = tk.Entry(middleFrame, width=44, borderwidth=2)
directoryEntry.insert(0, "Enter rom directory")
directoryButton = tk.Button(middleFrame, text="...", command=askDirectory)

submitButton = tk.Button(bottomFrame, text="Create cues!", command=callCueMaker)

generatingText = tk.Label(bottomFrame)


recursiveCheck.pack(side = "top", anchor = "nw")

genericCheck.pack(side = "top", anchor = "nw")


directoryEntry.pack(side = "left", fill = "x")
directoryButton.pack(side = "right")

submitButton.pack(side = "top")

generatingText.pack(side = "top")

genericExplanation.pack(side = "bottom")

topFrame.pack(side = "top", anchor = "nw")
middleFrame.pack(side = "top")
bottomFrame.pack(side = "top")

window.mainloop()
