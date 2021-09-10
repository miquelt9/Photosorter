# Photosorter
## Description
This respository cointains a python script that allows you to sort your photos.                                                 
It uses the exif data of the photos to keep them nicely organized.

## Brief Story
I've a external drive to keep my photos, and due to I wanted to sort them I searched a program to do it, however the one I founded ([andrewning](https://github.com/andrewning)/[sortphotos](https://github.com/andrewning/sortphotos)) didn't work for me because my amount of photos, it keeped the data stored in the ram memory before moving it to the destination and so the program was killed each time.                                     
So I finally did what Alex told me to do in first place which was writting an script by myself, and there it is.                                          
Please feel free to open issues/pull requests, suggest or ask whatever you want.

## Requirements
As you will have to run the program without installing anything you must have the libraries used in the script to run it.                             
They are _exif_, _Pillow_ and _pathlib_ :
```
pip install exif
pip install Pillow
pip install pathlib
```
    
## Running the script
To run the script the script you'll have to download the photosorter.py file and run it in the folder you want (I actually recommend to do it in the upper folder where the photos you wanna sort are)
```
python photosorter.py
```
Then you'll be asked to answer some question to configure the program

## Versions
#### 10/09/2021
The script is actually in beta version.                                                              
It only will be in  beta meanwhile reconfiguring issue is open (WIP)                                                     
Sorry for the personal comments i will work further into the documentation of the script
