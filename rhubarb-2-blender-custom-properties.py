#This blender script inserts the data from rhubarb as keyframed custom
#properties called 'visemeA', 'visemeB', etc onto the currently selected object.

#to use, change the variables rhubarb_path and audio_file to the correct values.
#- rhubarb_path should be the path to the rhubarb executible
#- audio_file should be the wav file you want to process.

#  note that on *nix, you can't use paths that use ~ refer to your home folder.

#Next, select the object you wish to attach the custom properties to.
#and run the script.

#if you get an error like 'command returned a non-zero exist status 1', 
#check the stderr of blender for more information. If that is inconvient, 
#it is likely that your audio_file can't be found or is the wrong format

#Note that the custom properties are on the 'Object Properties' tab, 
# not the 'Object Data Properties' tab

import bpy
import subprocess

rhubarb_path = "rhubarb" 
#if rhubarb is not in your PATH, replace with path to the rhubarb
#executible

audio_file = "/home/ribbon-otter/example-sound.wav"
#replace with the wav file you want to process

property_prefix = "viseme"
#the custom prefix for each custom property to solve any namespace collisions

rhubarb_output = subprocess.run([rhubarb_path, audio_file], capture_output=True, check=True)
#run rhubarb 

letters = ['A','B','C','D','E','F','G','H','X']
#all the possible letters that rhubarb outputs
#(including all the extentions)

data = rhubarb_output.stdout.split(b"\n")
data = [i.split(b"\t") for i in data]
#parse the data

obj = bpy.context.object
fps = bpy.context.scene.render.fps


for datum in data:
    
    if len(datum) < 2:
        continue
    #skip blank lines
    

    time, letter = datum
    letter = letter.decode();
    time = float(time);
    #load and convert to the correct types
    

    for test_letter in letters:
        obj[property_prefix + test_letter] = 1.0 if letter==test_letter else 0.0
        #set the custom properties in each object
    
    
    for i in letters:
        obj.keyframe_insert(data_path="[\"{}{}\"]".format(property_prefix,i), frame=time*fps)
        #insert a key frame for each custom property


#Author: ribbon-otter of github
#Date : 2022 Aug 16
#License: dual licensed under MIT and CC-0
#Copyright (c) 2022 ribbon-otter of github

#Permission is hereby granted, free of charge, to any person obtaining a copy of 
#this software and associated documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the
# following conditions:

#The above copyright notice and this permission notice (including the next paragraph)
# shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE. 
