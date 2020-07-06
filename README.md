# Cue Maker
A simple and easy to use program that fetches the original .cue files for your roms.

# Dependencies

```
Python 3.5 or greater
tkinter module (GUI only)
```

# Usage
This program will work with the following extensions:

```
.bin > .cue and .m3u creation
.img > .cue and .m3u creation
.chd > .m3u creation
```

**You only need the file "CueMaker.py" everything else will be fetched from this repo.**

Using this program is really simple. I'm using the argparse library, so you can pass the -h flag for usage instructions. Alternatively, you can see the output of the command here:

```
usage: CueMaker.py [-h] [-r] [-g] directory

Original .cue file fetcher for game roms and .m3u creator.

positional arguments:
  directory        the directory for the roms

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  search sub-folders
  -g, --generic    create generic cue files if originals can't be found

```

If you want to use a GUI, run the GUI.py file on a terminal. You can still see the console output. The GUI.py file is entirely optional.

## Formatting

You will need to follow certaing formatting on the roms name's in order to ensure the correct functionality of the program. The list of roms is ordered alphabetically when the program is executed, for this reason you need to make sure that Track and Disc files are in the correct order. To make it easy, make sure your roms comply with these points:

* If the file is a Track file, it must be enclosed in parenthesis and must have a space beforehand: " (Track 2)"
* If the game has multiple discs, you need to state it the same way as tracks: " (Disc 3)"
* If the game has multiple discs and multiple track files, the Disc indicator **must come before the Track indicator.**
* Preferably, put the Disc and Track indicators after the game's name, you may specify region anywhere else.

This is a correctly formatted list of roms:

```
3x3 Eyes - Kyuusei Koushu S (Japan) (Disc 1) (Track 1).bin
3x3 Eyes - Kyuusei Koushu S (Japan) (Disc 1) (Track 2).bin
3x3 Eyes - Kyuusei Koushu S (Japan) (Disc 1) (Track 3).bin
3x3 Eyes - Kyuusei Koushu S (Japan) (Disc 1) (Track 4).bin
3x3 Eyes - Kyuusei Koushu S (Japan) (Disc 2) (Track 1).bin
3x3 Eyes - Kyuusei Koushu S (Japan) (Disc 2) (Track 2).bin
```

## You are free to distribute and modify this software as long as you don't claim it as your own.
