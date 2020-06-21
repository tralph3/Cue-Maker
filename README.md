# Cue Maker
A simple and easy to use program that fetches the original .cue files for your roms.

# Usage
This program will work with the following extensions:

```
.bin > .cue and .m3u creation
.img > .cue and .m3u creation
.chd > .m3u creation
```

**It is required for the "psx.hash" file to be in the same folder as the script.**

Using this program is really simple, **you will need Python 3.5 or greater to run this software**. Simply run the program on a command line and pass the following arguments like this:

```
$ CueMaker.py <directory> <recursive> <generic-cues>
```

**Directory:** Input the absolute directory to your rom/s location.

**Recursive:** y/n tells the program to search sub-folders, default is n.

**Generic Cues:** y/n tells the program to generate generic cue files in case the originals can't be found.


```
$ CueMaker.py C:\RetroArch\Roms y y
```
**For Track file detection to work correctly, the track number should be at the end of the file name like so:**
```
Need for Speed - Porsche Unleashed (USA) (Track 04).bin
```

**The following will *most likely* cause issues:**
```
Need for Speed - Porsche Unleashed (Track 04) (USA).bin
```

**This program will create .m3u files provided your files are named in the following manner:**

```
"Game (Disc X)"
"Game (DiscX)"
"Game_(Disc X)"
"Game_(DiscX)"
```
 **The disc needs to be sorrounded by parenthesis (case insensitive)**
 
 **You can use the format "Disc x of x" as long as it's sorrounded by parenthesis**
 
 
**Many thanks to opsxcq for providing the cue sheets and the database: https://github.com/opsxcq/psx-cue-sbi-collection**
## You are free to distribute and modify this software as long as you don't claim it as your own.
