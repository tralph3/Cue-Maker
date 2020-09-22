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

echo "It's needed to run the script as root to move the files to /usr in some distros"

chmod +x cuemaker
sudo chown root cuemaker
sudo chown root links.cfg
sudo mkdir -vp /usr/share/cuemaker/
sudo mv -vf links.cfg /usr/share/cuemaker/
sudo mv -vf COPYING.txt /usr/share/cuemaker/
sudo mv -vf README.md /usr/share/cuemaker/
sudo mv -vf cuemaker /usr/bin/
