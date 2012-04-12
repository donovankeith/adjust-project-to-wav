"""
adjustProjectToWav v0.2.1 (April 12, 2012)
Copyright (C) 2012 by Donovan Keith (www.donovankeith.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE
 
Written for CINEMA 4D R12.048

Name-US: Adjust Project to .WAV
Description-US: Adjust Project to .WAV :: Adds a sound track to your scene, adjusts max time and adds buffer with markers 1 sec before start and end.

Version History:
0.2 = Changed default behavior to add track and offset it 1sec.

TO DO:
	Load .wav files into the Sound Track.
	Encapsulate some of the marker creation logic.
"""

import os, sys
import c4d
import wave

debug = False

def main():
	# Open a file chooser
	wav_path = c4d.storage.LoadDialog(c4d.FSTYPE_ANYTHING, title="Select a WAVE (*.wav) File", flags=False)
	wave_name = os.path.basename(wav_path)       # default name = filename

	if debug:
		print "wave_name: ", wave_name
    
	# Open the file
	wav = wave.open(wav_path,'rb')
	
	#Get framerate and length
	wav_frame_rate = wav.getframerate()
	wav_num_frames = wav.getnframes()
	
	length_in_seconds = float(wav_num_frames) / float(wav_frame_rate)
	
	if debug:
		print "wav_frame_rate = ", wav_frame_rate
		print "wav_num_frames = ", wav_num_frames
		print "length_in_seconds = ", length_in_seconds
		
	#Create and name the Sound null object
	sound_obj = c4d.BaseObject(c4d.Onull)
	sound_obj.SetName("Sound: " + wave_name)
	
	#Add and hide the Sound object
	doc.InsertObject(sound_obj)
	doc.SetActiveObject(sound_obj)
	sound_obj.SetEditorMode(c4d.MODE_OFF)
	sound_obj.SetRenderMode(c4d.MODE_OFF)
	
	#Tell C4D something has changed
	c4d.EventAdd()
	
	#Add a Sound track
	sound_track = c4d.CTrack(sound_obj, c4d.DescID(c4d.DescLevel(c4d.CTsound, c4d.CTsound, 0)))
	sound_track[c4d.CID_SOUND_START] = c4d.BaseTime(1.0)
	sound_track[c4d.CID_SOUND_NAME] = wav_path
	sound_obj.InsertTrackSorted(sound_track)

#	#Set the Sound property to the wav file NOT WORKING
#	sound_track[c4d.CID_SOUND_NAME] = "Test.wav"
#
#	if debug:
#		print "sound_track[c4d.CID_SOUND_NAME] = ", sound_track[c4d.CID_SOUND_NAME]
	
	#Tell C4D something has changed
	c4d.EventAdd()

	#Update Document Properties
	doc_frame_rate = doc.GetFps()
	rounded_max_time = round(round((length_in_seconds + 2.0) * doc_frame_rate)/doc_frame_rate)
	doc_max_time = c4d.BaseTime(rounded_max_time)
	doc.SetMaxTime(doc_max_time)
	
	#Store the current time
	old_time = doc.GetTime()
	
	#Open Timeline 4 (so marker command works)
	c4d.CallCommand(465001513) #Open Timeline 4
	
	#Marker at 0
	doc.SetTime(c4d.BaseTime(0.0))
	c4d.CallCommand(465001124) #Add a Marker

	#Marker at 1
	doc.SetTime(c4d.BaseTime(1.0))
	c4d.CallCommand(465001124) #Add a Marker
	
	#Marker at 1 second til end
	doc.SetTime(c4d.BaseTime(rounded_max_time - 1.0))
	c4d.CallCommand(465001124) #Add a Marker	

	#Marker at end
	doc.SetTime(c4d.BaseTime(rounded_max_time))
	c4d.CallCommand(465001124) #Add a Marker	

	#Set Preview Range Min/Max
	doc.SetLoopMinTime(c4d.BaseTime(0.0))
	doc.SetLoopMaxTime(c4d.BaseTime(rounded_max_time))

	c4d.EventAdd()

	#Close Timeline 4 (to cleanup view)
	c4d.CallCommand(12392) #CloseWindow

	#Restore the time to before script
	doc.SetTime(old_time)
	c4d.EventAdd()
	
if __name__ == "__main__":
	main()