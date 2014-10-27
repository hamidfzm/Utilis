#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Hamid FzM"
__copyright__ = "Copyright 2014, The Utilis Project"
__credits__ = ["Hamid FzM"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Hamid FzM"
__email__ = "hamidfzm@gmail.com"
__status__ = "Develop"

from os import path, getcwd, listdir, rename
print("It's possible to rename a group of sequential file like img001.jpg, \
img002.jpg, etc., img100.jpg with this utility. Use asterisk wildcard \
for file name pattern.\n\
For Example: img*.jpg\n")

def dotextention(extension):
    if extension.startswith('.'):
        return extension
    return '.%s'%extension

directory = raw_input('Enter folder [default](%s): '%getcwd()) or getcwd()
pattern = raw_input('Enter files naming pattern [default](*): ') or '*'
extension = raw_input('Enter files naming filter [default](*): ').split(',')

if extension is not None:
    extension = tuple(map(dotextention, extension))
wildcard = int(raw_input('Enter wildcard size [default](2): ') or 2)

counter = 0

print('Renaming files in %s ...\n'%directory)

for item in listdir(directory):
    if item.endswith(extension):
        counter += 1

        dest = pattern.replace('*', str(counter).zfill(wildcard)) + path.splitext(item)[1]
        rename(path.join(directory, item),
               path.join(directory, dest))
        print('%s renamed to %s'%(item, dest))
