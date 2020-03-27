# PSX Cue Maker
A simple and easy to use program that makes .cue and .m3u files for your PSX games.

# Usage
PS1 roms generally come in 3 formats, .bin, .img and .iso. You will need .cue files for .bin and .img, but .iso are extent from this, for this reason, this program will work with the mentioned formats only.

Using this program is really simple, **you will need Python 3.5 or greater to run this software**. Simply download the .py file and run it on the command line, it will ask you to input the absolute path to the folder where your roms are located, i.e. "C:\roms" for Windows, "~/roms" for Linux. After that it will ask you if you want it to search sub-folders, I added this check to not make a mess or need to move folders in case you don't want it entering other places. Then, it will create your files.

**This program won't detect roms that have Track files, and need more data in their .cue files for them to work**

**This program will create .m3u files provided your files are named in the following manner:**

```
"Game (Disc X)"
"Game (DiscX)"
"Game_(Disc X)"
"Game_(DiscX)"
```
 **The disc needs to be sorrounded by parenthesis (case insensitive)**
 
 **There must be a space or an underscore before the opening parenthesis** (if you wish to modify this condition it's on line 70)
 
 ## You are free to distribute and modify this software as long as you don't claim it as your own.
