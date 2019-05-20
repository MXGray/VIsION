<p><a href="https://github.com/MXGray/VIsION/blob/master/AnimatedVIsIONLogo_1920x1080.gif" target="_blank"><img src="https://github.com/MXGray/VIsION/blob/master/AnimatedVIsIONLogo_1920x1080.gif" border="0" alt="Animated VIsION Logo: This is an image of a closed camera lens that opens up to show the word VIsION and closes back again, in a loop." width="480" height="270" align="left" HSPACE="30" VSPACE="30" /></a><h2>VIsION</h2><br>Wearable AI for the Blind<br></p>

This aims to provide visually impaired users with an affordable solution for their day-to-day activities.

Being completely blind myself, this can help me know the objects in front of me, their placement and the distance of my central focus, with or without an Internet connection.

This video shows the target objectives of this project:  https://www.youtube.com/tv#/watch?v=NIZj7IW-FDk

A wearable form factor will free up both our hands and give us optimum mobility.
-  This is unlike the difficulty we experience when we need to take out our smartphones from time to time while walking around and holding our white canes;
-  This is also much better than straining our arms, necks and backs just to capture what's in front of us like a paper document or a set of physical objects; and
-  I also want a solution that won't require me to take out my smartphone while walking around, especially here in the Philippines where I can be victimized by violent crooks who are out to steal expensive smartphones from random passersby (my blindness is due to a senseless incident of violence 15 years ago).

For offline multiple object detection and recognition, I used the following:
-  A set of fine-tuned object detection and recognition, person / face detection and age / gender estimation AI models; along with
-  Custom scripts for distance estimation through an ultrasonic sensor and clockface object placement description through image post-processing.

I also used services from Microsoft Cognitive Services (Computer Vision & Batch Read File APIs) and Cloudsight to integrate online object recognition, visual scene description and OCR (optical character recognition) functions.

Note:  Release v0.0.2 is updated with OCR functions ...

Audible descriptions are through the Microsoft SAPI5 engine. Meanwhile, remote manual visual assistance is through Skype.

My device also serves as my pocket computer, which is very useful for me when I'm up and about.

I'm still working on offline OCR functions, mainly document detection and super-resolution among other image pre and post-processing functions. Plus:
-  I'll continue to test and improve my trained / fine-tuned Tesseract model; and
-  I'll further optimize the hardware components and software features of my project.

Also, this live video is for San Francisco Lighthouse for the Blind's annual Holman Prize 2019 competition (ongoing as of this writing):  https://www.youtube.com/tv#/watch?v=A5O-R_WJDgQ
-  This project was hand-picked this April 2019 as a semifinalist out of more than 110 participants across 6 continents.
  
