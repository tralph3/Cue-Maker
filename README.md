# PSX Cue Maker
A simple and easy to use program that makes .cue and .m3u files for your PSX roms.

# Usage
This program will work with the following extensions:

```
.bin > .cue and .m3u creation
.img > .cue and .m3u creation
.chd > .m3u creation
```

Using this program is really simple, **you will need Python 3.5 or greater to run this software**. Simply run the program on a command line and pass the following arguments like this:

```
$ CueMaker.py <directory> <recursive>
```

The directory argument is pretty self explanatory, the recursive parameter is a question. It asks you if you want to make the program recursive (i.e. search all sub-folders in the directory). For yes, put a y, for no, an n. If you don't input anything as a second parameter, then the default is n.

**This program won't detect roms that have Track files, and need more data in their .cue files for them to work**

**This program will create .m3u files provided your files are named in the following manner:**

```
"Game (Disc X)"
"Game (DiscX)"
"Game_(Disc X)"
"Game_(DiscX)"
```
 **The disc needs to be sorrounded by parenthesis (case insensitive)**
 
 **You can use the format "Disc x of x" as long as it's sorrounded by parenthesis**
 
 **There must be a space or an underscore before the opening parenthesis** (if you wish to modify this condition it's on line 85 of the latest version)
 
 ## You are free to distribute and modify this software as long as you don't claim it as your own.
