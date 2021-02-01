#!/bin/sh
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

if [ "$EUID" -ne 0 ]; then 
  echo "It's needed to run the script as root to move the files to /usr in some distros"
  exit 1
fi

sudo mkdir -vp /usr/share/cuemaker/

sudo cp -vf links.cfg COPYING.txt README.md /usr/share/cuemaker/
sudo cp -vf cuemaker.py /usr/local/bin/cuemaker

sudo chmod +x /usr/local/bin/cuemaker
sudo chown -R root:root /usr/share/cuemaker/
