#!usr/bin/env python  
#coding=utf-8  

#    Copyright (C) 2019  Grayscale & VIsION AI Labs Philippines
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#    The full GNU GPL v3 license of the software  and the hardware 3D printing source files in this repository ( https://github.com/MXGray/VIsION ) is found in https://github.com/MXGray/VIsION/commit/923b68e1dd835bd6ee00ebc5908de04146c1ea47
#   To contact the author of this repository, send an email to marxvergelmelencio@gmail.com or to grayscale.consultants@gmail.com or visit their Facebook page at https://facebook.com/grayscaleconsultants ...

# Import Required Packages
from __future__ import print_function

## Standard Packages
import os
os.system('color 9F')
import msvcrt
import subprocess
import sys
import time
import glob
import threading
import gc
import random
import requests
import operator
import datetime
import socket
import platform
from io import BytesIO

## Package to Send Emails from Gmail
import yagmail

if platform.system() == 'Windows':
	import win32gui
	import win32process

## Input Device Automation and Monitoring Packages
import keyboard
import pyautogui
pyautogui.FAILSAFE = False

## Audio Generation and Processing Packages
import pyaudio  
import wave  

## Image and Video Processing Libraries
import cv2
import numpy as np
OPENCV_VIDEOIO_PRIORITY_MSMF = 0
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from PIL import Image


# Collection of Non-Daemon Threads

## Beep Sound
if platform.system() == 'Windows':
	import winsound
	def beep(f,d):
		winsound.Beep(f,d)
elif platform.system() != 'Windows':
	# Install Beep by apt-get beep
	def beep(f,d):
		os.system('beep -f %s -l %s' % (f,d))

## Text-to-Speech
if platform.system() == 'Windows':
	### Windows-Specific TTS (Text to Speech) Packages
	from win32com.client import constants
	import win32com.client
	speaker=win32com.client.Dispatch('SAPI.SpVoice')
	# Configure TTS Settings
	speaker.Volume = 100
	speaker.Rate = 0
	def say(s):
		speaker.Speak(s)
elif platform.system() != 'Windows':
	### Run CLI Commands Below as Root to Install Pico TTS
	# wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-9_armhf.deb
	# wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-9_armhf.deb
	# apt-get install -f ./libttspico0_1.0+git20130326-9_armhf.deb ./libttspico-utils_1.0+git20130326-9_armhf.deb
	def say(s):
		os.system('pico2wave -w tmp.wav \"%s\"' % (s))
		os.system('rm -rf tmp.wav')

## Set Terminal Title
if platform.system() == 'Windows':
	import ctypes
	def title(s):
		ctypes.windll.kernel32.SetConsoleTitleW(s)
elif platform.system() != 'Windows':
	cmdterminal = ["xterm"]
	def title(s):
		# Tell Terminal to Change Current Title
		if os.getenv("TERM") in cmdterminal:
			print("\x1B]0;%s\x07" % s)

## Check Ultrasonic Ranger Hardware
from usb_iss import UsbIss, defs
iss = UsbIss()
def checkultrasonic():
	beep(538,333)
	print('\n   Checking Ultrasonic Ranger Hardware ...   \n')
	say('Checking hardware. ')
	try:
		if platform.system() == 'Windows':
			iss.open("COM7") # Check Device Manager for Correct COM Port Number
		elif platform.system() != 'Windows':
			iss.open('/dev/ttyACM0') # Check dmesg | grep -i /dev/tty* as Root
		iss.setup_i2c()
		beep(338,333)
		print('\n   Ultrasonic Ranger Found ...   \n   Activating Distance Sensing ...   \n')
		say('Ultrasonic ranger found. ')
		beep(338,333)
		say('Activating distance sensing. ')
		global ultrasonic
		ultrasonic = 'true'
	except Exception as e:
		ultrasonic = 'false'
		beep(138,333)
		print('\n   No Ultrasonic Ranger Found ...   \n   Disabling Distance Sensing ...   \n')
		say('Ultrasonic ranger not found! ')
		beep(138,333)
		say('Disabling distance sensing. ')

# Check Internet Connection
def checkinternet():
	beep(538,333)
	print('\n   Checking Internet Connectivity ...   \n')
	say('Checking Internet Connectivity.  ')
	remote_server = "www.youtube.com"
	try: 
		# Try to Resolve Host Name to Check If DNS is Listening
		host = socket.gethostbyname(remote_server)
		# Try to Connect to Host to Check If Host is Reachable
		s = socket.create_connection((host, 80), 2)
		s.close()
		global istatus
		istatus = 'true'
	except Exception as e:
		istatus = 'false'
	if istatus == 'true':
		beep(338,333)
		print('\n   Online & Offline Modes Enabled - Active Internet Connection Found ...   \n')
		say('Online and offline modes enabled. ')
	elif istatus == 'false':
		beep(238,333)
		print('\n  Offline Mode Enabled - Inactive Internet Connection ...   \n')
		say('Offline mode enabled. ')
		beep(238,333)
		say('Inactive Internet connection. ')

# Clean Up Environment
global path
path = os.path.dirname(os.path.realpath(__file__))
def cleanup():
	beep(538,333)
	print('\n   Preparing Virtual Environment ...   \n')
	say('Preparing virtual environment. ')
	global path
	path = os.path.dirname(os.path.realpath(__file__))
	try:
		if platform.system() == 'Windows':
			path = path.replace('\\','/')
		elif platform.system() != 'Windows':
			pass
		path1 = path+'/newimg/'
		path2 = path+'/killthread/'
		path3 = path+'/killthread2/'
		path4 = path+'/ocrfinroi/'
		path5 = path+'/ocrtxts/'
		path6 = path+'/ocrimgs/'
		os.system('rm -rf '+path1+'*')
		os.system('rm -rf '+path2+'*')
		os.system('rm -rf '+path3+'*')
		os.system('rm -rf '+path4+'*')
		os.system('rm -rf '+path5+'*')
		os.system('rm -rf '+path6+'*')
		return
	except Exception as e:
		say('Problem loading! Navigation mode deactivating now! Try to run again!  ')
		print('\n   Problem Loading ...   \n   Navigation Mode Deactivating Now ...   \n   Try Running Again ...   \n')
	if platform.system() == 'Windows':
		os.system('cls')
	elif platform.system() != 'Windows':
		os.system('clear')

## Check Camera
def checkcam():
	beep(538,333)
	print('\n   Checking Camera Hardware ...   \n')
	say('Checking camera. ')
	try:
		vs = WebcamVideoStream(src=0).start()
		window_name = "VIsION_CAM"
		interframe_wait_ms = 1200
		cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
		cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		while 1:
			frame = vs.read()
			frame = imutils.resize(frame, width=1600,height=1200)
			beep(333,666)
			cv2.imshow(window_name, frame)
			say('Active camera found. ')
			cv2.waitKey(interframe_wait_ms) 
			# Cam Cleanup
			cv2.destroyAllWindows()
			vs.stop()
			break
	except Exception as e:
		# Cam Cleanup
		cv2.destroyAllWindows()
		vs.stop()
		beep(338,333)
		print('\n   No Active Camera Found!   \n   Please Restart & Check ...   \n   Now Deactivating VIsION ...   \n')
		say('No active camera found. ')
		beep(238,222)
		say('Please restart and check. ')
		beep(338,222)
		beep(238,222)
		beep(1238,111)
		say('Now deactivating vision. ')
		sys.exit()

## Deactivate Sound
def deactivatesound(titletext):
	beep(338,333)
	beep(238,222)
	print('\n   '+titletext+' Deactivated ...   \n')
	beep(138,111)
	say(titletext+' deactivated!  ')
	CREATE_NO_WINDOW = 0x08000000
	if platform.system() == 'Windows':
		subprocess.call('taskkill /f /im firefox.exe /t', creationflags=CREATE_NO_WINDOW)
		os.system('cls')
	elif platform.system() != 'Windows':
		subprocess.call('kill -9 $(ps -x | grep firefox)', creationflags=CREATE_NO_WINDOW)
		os.system('clear')

## Intro Message for Each Mode
def intromsg(titletext):
	print('\n '+titletext+' Activated!  \n\n')
	if titletext == 'Navigation Mode' or titletext == 'Video Recording Mode' or titletext == 'Sound Recording Mode':
		print(' Quick Press to Go Back ... \n')
	else:
		pass
	beep(538,333)
	say(titletext+' activated. ')
	if titletext == 'Navigation Mode' or titletext == 'Video Recording Mode' or titletext == 'Sound Recording Mode':
		say('Quick press anytime to go back. ')
	else:
		pass
	if platform.system() == 'Windows':
		time.sleep(0.1)
		os.system('cls')
	elif platform.system() != 'Windows':
		time.sleep(0.1)
		os.system('clear')
	return

## Find Window Title and Activate
def findwin(titletext):
	if platform.system() == 'Windows':
		def window_enum_handler(hwnd, resultList):
			if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
				resultList.append((hwnd, win32gui.GetWindowText(hwnd)))
		def get_app_list(handles=[]):
			mlst=[]
			win32gui.EnumWindows(window_enum_handler, handles)
			for handle in handles:
				mlst.append(handle)
			return mlst
		appwindows = get_app_list()
		for i in appwindows:
			winname = i[1]
			winname = str(winname)
			winname = winname.strip()
			if winname == titletext:
				win32gui.SetForegroundWindow(i[0])
	elif platform.system() != 'Windows':
		# install wmctrl using apt-get install
		os.system('wmctrl -a '+titletext)


# Initialization
title("   VIsION Open Source DIY AI Glasses   ")

beep(538,333)
print('\n\n   VIsION   \n\n  Open Source, Do-It-Yourself  \n AI-Powered Eyeglasses for the Blind \n')
say('Vision. Open source, do it yourself, ')
say(', AI powered, eyeglasses for the blind. ')

checkultrasonic()
checkinternet()
cleanup()
checkcam()
gc.collect()

# Load VIsION Engine
beep(538,333)
print('\n   Now Loading VIsION ML & DL Models ...   \n')
say('Now loading vision machine learning and deep learning models. ')

## Main Navigation Mode Model
LABELS1 = open(path+'/multiobj/ade20k/classes.txt').read().strip().split("\n")
weightsPath1 = path+'/multiobj/ade20k/dn.caffemodel'
configPath1 = path+'/multiobj/ade20k/dn.prototxt'
net1 = cv2.dnn.readNetFromCaffe(configPath1, weightsPath1)
net1.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
net1.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

## Person and Object Detection Tensorflow Model
LABELS = open(path+'/multiobj/classes.txt').read().strip().split("\n")
weightsPath = path+'/multiobj/navnet.pb'
configPath = path+'/multiobj/navnet.pbtxt'
net = cv2.dnn.readNetFromTensorflow(weightsPath, configPath)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
#net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

## Face Detection Caffe Model
face_net = cv2.dnn.readNetFromCaffe(path+'/multiobj/face/deploy.prototxt.txt',path+'/multiobj/face/res10_300x300_ssd_iter_140000.caffemodel')
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
face_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
#face_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
face_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

## Age and Gender Estimation Tensorflow Model
age_list = ['zero to two-year old', 'four to six-year old', 'eight to twelve-year old', 'fifteen to twenty-year old', 'twenty five to thirty two-year old', 'thirty eight to forty three-year old', 'forty eight to fifty three-year old', 'sixty or so year old']
gender_list = ['male', 'female']
def initialize_caffe_models():
	age_net = cv2.dnn.readNetFromCaffe(path+'/multiobj/age/deploy_age.prototxt', path+'/multiobj/age/age_net.caffemodel')
	gender_net = cv2.dnn.readNetFromCaffe(path+'/multiobj/gender/deploy_gender.prototxt', path+'/multiobj/gender/gender_net.caffemodel')
	return(age_net, gender_net)
age_net, gender_net = initialize_caffe_models()
age_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
#age_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
age_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
gender_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
#gender_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
gender_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


#  IoT API Services
## Microsoft CIS Vision API Credentials
global onlinescenedescriptor_subscription_key
onlinescenedescriptor_subscription_key = "Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here"
if onlinescenedescriptor_subscription_key != 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here':
	assert onlinescenedescriptor_subscription_key
	onlinescenedescriptor_base_url = "https://southeastasia.api.cognitive.microsoft.com/vision/v2.0/"
	onlinescenedescriptor_analyze_url = onlinescenedescriptor_base_url + "analyze"
elif onlinescenedescriptor_subscription_key == 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here':
	print('\n   Offline Mode Only ...   \n   No Microsoft CIS Computer Vision API Credentials Found ...   \n   To enable faster recognition mode, open vision.py File. Press ctrl+f and type onlinescenedescriptor_subscription_key to supply your API key ...   \n')
	beep(238,333)
	say('Offline mode only. No Microsoft C I S computer vision API credentials found. To enable faster recognition mode, open vision.py file. Press control then F and type onlinescenedescriptor_subscription_key to supply your API key. ')

## Microsoft CIS OCR API Credentials
global onlineocr_subscription_key
onlineocr_subscription_key = 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here'
if onlineocr_subscription_key != 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here':
	assert onlineocr_subscription_key
	onlineocr_base_url = 'https://southeastasia.api.cognitive.microsoft.com/vision/v2.0/'
	text_recognition_url = onlineocr_base_url + 'read/core/asyncBatchAnalyze'
elif onlineocr_subscription_key == 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here':
	print('\n   Offline Mode Only ...   \n   No Microsoft CIS Computer Vision API Credentials Found ...   \n   To enable faster OCR mode, open vision.py File. Press ctrl+f and type onlineocr_subscription_key to supply your API key ...   \n')
	beep(238,333)
	say('Offline mode only. No Microsoft C I S computer vision API credentials found. To enable faster OCR mode, open vision.py file. Press control then f and type onlineocr_subscription_key to supply your API key. ')

## Cloudsight Image Classification API Credentials
import cloudsight
global onetimerecognition_api_key 
onetimerecognition_api_key = 'Enter-Your-Cloudsight-API-Key-Here'
global onetimerecognition_API 
onetimerecognition_API = 'Enter-Your-Cloudsight-API-Here'
if onetimerecognition_api_key != 'Enter-Your-Cloudsight-API-Key-Here':
	if onetimerecognition_API != 'Enter-Your-Cloudsight-API-Here':
		onetimerecognition_api_base_url = 'https://api.cloudsightapi.com'
	elif onetimerecognition_API == 'Enter-Your-Cloudsight-API-Here':
		print('\n   Offline Mode Only ...   \n   No Cloudsight API Credentials Found ...   \n   To enable one-time recognition mode, open vision.py File. Press ctrl+f and type onetimerecognition_API to supply your API keys ...   \n')
		beep(238,333)
		say('Offline mode only. No Cloudsight API credentials found. To enable one time recognition mode, open vision.py file. Press control then f and type onetimerecognition_API to supply your API keys. ')
elif onetimerecognition_api_key == 'Enter-Your-Cloudsight-API-Key-Here':
	print('\n   Offline Mode Only ...   \n   No Cloudsight API Credentials Found ...   \n   To enable one-time recognition mode, open vision.py File. Go to lines 312 and 313. Supply your API keys ...   \n')
	beep(238,333)
	say('Offline mode only. No Cloudsight API credentials found. To enable one time recognition mode, open vision.py file. Press control then f and type onetimerecognition_API to supply your API keys. ')


# Parent Thread of SeeingWithSound Mode
def seeingwithsoundmode():
	title("   SeeingWithSound Mode   ")
	titletext = 'SeeingWithSound Mode'

	cleanup()
	intromsg(titletext)

	# Distance Estimation Engine
	def distcalcx(dcx,t):
		try:
			iss.i2c.write(0xE0, 0x01, [0x06])
			iss.i2c.write(	0xE0, 0x02, [0xFF])

			while 1:
				event_is_set = dcx.wait(t)

				if event_is_set:
					return
				else:
					time.sleep(0.5)
					iss.i2c.write(0xE0, 0x00, [0x50])
					time.sleep(0.067)
					data = iss.i2c.read(0xE0, 0x03, 1)
					data = data[0]
					data = int(data)

					if data > 0 and data < 24:
						data = str(data)
						say(data+' inches! ')
					elif data > 24 and 	data < 108:
						data = int(data) / int(12)
						data = round(data,1)
						data = str(data)
						say(data+' feet! ')
					elif data > 108:
						say('Beyond nine feet! ')
					elif data == 0:
						time.sleep(0.067)

			return

		except Exception as e:
			print(e)
			#deactivatesound()

	dcx = threading.Event()
	distcalcx = threading.Thread(target=distcalcx,daemon=True,args=(dcx, 0.03), )

	# Run SeeingWithSound vOIC Offline Web Browser App
	currdir = os.path.dirname(os.path.realpath(__file__))+'\\SeeingWithSound.html'
	currdir = currdir.strip()
	if platform.system() == 'Windows':
		os.system('Start firefox '+currdir)
		os.system('cls')
	elif platform.system() != 'Windows':
		os.system('firefox '+currdir)
		os.system('clear')

	beep(666,333)
	print('\n   Quick Press to Deactivate SeeingWithSound vOIC ...   \n')
	say('Quick press to deactivate SeeingWithSound V O I C!  ')
	beep(333,222)
	pyautogui.press('esc')
	time.sleep(2.5)
	beep(333,222)
	pyautogui.press('esc')
	time.sleep(3.5)
	beep(555,222)

	if platform.system() == 'Windows':
		def window_enum_handler(hwnd, resultList):
			if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
				resultList.append((hwnd, win32gui.GetWindowText(hwnd)))
		def get_app_list(handles=[]):
			mlst=[]
			win32gui.EnumWindows(window_enum_handler, handles)
			for handle in handles:
				mlst.append(handle)
			return mlst
		appwindows = get_app_list()
		for i in appwindows:
			winname = i[1]
			winname = str(winname)
			winname = winname.strip()
			if winname == 'SeeingWithSound Mode  ':
				win32gui.SetForegroundWindow(i[0])
	elif platform.system() != 'Windows':
		pyautogui.hotkey('altleft','tab')

	if ultrasonic == 'true':
		distcalcx.start()
	elif ultrasonic == 'false':
		pass

	seeingwithsoundtimelimit = time.time() + 3600
	while 1:
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			if ultrasonic == 'true':
				dcx.set()
				break
			elif ultrasonic == 'false':
				break
		elif time.time() > seeingwithsoundtimelimit:
			if ultrasonic == 'true':
				dcx.set()
				break
			elif ultrasonic == 'false':
				break
		else:
			time.sleep(0.1)

	# Terminate SeeingWithSound Mode
	CREATE_NO_WINDOW = 0x08000000
	subprocess.call('taskkill /f /im firefox.exe /t', creationflags=CREATE_NO_WINDOW)
	if platform.system() == 'Windows':
		subprocess.call('taskkill /f /im firefox.exe /t', creationflags=CREATE_NO_WINDOW)
		os.system('cls')
	elif platform.system() != 'Windows':
		subprocess.call('kill -9 $(ps -x | grep firefox)', creationflags=CREATE_NO_WINDOW)
		os.system('clear')

	beep(338,222)
	beep(238,222)
	beep(138,111)
	say('SeeingWithSound mode deactivated!')
	print('\n   SeeingWithSound Mode Deactivated ...   \n')
	return


# Parent Thread of Navigation Mode
def navigationmode():
	## Initialization
	title("  VIsION Navigation Mode  ")
	titletext = 'Navigation Mode'

	intromsg(titletext)
	gc.collect()

	vs = WebcamVideoStream(src=0).start()
	window_name = "VIsION_CAM"
	interframe_wait_ms = 1000
	cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

	maintimelimit = time.time() + 300
	while not time.time() > maintimelimit:
		gc.collect()

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## Collection of Daemonic Threads

		#  wait sound
		def waitsound1(waitsnd1,t):
			time.sleep(0.1)
			speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
			psndcounter = -1
			psndcounter2 = -1
			say(random.choice(speakthisnow))
			print('\n   '+random.choice(speakthisnow)+'   \n')
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			while not waitsnd1.is_set():
				psndcounter += 25
				psndcounter2 += 0.01
				freq = 338 + psndcounter 
				dur = 66
				beep(freq,dur)
				time.sleep(0.2-psndcounter2)
				event_is_set = waitsnd1.wait(t)
				if event_is_set:
					break
			return
	
		waitsnd1 = threading.Event()
		waitsound1 = threading.Thread(target=waitsound1,daemon=True,args=(waitsnd1, 0.03), )
	
		def waitsound2(waitsnd2,t):
			time.sleep(0.1)
			speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
			psndcounter = -1
			psndcounter2 = -1
			say(random.choice(speakthisnow))
			print('\n   '+random.choice(speakthisnow)+'   \n')
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			while not waitsnd2.is_set():
				psndcounter += 25
				psndcounter2 += 0.01
				freq = 338 + psndcounter 
				dur = 66
				beep(freq,dur)
				time.sleep(0.2-psndcounter2)
				event_is_set = waitsnd2.wait(t)
				if event_is_set:
					break
			return
	
		waitsnd2 = threading.Event()
		waitsound2 = threading.Thread(target=waitsound2,daemon=True,args=(waitsnd2, 0.03), )
	
		def waitsound3(waitsnd3,t):
			time.sleep(0.1)
			speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
			psndcounter = -1
			psndcounter2 = -1
			say(random.choice(speakthisnow))
			print('\n   '+random.choice(speakthisnow)+'   \n')
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			while not waitsnd3.is_set():
				psndcounter += 25
				psndcounter2 += 0.01
				freq = 338 + psndcounter 
				dur = 66
				beep(freq,dur)
				time.sleep(0.2-psndcounter2)
				event_is_set = waitsnd3.wait(t)
				if event_is_set:
					break
			return
	
		waitsnd3 = threading.Event()
		waitsound3 = threading.Thread(target=waitsound3,daemon=True,args=(waitsnd3, 0.03), )
	
		## Distance Estimation Engine
		def distcalc1(dc1,t):
			try:
				iss.i2c.write(0xE0, 0x01, [0x06])
				iss.i2c.write(0xE0, 0x02, [0xFF])
				distcalctimelimit = time.time() + 9
				while time.time() < distcalctimelimit:
					event_is_set = dc1.wait(t)
					if event_is_set:
						iss.i2c.write(0xE0, 0x00, [0x50])
						time.sleep(0.067)
						data = iss.i2c.read(0xE0, 0x03, 1)
						data = data[0]
						data = int(data)
						if data > 0 and data < 24:
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' inches! ')
							break
						elif data > 24 and 	data < 108:
							data = int(data) / int(12)
							data = round(data,1)
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' feet! ')
							break
						elif data > 108:
							beep(338,222)
							say('Distance is beyond nine feet! ')
							break
						elif data == 0:
							beep(538,111)
							time.sleep(0.067)
					else:
						time.sleep(0.01)
				return
			except Exception as e:
				print(e)
	
		dc1 = threading.Event()
		distcalc1 = threading.Thread(target=distcalc1,daemon=True,args=(dc1, 0.03), )
	
		def distcalc2(dc2,t):
			try:
				iss.i2c.write(0xE0, 0x01, [0x06])
				iss.i2c.write(0xE0, 0x02, [0xFF])
				distcalctimelimit = time.time() + 9
				while time.time() < distcalctimelimit:
					event_is_set = dc2.wait(t)
					if event_is_set:
						iss.i2c.write(0xE0, 0x00, [0x50])
						time.sleep(0.067)
						data = iss.i2c.read(0xE0, 0x03, 1)
						data = data[0]
						data = int(data)
						if data > 0 and data < 24:
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' inches! ')
							break
						elif data > 24 and 	data < 108:
							data = int(data) / int(12)
							data = round(data,1)
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' feet! ')
							break
						elif data > 108:
							beep(338,222)
							say('Distance is beyond nine feet! ')
							break
						elif data == 0:
							beep(538,111)
							time.sleep(0.067)
					else:
						time.sleep(0.01)
				return
			except Exception as e:
				print(e)
	
		dc2 = threading.Event()
		distcalc2 = threading.Thread(target=distcalc2,daemon=True,args=(dc2, 0.03), )
	
		def distcalc3(dc3,t):
			try:
				iss.i2c.write(0xE0, 0x01, [0x06])
				iss.i2c.write(0xE0, 0x02, [0xFF])
				distcalctimelimit = time.time() + 9
				while time.time() < distcalctimelimit:
					event_is_set = dc3.wait(t)
					if event_is_set:
						iss.i2c.write(0xE0, 0x00, [0x50])
						time.sleep(0.067)
						data = iss.i2c.read(0xE0, 0x03, 1)
						data = data[0]
						data = int(data)
						if data > 0 and data < 24:
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' inches! ')
							break
						elif data > 24 and 	data < 108:
							data = int(data) / int(12)
							data = round(data,1)
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' feet! ')
							break
						elif data > 108:
							beep(338,222)
							say('Distance is beyond nine feet! ')
							break
						elif data == 0:
							beep(538,111)
							time.sleep(0.067)
					else:
						time.sleep(0.01)
				return
			except Exception as e:
				print(e)
	
		dc3 = threading.Event()
		distcalc3 = threading.Thread(target=distcalc3,daemon=True,args=(dc3, 0.03), )
	
		## Processing Sound
		def procsound1():
			try:
				# Define Stream Chunk
				chunk = 1024
				# Open WAV
				f = wave.open(path+'/takesnapshot.wav', "rb")
				# Instantiate PyAudio
				p = pyaudio.PyAudio()  
				# Open Stream
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
				# Read Data from Stream
				data = f.readframes(chunk)  
				# Play Stream
				while data:
					stream.write(data)
					data = f.readframes(chunk)
				# Stop Stream
				stream.stop_stream()
				stream.close()
				# Close PyAudio
				p.terminate()
				gc.collect()
			except Exception as e:
				print(e)
	
		procsound1 = threading.Thread(target=procsound1,daemon=True)
	
		def procsound2():
			try:
				# Define Stream Chunk
				chunk = 1024
				# Open WAV
				f = wave.open(path+'/takesnapshot.wav', "rb")
				# Instantiate PyAudio
				p = pyaudio.PyAudio()  
				# Open Stream
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
				# Read Data from Stream
				data = f.readframes(chunk)  
				# Play Stream
				while data:
					stream.write(data)
					data = f.readframes(chunk)
				# Stop Stream
				stream.stop_stream()
				stream.close()
				# Close PyAudio
				p.terminate()
				gc.collect()
			except Exception as e:
				print(e)
	
		procsound2 = threading.Thread(target=procsound2,daemon=True)
	
		def procsound3():
			try:
				# Define Stream Chunk
				chunk = 1024
				# Open WAV
				f = wave.open(path+'/takesnapshot.wav', "rb")
				# Instantiate PyAudio
				p = pyaudio.PyAudio()  
				# Open Stream
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
				# Read Data from Stream
				data = f.readframes(chunk)  
				# Play Stream
				while data:
					stream.write(data)
					data = f.readframes(chunk)
				# Stop Stream
				stream.stop_stream()
				stream.close()
				# Close PyAudio
				p.terminate()
				gc.collect()
			except Exception as e:
				print(e)
	
		procsound3 = threading.Thread(target=procsound3,daemon=True)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		rcounter = -1
		gc.collect()

		## Online Scene Descriptor
		while 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			frame = vs.read()
			frame = imutils.resize(frame, width=1600,height=1200)
			img_path = path+'/newimg/Analyzing_This_Scene.jpg'
			beep(333,666)
			cv2.imshow(window_name, frame)
			cv2.waitKey(interframe_wait_ms) 

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			procsound1.start()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			waitsound1.start()
			if ultrasonic == 'true':
				distcalc1.start()
			elif ultrasonic == 'false':
				pass
			cv2.imwrite(img_path, frame)
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			# Cam Cleanup
			cv2.destroyAllWindows()
			break

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		Analyzing_Snapshot = path+'/newimg/Analyzing_This_Scene.jpg'
		beep(338,333)
		if platform.system() == 'Windows':
			os.system(Analyzing_Snapshot)
		elif platform.system() != 'Windows':
			os.system('firefox '+Analyzing_Snapshot)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		# Microsoft CIS Vision API Processing
		image_path = img_path
		image_data = open(image_path, "rb").read()
		headers    = {'Ocp-Apim-Subscription-Key': onlinescenedescriptor_subscription_key, 'Content-Type': 'application/octet-stream'}
		params     = {'visualFeatures': 'Categories,Description,Color'}

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		response = requests.post(onlinescenedescriptor_analyze_url, headers=headers, params=params, data=image_data)
		response.raise_for_status()
		analysis = response.json()
		image_caption = analysis["description"]["captions"][0]["text"].capitalize()
		waitsnd1.set()
		beep(555,333)
		print('\n   '+image_caption+'   \n')
		say(image_caption)
		if ultrasonic == 'true':
			dc1.set()
		elif ultrasonic == 'false':
			pass

		if platform.system() == 'Windows':
			os.system('taskkill /f /im firefox.exe /t')
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('kill -9 $(ps -x | grep firefox)')
			os.system('clear')

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return


		## Offline Scene Descriptor
		gc.collect()
		i = -1
		while 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			frame = vs.read()
			#frame = imutils.resize(frame, width=240,height=180)
			frame = imutils.resize(frame, width=1600,height=1200)
			img_path = 'newimg/Analyzing_This_Scene.jpg'
			beep(333,666)
			cv2.imshow(window_name, frame)
			cv2.waitKey(interframe_wait_ms)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			procsound2.start()
			waitsound2.start()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			cv2.imwrite(img_path, frame)
			# Cam Cleanup
			cv2.destroyAllWindows()
			if ultrasonic == 'true':
				distcalc2.start()
			elif ultrasonic == 'false':
				pass
			break

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if platform.system() == 'Windows':
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('clear')

		image = cv2.imread(img_path)
		image = imutils.resize(image, width=240,height=180)
		Analyzing_Snapshot = path+'/newimg/Analyzing_This_Scene.jpg'
		beep(338,333)
		if platform.system() == 'Windows':
			os.system(Analyzing_Snapshot)
		elif platform.system() != 'Windows':
			os.system('firefox '+Analyzing_Snapshot)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## ML Model Processing
		blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
		net1.setInput(blob)
		score1 = net1.forward()
		classIds = np.argmax(score1[0], axis=0)
		uniqueclassids = np.unique(classIds)
		noofobjs = len(uniqueclassids)
		noteableobjs = float(noofobjs*0.40)
		noteableobjs = round(noteableobjs,0)
		noteableobjs = int(noteableobjs)
		num = 0
		beep(538,222)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if noteableobjs <= 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			waitsnd2.set()
			print('\n   '+str(noteableobjs)+' object ...   \n')
			say(str(noteableobjs)+' object!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc2.set()
			elif ultrasonic == 'false':
				pass

		else:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			waitsnd2.set()
			print('\n   '+str(noteableobjs)+' objects ...   \n')
			say(str(noteableobjs)+' objects!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc2.set()
			elif ultrasonic == 'false':
				pass

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		beep(338,222)
		if noteableobjs == 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			print('\n   Analyzing ...   \n')
			say(' Analyzing!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')

		else:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if i == 0:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				print('\n   From Top to Bottom, Left to Right:   \n')
				say(' From top to bottom, left to right!  ')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

			elif i == 1:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				time.sleep(0.01)
				print('\n   From Top to Bottom, Left to Right:   \n')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			elif i == 2:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				print('\n   From Top to Bottom, Left to Right:   \n')
				say(' Still top to bottom, left to right!  ')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			elif i > 2:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				time.sleep(0.01)
				print('\n   From top to bottom, left to right:   \n')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			topobjs = -1
			reslist = []

			for uniqueclassidsperitem in uniqueclassids:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				topobjs += 1
				if topobjs > (noteableobjs-1):

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							waitsnd3.set()
							dc1.set()
							dc2.set()
							dc3.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					pass

				else:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							waitsnd3.set()
							dc1.set()
							dc2.set()
							dc3.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					#num += 1
					res = LABELS1[uniqueclassidsperitem-1]
					res = str(res)
					res = res.strip()
					if res == 'person':
						reslist.append(res)
						pass
					else:
						reslist.append(res)
						pass

			def sayres():
				num = 0
				for resitem in reslist:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							waitsnd3.set()
							dc1.set()
							dc2.set()
							dc3.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					num += 1
					freq = 438
					dur = 222
					beep(438,222)
					print('\n   '+resitem+'!   \n')
					say(resitem+'!  ')
					time.sleep(0.3)

			sayres()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

		if platform.system() == 'Windows':
			os.system('taskkill /f /im firefox.exe /t')
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('kill -9 $(ps -x | grep firefox)')
			os.system('clear')


		# Person Detector
		gc.collect()
		while 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			frame = vs.read()
			frame = imutils.resize(frame, width=1600,height=1200)
			img_path = 'newimg/Analyzing_This_Scene.jpg'
			beep(333,333)
			cv2.imshow(window_name, frame)
			cv2.waitKey(interframe_wait_ms)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			procsound3.start()
			waitsound3.start()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				distcalc3.start()
			elif ultrasonic == 'false':
				pass

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			cv2.imwrite(img_path, frame)
			# Cam Cleanup
			cv2.destroyAllWindows()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			break

		vs.stop()

		image = cv2.imread(img_path)
		#clone = image.copy()
		(H, W) = image.shape[:2]

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		Analyzing_Snapshot = path+'/newimg/Analyzing_This_Scene.jpg'
		beep(338,333)
		if platform.system() == 'Windows':
			os.system(Analyzing_Snapshot)
		elif platform.system() != 'Windows':
			os.system('firefox '+Analyzing_Snapshot)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## DL Model Processing
		blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
		net.setInput(blob)
		(boxes, masks) = net.forward(["detection_out_final", "detection_masks"])

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if len(boxes) == 0:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			numpers = 'Nobody\'s in front of you! '
			numobjs = 'No object!  '
			waitsnd3.set()
			beep(538,333)
			say(numpers+numobjs)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc3.set()
			elif ultrasonic == 'false':
				pass

		elif len(boxes) > 0:
			finlist = []
			yyy = 0
			zzz = 0

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					waitsnd3.set()
					dc1.set()
					dc2.set()
					dc3.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			for i in range(0, 	boxes.shape[2]):

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				classID = int(boxes[0, 0, i, 1])
				confidence = boxes[0, 0, i, 2]

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						waitsnd3.set()
						dc1.set()
						dc2.set()
						dc3.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				if confidence > 0.5:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							waitsnd3.set()
							dc1.set()
							dc2.set()
							dc3.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					box = boxes[0, 0, i, 3:7] * np.array([W, H, W, H])
					(startX, startY, endX, endY) = box.astype("int")
					boxW = endX - startX
					boxH = endY - startY
					x = (startX + endX) / 2
					y = (startY + endY) / 2.50

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							waitsnd3.set()
							dc1.set()
							dc2.set()
							dc3.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					if x <= 320 and y <= 240:
						z = '1 '
						zz = ' Left side. Ten o\'clock.  '
					elif x >= 321 and x <= 1280 and y <= 240:
						z = '4 '
						zz = ' Center. Twelve o\'clock.  '
					elif x >= 1281 and y <= 240:
						z = '7 '
						zz = ' Right side. One o\'clock.  '
					elif x <= 320 and y >= 241 and y <= 960:
						z = '2 '
						zz = ' Left side. Nine o\'clock.  '
					elif x >= 321 and x <= 1280 and y >= 241 and y <= 960:
						z = '5 '
						zz = ' Dead center.  '
					elif x >= 1281 and y >= 241 and y <= 960:
						z = '8 '
						zz = ' Right side. Three o\'clock.  '
					elif x <= 320 and y >= 961:
						z = '3 '
						zz = ' Left side. Seven o\'clock.  '
					elif x >= 321 and x <= 1280 and y >= 961:
						z = '6 '
						zz = ' Center. Six o\'clock.  '
					elif x >= 1281 and y >= 961:
						z = '9 '
						zz = ' Right side. Five o\'clock.  '

					text = LABELS[classID]
					finres = text
					finres = str(finres)
					finres = finres.strip()

					#iii = -1
					if finres == 'person':
						zzz += 1

						# extract the ROI of the image
						roi = image[startY:endY, startX:endX]
						roi2 = roi
						image2 = roi2
						(h, w) = image2.shape[:2]

						## Check BSTATUS
						if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
							try:
								waitsnd1.set()
								waitsnd2.set()
								waitsnd3.set()
								dc1.set()
								dc2.set()
								dc3.set()
								cv2.destroyAllWindows()
								vs.stop()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return

						## DL Model Processing
						blob = cv2.dnn.blobFromImage(cv2.resize(image2, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
						face_net.setInput(blob)
						detections = face_net.forward()
						detectf = len(detections)

						## Check BSTATUS
						if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
							try:
								waitsnd1.set()
								waitsnd2.set()
								waitsnd3.set()
								dc1.set()
								dc2.set()
								dc3.set()
								cv2.destroyAllWindows()
								vs.stop()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return

						if detectf == 0:
							agegenderfin = 'not sure of age and gender'
							agegenderfin = agegenderfin.strip()
							finres = finres+', '+agegenderfin
							finlist.append(z+finres+'. '+zz)
						elif detectf > 0:
							#for i in range(0, detections.shape[2]):
							confidence = detections[0, 0, i, 2]

							if confidence > 0.5:
								blob = cv2.dnn.blobFromImage(image2, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

								#Predict Gender
								gender_net.setInput(blob)
								gender_preds = gender_net.forward()
								gender = gender_list[gender_preds[0].argmax()]
								gender = str(gender)
								genderfin = gender.strip()

								#Predict Age
								age_net.setInput(blob)
								age_preds = age_net.forward()
								age = age_list[age_preds[0].argmax()]
								age = str(age)
								agefin = age.strip()
								agegenderfin = agefin+' '+genderfin
								agegenderfin = str(agegenderfin)
								agegenderfin = agegenderfin.strip()

								finres = finres+', '+agegenderfin
								finlist.append(z+finres+'. '+zz)

							else:
								agegenderfin = 'Unsure of age and gender.  '
								finres = finres+', '+agegenderfin
								finlist.append(z+finres+'. '+zz)

					elif finres != 'person':
						yyy += 1

						finlist.append(z+finres+'. '+zz)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		def isayres():
			if zzz < 1 and yyy < 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = 'No object detected. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz < 1 and yyy == 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = str(yyy)+' Object. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz < 1 and yyy > 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = str(yyy)+' Objects. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy < 1:
				numpers = str(zzz)+' Person. '
				numobjs = 'No Object. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy == 1:
				numpers = str(zzz)+' Person. '
				numobjs = str(yyy)+' Object. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy > 1:
				numpers = str(zzz)+' Person. '
				numobjs = str(yyy)+' Objects. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy < 1:
				numpers = str(zzz)+' Persons. '
				numobjs = 'No object detected. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy == 1:
				numpers = str(zzz)+' Persons. '
				numobjs = str(yyy)+' Object. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy > 1:
				numpers = str(zzz)+' Persons. '
				numobjs = str(yyy)+' Objects. '
				waitsnd3.set()
				if ultrasonic == 'true':
					dc3.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)

			prlist = sorted(finlist)
			for persandobjs in prlist:
				persandobjs = str(persandobjs)
				persandobjs = persandobjs.strip()
				persandobjs = persandobjs.replace('1 ', '')
				persandobjs = persandobjs.replace('2 ', '')
				persandobjs = persandobjs.replace('3 ', '')
				persandobjs = persandobjs.replace('4 ', '')
				persandobjs = persandobjs.replace('5 ', '')
				persandobjs = persandobjs.replace('6 ', '')
				persandobjs = persandobjs.replace('7 ', '')
				persandobjs = persandobjs.replace('8 ', '')
				persandobjs = persandobjs.replace('9 ', '')
				beep(538,333)
				print('\n   '+persandobjs+'   \n')
				say(persandobjs)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		isayres()

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		try:
			cv2.destroyAllWindows()
			vs.stop()
			waitsnd1.set()
			waitsnd2.set()
			waitsnd3.set()
			dc1.set()
			dc2.set()
			dc3.set()
			if platform.system() == 'Windows':
				os.system('taskkill /f /im firefox.exe /t')
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('kill -9 $(ps -x | grep firefox)')
				os.system('clear')
		except Exception as e:
			pass

	return


# Parent Thread of Offline Navigation Mode
def offlinenavigationmode():
	## Initialization
	title("  VIsION Navigation Mode  ")
	titletext = 'Navigation Mode'

	intromsg(titletext)
	gc.collect()

	vs = WebcamVideoStream(src=0).start()
	window_name = "VIsION_CAM"
	interframe_wait_ms = 1000
	cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

	maintimelimit = time.time() + 300
	while not time.time() > maintimelimit:
		gc.collect()

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## Collection of Daemonic Threads

		#  wait sound
		def waitsound1(waitsnd1,t):
			time.sleep(0.1)
			speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
			psndcounter = -1
			psndcounter2 = -1
			say(random.choice(speakthisnow))
			print('\n   '+random.choice(speakthisnow)+'   \n')
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			while not waitsnd1.is_set():
				psndcounter += 25
				psndcounter2 += 0.01
				freq = 338 + psndcounter 
				dur = 66
				beep(freq,dur)
				time.sleep(0.2-psndcounter2)
				event_is_set = waitsnd1.wait(t)
				if event_is_set:
					break
			return
	
		waitsnd1 = threading.Event()
		waitsound1 = threading.Thread(target=waitsound1,daemon=True,args=(waitsnd1, 0.03), )
	
		def waitsound2(waitsnd2,t):
			time.sleep(0.1)
			speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
			psndcounter = -1
			psndcounter2 = -1
			say(random.choice(speakthisnow))
			print('\n   '+random.choice(speakthisnow)+'   \n')
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			while not waitsnd2.is_set():
				psndcounter += 25
				psndcounter2 += 0.01
				freq = 338 + psndcounter 
				dur = 66
				beep(freq,dur)
				time.sleep(0.2-psndcounter2)
				event_is_set = waitsnd2.wait(t)
				if event_is_set:
					break
			return
	
		waitsnd2 = threading.Event()
		waitsound2 = threading.Thread(target=waitsound2,daemon=True,args=(waitsnd2, 0.03), )
	
		## Distance Estimation Engine
		def distcalc1(dc1,t):
			try:
				iss.i2c.write(0xE0, 0x01, [0x06])
				iss.i2c.write(0xE0, 0x02, [0xFF])
				distcalctimelimit = time.time() + 9
				while time.time() < distcalctimelimit:
					event_is_set = dc1.wait(t)
					if event_is_set:
						iss.i2c.write(0xE0, 0x00, [0x50])
						time.sleep(0.067)
						data = iss.i2c.read(0xE0, 0x03, 1)
						data = data[0]
						data = int(data)
						if data > 0 and data < 24:
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' inches! ')
							break
						elif data > 24 and 	data < 108:
							data = int(data) / int(12)
							data = round(data,1)
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' feet! ')
							break
						elif data > 108:
							beep(338,222)
							say('Distance is beyond nine feet! ')
							break
						elif data == 0:
							beep(538,111)
							time.sleep(0.067)
					else:
						time.sleep(0.01)
				return
			except Exception as e:
				print(e)
	
		dc1 = threading.Event()
		distcalc1 = threading.Thread(target=distcalc1,daemon=True,args=(dc1, 0.03), )
	
		def distcalc2(dc2,t):
			try:
				iss.i2c.write(0xE0, 0x01, [0x06])
				iss.i2c.write(0xE0, 0x02, [0xFF])
				distcalctimelimit = time.time() + 9
				while time.time() < distcalctimelimit:
					event_is_set = dc2.wait(t)
					if event_is_set:
						iss.i2c.write(0xE0, 0x00, [0x50])
						time.sleep(0.067)
						data = iss.i2c.read(0xE0, 0x03, 1)
						data = data[0]
						data = int(data)
						if data > 0 and data < 24:
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' inches! ')
							break
						elif data > 24 and 	data < 108:
							data = int(data) / int(12)
							data = round(data,1)
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' feet! ')
							break
						elif data > 108:
							beep(338,222)
							say('Distance is beyond nine feet! ')
							break
						elif data == 0:
							beep(538,111)
							time.sleep(0.067)
					else:
						time.sleep(0.01)
				return
			except Exception as e:
				print(e)
	
		dc2 = threading.Event()
		distcalc2 = threading.Thread(target=distcalc2,daemon=True,args=(dc2, 0.03), )
	
		## Processing Sound
		def procsound1():
			try:
				# Define Stream Chunk
				chunk = 1024
				# Open WAV
				f = wave.open(path+'/takesnapshot.wav', "rb")
				# Instantiate PyAudio
				p = pyaudio.PyAudio()  
				# Open Stream
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
				# Read Data from Stream
				data = f.readframes(chunk)  
				# Play Stream
				while data:
					stream.write(data)
					data = f.readframes(chunk)
				# Stop Stream
				stream.stop_stream()
				stream.close()
				# Close PyAudio
				p.terminate()
				gc.collect()
			except Exception as e:
				print(e)
	
		procsound1 = threading.Thread(target=procsound1,daemon=True)
	
		def procsound2():
			try:
				# Define Stream Chunk
				chunk = 1024
				# Open WAV
				f = wave.open(path+'/takesnapshot.wav', "rb")
				# Instantiate PyAudio
				p = pyaudio.PyAudio()  
				# Open Stream
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
				# Read Data from Stream
				data = f.readframes(chunk)  
				# Play Stream
				while data:
					stream.write(data)
					data = f.readframes(chunk)
				# Stop Stream
				stream.stop_stream()
				stream.close()
				# Close PyAudio
				p.terminate()
				gc.collect()
			except Exception as e:
				print(e)
	
		procsound2 = threading.Thread(target=procsound2,daemon=True)
	
		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		rcounter = -1
		gc.collect()


		## Offline Scene Descriptor
		gc.collect()
		i = -1
		while 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			frame = vs.read()
			#frame = imutils.resize(frame, width=240,height=180)
			frame = imutils.resize(frame, width=1600,height=1200)
			img_path = 'newimg/Analyzing_This_Scene.jpg'
			beep(333,666)
			cv2.imshow(window_name, frame)
			cv2.waitKey(interframe_wait_ms)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			procsound1.start()
			waitsound1.start()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			cv2.imwrite(img_path, frame)
			# Cam Cleanup
			cv2.destroyAllWindows()
			if ultrasonic == 'true':
				distcalc1.start()
			elif ultrasonic == 'false':
				pass
			break

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if platform.system() == 'Windows':
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('clear')

		image = cv2.imread(img_path)
		image = imutils.resize(image, width=240,height=180)
		Analyzing_Snapshot = path+'/newimg/Analyzing_This_Scene.jpg'
		beep(338,333)
		if platform.system() == 'Windows':
			os.system(Analyzing_Snapshot)
		elif platform.system() != 'Windows':
			os.system('firefox '+Analyzing_Snapshot)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## ML Model Processing
		blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
		net1.setInput(blob)
		score1 = net1.forward()
		classIds = np.argmax(score1[0], axis=0)
		uniqueclassids = np.unique(classIds)
		noofobjs = len(uniqueclassids)
		noteableobjs = float(noofobjs*0.40)
		noteableobjs = round(noteableobjs,0)
		noteableobjs = int(noteableobjs)
		num = 0
		beep(538,222)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if noteableobjs <= 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			waitsnd1.set()
			print('\n   '+str(noteableobjs)+' object ...   \n')
			say(str(noteableobjs)+' object!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc1.set()
			elif ultrasonic == 'false':
				pass

		else:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			waitsnd1.set()
			print('\n   '+str(noteableobjs)+' objects ...   \n')
			say(str(noteableobjs)+' objects!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc1.set()
			elif ultrasonic == 'false':
				pass

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		beep(338,222)
		if noteableobjs == 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			print('\n   Analyzing ...   \n')
			say(' Analyzing!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')

		else:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if i == 0:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				print('\n   From Top to Bottom, Left to Right:   \n')
				say(' From top to bottom, left to right!  ')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

			elif i == 1:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				time.sleep(0.01)
				print('\n   From Top to Bottom, Left to Right:   \n')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			elif i == 2:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				print('\n   From Top to Bottom, Left to Right:   \n')
				say(' Still top to bottom, left to right!  ')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			elif i > 2:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				time.sleep(0.01)
				print('\n   From top to bottom, left to right:   \n')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			topobjs = -1
			reslist = []

			for uniqueclassidsperitem in uniqueclassids:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				topobjs += 1
				if topobjs > (noteableobjs-1):

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					pass

				else:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					#num += 1
					res = LABELS1[uniqueclassidsperitem-1]
					res = str(res)
					res = res.strip()
					if res == 'person':
						reslist.append(res)
						pass
					else:
						reslist.append(res)
						pass

			def sayres():
				num = 0
				for resitem in reslist:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					num += 1
					freq = 438
					dur = 222
					beep(438,222)
					print('\n   '+resitem+'!   \n')
					say(resitem+'!  ')
					time.sleep(0.3)

			sayres()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

		if platform.system() == 'Windows':
			os.system('taskkill /f /im firefox.exe /t')
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('kill -9 $(ps -x | grep firefox)')
			os.system('clear')


		# Person Detector
		gc.collect()
		while 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			frame = vs.read()
			frame = imutils.resize(frame, width=1600,height=1200)
			img_path = 'newimg/Analyzing_This_Scene.jpg'
			beep(333,333)
			cv2.imshow(window_name, frame)
			cv2.waitKey(interframe_wait_ms)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			procsound2.start()
			waitsound2.start()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				distcalc2.start()
			elif ultrasonic == 'false':
				pass

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			cv2.imwrite(img_path, frame)
			# Cam Cleanup
			cv2.destroyAllWindows()
			vs.stop()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			break

		vs.stop()

		image = cv2.imread(img_path)
		#clone = image.copy()
		(H, W) = image.shape[:2]

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		Analyzing_Snapshot = path+'/newimg/Analyzing_This_Scene.jpg'
		beep(338,333)
		if platform.system() == 'Windows':
			os.system(Analyzing_Snapshot)
		elif platform.system() != 'Windows':
			os.system('firefox '+Analyzing_Snapshot)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## DL Model Processing
		blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
		net.setInput(blob)
		(boxes, masks) = net.forward(["detection_out_final", "detection_masks"])

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if len(boxes) == 0:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			numpers = 'Nobody\'s in front of you! '
			numobjs = 'No object!  '
			waitsnd2.set()
			beep(538,333)
			say(numpers+numobjs)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc2.set()
			elif ultrasonic == 'false':
				pass

		elif len(boxes) > 0:
			finlist = []
			yyy = 0
			zzz = 0

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					cv2.destroyAllWindows()
					vs.stop()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			for i in range(0, 	boxes.shape[2]):

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				classID = int(boxes[0, 0, i, 1])
				confidence = boxes[0, 0, i, 2]

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				if confidence > 0.5:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					box = boxes[0, 0, i, 3:7] * np.array([W, H, W, H])
					(startX, startY, endX, endY) = box.astype("int")
					boxW = endX - startX
					boxH = endY - startY
					x = (startX + endX) / 2
					y = (startY + endY) / 2.50

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					if x <= 320 and y <= 240:
						z = '1 '
						zz = ' Left side. Ten o\'clock.  '
					elif x >= 321 and x <= 1280 and y <= 240:
						z = '4 '
						zz = ' Center. Twelve o\'clock.  '
					elif x >= 1281 and y <= 240:
						z = '7 '
						zz = ' Right side. One o\'clock.  '
					elif x <= 320 and y >= 241 and y <= 960:
						z = '2 '
						zz = ' Left side. Nine o\'clock.  '
					elif x >= 321 and x <= 1280 and y >= 241 and y <= 960:
						z = '5 '
						zz = ' Dead center.  '
					elif x >= 1281 and y >= 241 and y <= 960:
						z = '8 '
						zz = ' Right side. Three o\'clock.  '
					elif x <= 320 and y >= 961:
						z = '3 '
						zz = ' Left side. Seven o\'clock.  '
					elif x >= 321 and x <= 1280 and y >= 961:
						z = '6 '
						zz = ' Center. Six o\'clock.  '
					elif x >= 1281 and y >= 961:
						z = '9 '
						zz = ' Right side. Five o\'clock.  '

					text = LABELS[classID]
					finres = text
					finres = str(finres)
					finres = finres.strip()

					#iii = -1
					if finres == 'person':
						zzz += 1

						# extract the ROI of the image
						roi = image[startY:endY, startX:endX]
						roi2 = roi
						image2 = roi2
						(h, w) = image2.shape[:2]

						## Check BSTATUS
						if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
							try:
								waitsnd1.set()
								waitsnd2.set()
								dc1.set()
								dc2.set()
								cv2.destroyAllWindows()
								vs.stop()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return

						## DL Model Processing
						blob = cv2.dnn.blobFromImage(cv2.resize(image2, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
						face_net.setInput(blob)
						detections = face_net.forward()
						detectf = len(detections)

						## Check BSTATUS
						if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
							try:
								waitsnd1.set()
								waitsnd2.set()
								dc1.set()
								dc2.set()
								cv2.destroyAllWindows()
								vs.stop()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return

						if detectf == 0:
							agegenderfin = 'not sure of age and gender'
							agegenderfin = agegenderfin.strip()
							finres = finres+', '+agegenderfin
							finlist.append(z+finres+'. '+zz)
						elif detectf > 0:
							#for i in range(0, detections.shape[2]):
							confidence = detections[0, 0, i, 2]

							if confidence > 0.5:
								blob = cv2.dnn.blobFromImage(image2, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

								#Predict Gender
								gender_net.setInput(blob)
								gender_preds = gender_net.forward()
								gender = gender_list[gender_preds[0].argmax()]
								gender = str(gender)
								genderfin = gender.strip()

								#Predict Age
								age_net.setInput(blob)
								age_preds = age_net.forward()
								age = age_list[age_preds[0].argmax()]
								age = str(age)
								agefin = age.strip()
								agegenderfin = agefin+' '+genderfin
								agegenderfin = str(agegenderfin)
								agegenderfin = agegenderfin.strip()

								finres = finres+', '+agegenderfin
								finlist.append(z+finres+'. '+zz)

							else:
								agegenderfin = 'Unsure of age and gender.  '
								finres = finres+', '+agegenderfin
								finlist.append(z+finres+'. '+zz)

					elif finres != 'person':
						yyy += 1

						finlist.append(z+finres+'. '+zz)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		def isayres():
			if zzz < 1 and yyy < 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = 'No object detected. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz < 1 and yyy == 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = str(yyy)+' Object. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz < 1 and yyy > 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = str(yyy)+' Objects. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy < 1:
				numpers = str(zzz)+' Person. '
				numobjs = 'No Object. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy == 1:
				numpers = str(zzz)+' Person. '
				numobjs = str(yyy)+' Object. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy > 1:
				numpers = str(zzz)+' Person. '
				numobjs = str(yyy)+' Objects. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy < 1:
				numpers = str(zzz)+' Persons. '
				numobjs = 'No object detected. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy == 1:
				numpers = str(zzz)+' Persons. '
				numobjs = str(yyy)+' Object. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy > 1:
				numpers = str(zzz)+' Persons. '
				numobjs = str(yyy)+' Objects. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)

			prlist = sorted(finlist)
			for persandobjs in prlist:
				persandobjs = str(persandobjs)
				persandobjs = persandobjs.strip()
				persandobjs = persandobjs.replace('1 ', '')
				persandobjs = persandobjs.replace('2 ', '')
				persandobjs = persandobjs.replace('3 ', '')
				persandobjs = persandobjs.replace('4 ', '')
				persandobjs = persandobjs.replace('5 ', '')
				persandobjs = persandobjs.replace('6 ', '')
				persandobjs = persandobjs.replace('7 ', '')
				persandobjs = persandobjs.replace('8 ', '')
				persandobjs = persandobjs.replace('9 ', '')
				beep(538,333)
				print('\n   '+persandobjs+'   \n')
				say(persandobjs)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		isayres()

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				cv2.destroyAllWindows()
				vs.stop()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		try:
			cv2.destroyAllWindows()
			vs.stop()
			waitsnd1.set()
			waitsnd2.set()
			dc1.set()
			dc2.set()
			if platform.system() == 'Windows':
				os.system('taskkill /f /im firefox.exe /t')
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('kill -9 $(ps -x | grep firefox)')
				os.system('clear')
		except Exception as e:
			pass

	return


# Parent Thread of Offline Navigation Mode
def offlinenavigationmode():
	## Initialization
	title("  VIsION Navigation Mode  ")
	titletext = 'Navigation Mode'

	intromsg(titletext)
	gc.collect()

	vs = WebcamVideoStream(src=0).start()
	window_name = "VIsION_CAM"
	interframe_wait_ms = 1000
	cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

	maintimelimit = time.time() + 300
	while not time.time() > maintimelimit:
		gc.collect()

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				waitsnd3.set()
				dc1.set()
				dc2.set()
				dc3.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## Collection of Daemonic Threads

		#  wait sound
		def waitsound1(waitsnd1,t):
			time.sleep(0.1)
			speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
			psndcounter = -1
			psndcounter2 = -1
			say(random.choice(speakthisnow))
			print('\n   '+random.choice(speakthisnow)+'   \n')
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			while not waitsnd1.is_set():
				psndcounter += 25
				psndcounter2 += 0.01
				freq = 338 + psndcounter 
				dur = 66
				beep(freq,dur)
				time.sleep(0.2-psndcounter2)
				event_is_set = waitsnd1.wait(t)
				if event_is_set:
					break
			return
	
		waitsnd1 = threading.Event()
		waitsound1 = threading.Thread(target=waitsound1,daemon=True,args=(waitsnd1, 0.03), )
	
		def waitsound2(waitsnd2,t):
			time.sleep(0.1)
			speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
			psndcounter = -1
			psndcounter2 = -1
			say(random.choice(speakthisnow))
			print('\n   '+random.choice(speakthisnow)+'   \n')
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			while not waitsnd2.is_set():
				psndcounter += 25
				psndcounter2 += 0.01
				freq = 338 + psndcounter 
				dur = 66
				beep(freq,dur)
				time.sleep(0.2-psndcounter2)
				event_is_set = waitsnd2.wait(t)
				if event_is_set:
					break
			return
	
		waitsnd2 = threading.Event()
		waitsound2 = threading.Thread(target=waitsound2,daemon=True,args=(waitsnd2, 0.03), )
	
			## Distance Estimation Engine
		def distcalc1(dc1,t):
			try:
				iss.i2c.write(0xE0, 0x01, [0x06])
				iss.i2c.write(0xE0, 0x02, [0xFF])
				distcalctimelimit = time.time() + 9
				while time.time() < distcalctimelimit:
					event_is_set = dc1.wait(t)
					if event_is_set:
						iss.i2c.write(0xE0, 0x00, [0x50])
						time.sleep(0.067)
						data = iss.i2c.read(0xE0, 0x03, 1)
						data = data[0]
						data = int(data)
						if data > 0 and data < 24:
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' inches! ')
							break
						elif data > 24 and 	data < 108:
							data = int(data) / int(12)
							data = round(data,1)
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' feet! ')
							break
						elif data > 108:
							beep(338,222)
							say('Distance is beyond nine feet! ')
							break
						elif data == 0:
							beep(538,111)
							time.sleep(0.067)
					else:
						time.sleep(0.01)
				return
			except Exception as e:
				print(e)
	
		dc1 = threading.Event()
		distcalc1 = threading.Thread(target=distcalc1,daemon=True,args=(dc1, 0.03), )
	
		def distcalc2(dc2,t):
			try:
				iss.i2c.write(0xE0, 0x01, [0x06])
				iss.i2c.write(0xE0, 0x02, [0xFF])
				distcalctimelimit = time.time() + 9
				while time.time() < distcalctimelimit:
					event_is_set = dc2.wait(t)
					if event_is_set:
						iss.i2c.write(0xE0, 0x00, [0x50])
						time.sleep(0.067)
						data = iss.i2c.read(0xE0, 0x03, 1)
						data = data[0]
						data = int(data)
						if data > 0 and data < 24:
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' inches! ')
							break
						elif data > 24 and 	data < 108:
							data = int(data) / int(12)
							data = round(data,1)
							data = str(data)
							beep(338,222)
							say('Distance is '+data+' feet! ')
							break
						elif data > 108:
							beep(338,222)
							say('Distance is beyond nine feet! ')
							break
						elif data == 0:
							beep(538,111)
							time.sleep(0.067)
					else:
						time.sleep(0.01)
				return
			except Exception as e:
				print(e)
	
		dc2 = threading.Event()
		distcalc2 = threading.Thread(target=distcalc2,daemon=True,args=(dc2, 0.03), )
		
		## Processing Sound
		def procsound1():
			try:
				# Define Stream Chunk
				chunk = 1024
				# Open WAV
				f = wave.open(path+'/takesnapshot.wav', "rb")
				# Instantiate PyAudio
				p = pyaudio.PyAudio()  
				# Open Stream
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
				# Read Data from Stream
				data = f.readframes(chunk)  
				# Play Stream
				while data:
					stream.write(data)
					data = f.readframes(chunk)
				# Stop Stream
				stream.stop_stream()
				stream.close()
				# Close PyAudio
				p.terminate()
				gc.collect()
			except Exception as e:
				print(e)
	
		procsound1 = threading.Thread(target=procsound1,daemon=True)
	
		def procsound2():
			try:
				# Define Stream Chunk
				chunk = 1024
				# Open WAV
				f = wave.open(path+'/takesnapshot.wav', "rb")
				# Instantiate PyAudio
				p = pyaudio.PyAudio()  
				# Open Stream
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
				# Read Data from Stream
				data = f.readframes(chunk)  
				# Play Stream
				while data:
					stream.write(data)
					data = f.readframes(chunk)
				# Stop Stream
				stream.stop_stream()
				stream.close()
				# Close PyAudio
				p.terminate()
				gc.collect()
			except Exception as e:
				print(e)
	
		procsound2 = threading.Thread(target=procsound2,daemon=True)
	
		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		rcounter = -1
		gc.collect()

		## Offline Scene Descriptor
		gc.collect()
		i = -1
		while 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			frame = vs.read()
			#frame = imutils.resize(frame, width=240,height=180)
			frame = imutils.resize(frame, width=1600,height=1200)
			img_path = 'newimg/Analyzing_This_Scene.jpg'
			beep(333,666)
			cv2.imshow(window_name, frame)
			cv2.waitKey(interframe_wait_ms)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			procsound1.start()
			waitsound1.start()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			cv2.imwrite(img_path, frame)
			# Cam Cleanup
			cv2.destroyAllWindows()
			if ultrasonic == 'true':
				distcalc1.start()
			elif ultrasonic == 'false':
				pass
			break

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if platform.system() == 'Windows':
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('clear')

		image = cv2.imread(img_path)
		image = imutils.resize(image, width=240,height=180)
		Analyzing_Snapshot = path+'/newimg/Analyzing_This_Scene.jpg'
		beep(338,333)
		if platform.system() == 'Windows':
			os.system(Analyzing_Snapshot)
		elif platform.system() != 'Windows':
			os.system('firefox '+Analyzing_Snapshot)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## ML Model Processing
		blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
		net1.setInput(blob)
		score1 = net1.forward()
		classIds = np.argmax(score1[0], axis=0)
		uniqueclassids = np.unique(classIds)
		noofobjs = len(uniqueclassids)
		noteableobjs = float(noofobjs*0.40)
		noteableobjs = round(noteableobjs,0)
		noteableobjs = int(noteableobjs)
		num = 0
		beep(538,222)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if noteableobjs <= 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			waitsnd1.set()
			print('\n   '+str(noteableobjs)+' object ...   \n')
			say(str(noteableobjs)+' object!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc1.set()
			elif ultrasonic == 'false':
				pass

		else:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			waitsnd1.set()
			print('\n   '+str(noteableobjs)+' objects ...   \n')
			say(str(noteableobjs)+' objects!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc1.set()
			elif ultrasonic == 'false':
				pass

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		beep(338,222)
		if noteableobjs == 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			print('\n   Analyzing ...   \n')
			say(' Analyzing!  ')

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')

		else:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if i == 0:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				print('\n   From Top to Bottom, Left to Right:   \n')
				say(' From top to bottom, left to right!  ')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

			elif i == 1:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				time.sleep(0.01)
				print('\n   From Top to Bottom, Left to Right:   \n')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			elif i == 2:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				print('\n   From Top to Bottom, Left to Right:   \n')
				say(' Still top to bottom, left to right!  ')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			elif i > 2:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				time.sleep(0.01)
				print('\n   From top to bottom, left to right:   \n')

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			topobjs = -1
			reslist = []

			for uniqueclassidsperitem in uniqueclassids:

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				topobjs += 1
				if topobjs > (noteableobjs-1):

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					pass

				else:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					#num += 1
					res = LABELS1[uniqueclassidsperitem-1]
					res = str(res)
					res = res.strip()
					if res == 'person':
						reslist.append(res)
						pass
					else:
						reslist.append(res)
						pass

			def sayres():
				num = 0
				for resitem in reslist:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					num += 1
					freq = 438
					dur = 222
					beep(438,222)
					print('\n   '+resitem+'!   \n')
					say(resitem+'!  ')
					time.sleep(0.3)

			sayres()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

		if platform.system() == 'Windows':
			os.system('taskkill /f /im firefox.exe /t')
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('kill -9 $(ps -x | grep firefox)')
			os.system('clear')


		# Person Detector
		gc.collect()
		while 1:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			frame = vs.read()
			frame = imutils.resize(frame, width=1600,height=1200)
			img_path = 'newimg/Analyzing_This_Scene.jpg'
			beep(333,333)
			cv2.imshow(window_name, frame)
			cv2.waitKey(interframe_wait_ms)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			procsound2.start()
			waitsound2.start()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				distcalc2.start()
			elif ultrasonic == 'false':
				pass

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			cv2.imwrite(img_path, frame)
			# Cam Cleanup
			cv2.destroyAllWindows()

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			break

		vs.stop()

		image = cv2.imread(img_path)
		#clone = image.copy()
		(H, W) = image.shape[:2]

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		Analyzing_Snapshot = path+'/newimg/Analyzing_This_Scene.jpg'
		beep(338,333)
		if platform.system() == 'Windows':
			os.system(Analyzing_Snapshot)
		elif platform.system() != 'Windows':
			os.system('firefox '+Analyzing_Snapshot)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		## DL Model Processing
		blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
		net.setInput(blob)
		(boxes, masks) = net.forward(["detection_out_final", "detection_masks"])

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		if len(boxes) == 0:

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			numpers = 'Nobody\'s in front of you! '
			numobjs = 'No object!  '
			waitsnd2.set()
			beep(538,333)
			say(numpers+numobjs)

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			if ultrasonic == 'true':
				dc2.set()
			elif ultrasonic == 'false':
				pass

		elif len(boxes) > 0:
			finlist = []
			yyy = 0
			zzz = 0

			## Check BSTATUS
			if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
				try:
					waitsnd1.set()
					waitsnd2.set()
					dc1.set()
					dc2.set()
					if platform.system() == 'Windows':
						os.system('taskkill /f /im firefox.exe /t')
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('kill -9 $(ps -x | grep firefox)')
						os.system('clear')
					deactivatesound(titletext)
					return
				except Exception as e:
					deactivatesound(titletext)
					return

			for i in range(0, 	boxes.shape[2]):

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				classID = int(boxes[0, 0, i, 1])
				confidence = boxes[0, 0, i, 2]

				## Check BSTATUS
				if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
					try:
						waitsnd1.set()
						waitsnd2.set()
						dc1.set()
						dc2.set()
						if platform.system() == 'Windows':
							os.system('taskkill /f /im firefox.exe /t')
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('kill -9 $(ps -x | grep firefox)')
							os.system('clear')
						deactivatesound(titletext)
						return
					except Exception as e:
						deactivatesound(titletext)
						return

				if confidence > 0.5:

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					box = boxes[0, 0, i, 3:7] * np.array([W, H, W, H])
					(startX, startY, endX, endY) = box.astype("int")
					boxW = endX - startX
					boxH = endY - startY
					x = (startX + endX) / 2
					y = (startY + endY) / 2.50

					## Check BSTATUS
					if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							dc1.set()
							dc2.set()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							deactivatesound(titletext)
							return

					if x <= 320 and y <= 240:
						z = '1 '
						zz = ' Left side. Ten o\'clock.  '
					elif x >= 321 and x <= 1280 and y <= 240:
						z = '4 '
						zz = ' Center. Twelve o\'clock.  '
					elif x >= 1281 and y <= 240:
						z = '7 '
						zz = ' Right side. One o\'clock.  '
					elif x <= 320 and y >= 241 and y <= 960:
						z = '2 '
						zz = ' Left side. Nine o\'clock.  '
					elif x >= 321 and x <= 1280 and y >= 241 and y <= 960:
						z = '5 '
						zz = ' Dead center.  '
					elif x >= 1281 and y >= 241 and y <= 960:
						z = '8 '
						zz = ' Right side. Three o\'clock.  '
					elif x <= 320 and y >= 961:
						z = '3 '
						zz = ' Left side. Seven o\'clock.  '
					elif x >= 321 and x <= 1280 and y >= 961:
						z = '6 '
						zz = ' Center. Six o\'clock.  '
					elif x >= 1281 and y >= 961:
						z = '9 '
						zz = ' Right side. Five o\'clock.  '

					text = LABELS[classID]
					finres = text
					finres = str(finres)
					finres = finres.strip()

					#iii = -1
					if finres == 'person':
						zzz += 1

						# extract the ROI of the image
						roi = image[startY:endY, startX:endX]
						roi2 = roi
						image2 = roi2
						(h, w) = image2.shape[:2]

						## Check BSTATUS
						if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
							try:
								waitsnd1.set()
								waitsnd2.set()
								dc1.set()
								dc2.set()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return

						## DL Model Processing
						blob = cv2.dnn.blobFromImage(cv2.resize(image2, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
						face_net.setInput(blob)
						detections = face_net.forward()
						detectf = len(detections)

						## Check BSTATUS
						if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
							try:
								waitsnd1.set()
								waitsnd2.set()
								dc1.set()
								dc2.set()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return

						if detectf == 0:
							agegenderfin = 'not sure of age and gender'
							agegenderfin = agegenderfin.strip()
							finres = finres+', '+agegenderfin
							finlist.append(z+finres+'. '+zz)
						elif detectf > 0:
							#for i in range(0, detections.shape[2]):
							confidence = detections[0, 0, i, 2]

							if confidence > 0.5:
								blob = cv2.dnn.blobFromImage(image2, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

								#Predict Gender
								gender_net.setInput(blob)
								gender_preds = gender_net.forward()
								gender = gender_list[gender_preds[0].argmax()]
								gender = str(gender)
								genderfin = gender.strip()

								#Predict Age
								age_net.setInput(blob)
								age_preds = age_net.forward()
								age = age_list[age_preds[0].argmax()]
								age = str(age)
								agefin = age.strip()
								agegenderfin = agefin+' '+genderfin
								agegenderfin = str(agegenderfin)
								agegenderfin = agegenderfin.strip()

								finres = finres+', '+agegenderfin
								finlist.append(z+finres+'. '+zz)

							else:
								agegenderfin = 'Unsure of age and gender.  '
								finres = finres+', '+agegenderfin
								finlist.append(z+finres+'. '+zz)

					elif finres != 'person':
						yyy += 1

						finlist.append(z+finres+'. '+zz)

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		def isayres():
			if zzz < 1 and yyy < 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = 'No object detected. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz < 1 and yyy == 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = str(yyy)+' Object. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz < 1 and yyy > 1:
				numpers = 'Nobody\'s in front of you. '
				numobjs = str(yyy)+' Objects. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy < 1:
				numpers = str(zzz)+' Person. '
				numobjs = 'No Object. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy == 1:
				numpers = str(zzz)+' Person. '
				numobjs = str(yyy)+' Object. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz == 1 and yyy > 1:
				numpers = str(zzz)+' Person. '
				numobjs = str(yyy)+' Objects. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy < 1:
				numpers = str(zzz)+' Persons. '
				numobjs = 'No object detected. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy == 1:
				numpers = str(zzz)+' Persons. '
				numobjs = str(yyy)+' Object. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)
			elif zzz > 1 and yyy > 1:
				numpers = str(zzz)+' Persons. '
				numobjs = str(yyy)+' Objects. '
				waitsnd2.set()
				if ultrasonic == 'true':
					dc2.set()
				elif ultrasonic == 'false':
					pass
				beep(538,333)
				print('\n   '+numpers+numobjs+'   \n')
				say(numpers+numobjs)
				time.sleep(0.3)

			prlist = sorted(finlist)
			for persandobjs in prlist:
				persandobjs = str(persandobjs)
				persandobjs = persandobjs.strip()
				persandobjs = persandobjs.replace('1 ', '')
				persandobjs = persandobjs.replace('2 ', '')
				persandobjs = persandobjs.replace('3 ', '')
				persandobjs = persandobjs.replace('4 ', '')
				persandobjs = persandobjs.replace('5 ', '')
				persandobjs = persandobjs.replace('6 ', '')
				persandobjs = persandobjs.replace('7 ', '')
				persandobjs = persandobjs.replace('8 ', '')
				persandobjs = persandobjs.replace('9 ', '')
				beep(538,333)
				print('\n   '+persandobjs+'   \n')
				say(persandobjs)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		isayres()

		## Check BSTATUS
		if keyboard.is_pressed('1') or keyboard.is_pressed('2'):
			try:
				waitsnd1.set()
				waitsnd2.set()
				dc1.set()
				dc2.set()
				if platform.system() == 'Windows':
					os.system('taskkill /f /im firefox.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('kill -9 $(ps -x | grep firefox)')
					os.system('clear')
				deactivatesound(titletext)
				return
			except Exception as e:
				deactivatesound(titletext)
				return

		try:
			cv2.destroyAllWindows()
			vs.stop()
			waitsnd1.set()
			waitsnd2.set()
			dc1.set()
			dc2.set()
			if platform.system() == 'Windows':
				os.system('taskkill /f /im firefox.exe /t')
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('kill -9 $(ps -x | grep firefox)')
				os.system('clear')
		except Exception as e:
			pass

	return


# Parent Thread of Online OCR Mode
def onlineocr():
				title("  VIsION OCR Mode  ")
				titletext = 'OCR Mode'

				path = os.path.dirname(os.path.realpath(__file__))
				cleanup()
				intromsg(titletext)
				gc.collect()

				vs = WebcamVideoStream(src=0).start()
				window_name = "VIsION_CAM"
				interframe_wait_ms = 800
				cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
				cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

				## Collection of Daemonic Threads

				#  wait sound1
				def waitsound1(waitsnd1,t):
					time.sleep(3)
					beep(338,222)
					print('\n   Quick Press to Take Snapshot ...   ')
					say('Quick press to take snapshot! ')
					beep(338,222)
					print('\n   Hold Press to Deactivate ...   ')
					say('Hold press to deactivate! ')
					beep(338,222)
					print('\n   Or Leave Idle to Auto Deactivate ...   ')
					say('Or, leave idle to auto deactivate! ')

					while not waitsnd1.is_set():
						event_is_set = waitsnd1.wait(t)
						if event_is_set:
							return
						else:
							time.sleep(7)
							beep(338,222)
							say('Waiting for keypress. ')
					return

				waitsnd1 = threading.Event()
				waitsound1 = threading.Thread(target=waitsound1,daemon=True,args=(waitsnd1, 0.03), )

				#  wait sound2
				def waitsound2(waitsnd2,t):
					time.sleep(0.1)
					speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
					psndcounter = -1
					psndcounter2 = -1
					say(random.choice(speakthisnow))
					print('\n   '+random.choice(speakthisnow)+'   \n')
					if platform.system() == 'Windows':
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('clear')
					while not waitsnd2.is_set():
						psndcounter += 25
						psndcounter2 += 0.01
						freq = 338 + psndcounter 
						dur = 66
						beep(freq,dur)
						time.sleep(0.2-psndcounter2)
						event_is_set = waitsnd2.wait(t)
						if event_is_set:
							break
					return

				waitsnd2 = threading.Event()
				waitsound2 = threading.Thread(target=waitsound2,daemon=True,args=(waitsnd2, 0.03), )

				#  wait sound3
				def waitsound3(waitsnd3,t):
					time.sleep(0.1)
					speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
					psndcounter = -1
					psndcounter2 = -1
					say(random.choice(speakthisnow))
					print('\n   '+random.choice(speakthisnow)+'   \n')
					if platform.system() == 'Windows':
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('clear')
					while not waitsnd3.is_set():
						psndcounter += 25
						psndcounter2 += 0.01
						freq = 338 + psndcounter 
						dur = 66
						beep(freq,dur)
						time.sleep(0.2-psndcounter2)
						event_is_set = waitsnd3.wait(t)
						if event_is_set:
							break
					return

				waitsnd3 = threading.Event()
				waitsound3 = threading.Thread(target=waitsound3,daemon=True,args=(waitsnd3, 0.03), )


				# Processing Sound
				def procsound():
					try:
						# Define Stream Chunk
						chunk = 1024
						# Open WAV
						f = wave.open('takesnapshot.wav', "rb")
						# Instantiate PyAudio
						p = pyaudio.PyAudio()  
						# Open Stream
						stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
						# Read Data from Stream
						data = f.readframes(chunk)  
						# Play Stream
						while data:
							stream.write(data)
							data = f.readframes(chunk)
						# Stop Stream
						stream.stop_stream()
						stream.close()
						# Close PyAudio
						p.terminate()
						gc.collect()
						#sys.exit()
					except Exception as e:
						print(e)
						#deactivatesound()

				procsound = threading.Thread(target=procsound,daemon=True)

				waitsound1.start()
				beep(338,222)
				camviewtimelimit = time.time() + 180
				while 1:
					gc.collect()

					frame = vs.read()
					frame = imutils.resize(frame, width=3264,height=2448)
					#frame = imutils.resize(frame, width=1600,height=1200)
					img_path = 'ocrimgs/capture.jpg'
					cv2.imshow(window_name, frame)
					cv2.waitKey(interframe_wait_ms) 

					## Check BSTATUS
					if keyboard.is_pressed('1'):
						waitsnd1.set()
						beep(538,222)
						procsound.start()
						cv2.imwrite(img_path, frame)
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('clear')
						break

					elif keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							waitsnd1.set()
							cv2.destroyAllWindows()
							vs.stop()
							deactivatesound(titletext)
							return

					elif time.time() > camviewtimelimit:
						beep(238,222)
						say('OCR mode auto deactivating now.  ')
						try:
							waitsnd1.set()
							waitsnd2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							waitsnd1.set()
							cv2.destroyAllWindows()
							vs.stop()
							deactivatesound(titletext)
							return

					else:
						time.sleep(0.001)

				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

				waitsound2.start()
				# Image Post Processing
				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass
				img_path = path+'/ocrimgs/capture.jpg'
				image = img_path
				image = cv2.imread(image)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (5, 5), 0)
				image = cv2.imwrite(img_path, gray)

				if platform.system() == 'Windows':
					path = path.replace('\\','/')
					os.system('magick convert '+img_path+' -unsharp 0x0.55+0.55+0.008 -set density 300 -quality 175 -alpha off '+path+'/ocrfinroi/CapturedSnapshot.jpg')
				elif platform.system() != 'Windows':
					# Install ImageMagick by apt-get install ImageMagick
					os.system('convert '+img_path+' -unsharp 0x0.55+0.55+0.008 -set density 300 -quality 175 -alpha off '+path+'/ocrfinroi/CapturedSnapshot.jpg')

				while 1:
					if platform.system() == 'Windows':
						path = path.replace('\\','/')
					elif platform.system() != 'Windows':
						pass
					if os.path.exists(path+'/ocrfinroi/CapturedSnapshot.jpg'):
						break
					else:
						time.sleep(0.01)

				# Microsoft CIS OCR API Processing
				with open('ocrfinroi/CapturedSnapshot.jpg', "rb") as image:
					headers = {'Ocp-Apim-Subscription-Key': onlineocr_subscription_key, 'Content-Type': 'application/octet-stream'}
					params  = {'mode': 'Printed'}
					data = image
					response = requests.post(
						text_recognition_url, headers=headers, params=params, data=data)
					response.raise_for_status()

				operation_url = response.headers["Operation-Location"]

				# Wait for Results from Microsoft CIS OCR API
				analysis = {}
				poll = True
				while (poll):
					response_final = requests.get(
						response.headers["Operation-Location"], headers=headers)
					analysis = response_final.json()
					#print(analysis)
					time.sleep(1)

					if ("recognitionResults" in analysis):
						poll= False 
					if ("status" in analysis and analysis['status'] == 'Failed'):
						poll= False

				polygons=[]
				if ("recognitionResults" in analysis):
					polygons = [(line["boundingBox"], line["text"])

						for line in analysis["recognitionResults"][0]["lines"]]

				textres = []
				for polygon in polygons:
					text = polygon[1]
					text = text.strip()
					textres.append(text)

				i = 0
				if platform.system() == 'Windows':
					path = path.replace('\\','/')
					x = open(path+'/ocrtxts/OCRResults.txt', "w")
				elif platform.system() != 'Windows':
					x = open(path+'/ocrtxts/OCRResults.txt', "w")

				for word in textres:
					i += 1
					if i % 3	 == 0:
						x.write('\n')
					else:
						word = word.strip()
						word = word.replace('\n',' ')
					x.write(word)

				x.close()

				while 1:
					if platform.system() == 'Windows':
						path = path.replace('\\','/')
					elif platform.system() != 'Windows':
						pass

					if os.path.exists(path+'/ocrtxts/OCRResults.txt'):
						xx = open(path+'/ocrtxts/OCRResults.txt', "r")
						yy = xx.readlines()
						numln = len(yy)
						lsln = []
						for ln in yy:
							if ln == '' or ln == '\n':
								lsln.append('1')
							else:
								time.sleep(0.01)
						xx.close()
						numempty = len(lsln)
						if numln == numempty:
							if platform.system() == 'Windows':
								path = path.replace('\\','/')
							elif platform.system() != 'Windows':
								pass
							xxx = open(path+'/ocrtxts/OCRResults.txt', "w")
							xxx.write('Recognition error! Please make sure you\'re in a well lit environment. Also try to place the document at least 5 inches from your central view. ')
							xxx.close()
						else:
							pass
						waitsnd2.set()
						beep(538,333)
						print('\n   OCR processing is now complete ...   \n   A text file and an image will now be emailed to you ...   \n   The text output will also be read out to you in the next few seconds ...   \n')
						def saymsg():
							say('OCR processing is now complete! A text file and an image will now be emailed to you. The text output will also be read out to you in the next few seconds!  ')
						saymsg = threading.Thread(target=saymsg,daemon='True')
						saymsg.start()
						break
					else:
						time.sleep(0.01)

				waitsound3.start()

				now = datetime.datetime.now()
				month = str(now.month)
				day = str(now.day)
				year = str(now.year)
				hour = str(now.hour)
				minute = str(now.minute)

				# Email Details
				print('\n   To enter your own sender and recipient emails, open the vision.py file. Press ctrl+f and type marxvergelmelencio@gmail.com to replace these emails with your own. Comment out these lines afterwards.  \n')
				say('To enter your own sender and recipeient emails, open the vision.py file. Press control then f and type marxvergelmelencio@gmail.com to replace these emails with your own. Comment out these lines afterwards.')
				time.sleep(3)

				to = 'marxvergelmelencio@gmail.com'
				subject = 'VIsION OCR Text Output with Snapshot:  '+hour+':'+minute+', '+month+' '+day+', '+year
				body = 'Brought to you by VIsION AI Labs ... '

				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass

				textoutput = path+'/ocrtxts/OCRResults.txt'
				snapshotimg = path+'/ocrfinroi/CapturedSnapshot.jpg'

				yag = yagmail.SMTP('visiondemoemail1234@gmail.com')
				yag.send(to,subject,contents=[body,textoutput,snapshotimg])

				waitsnd3.set()
				beep(538,222)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

				print('\n   Text output and captured snapshot emailed to '+to+' ...   \n')
				def saymsg2():
					say('Text output and captured snapshot emailed to '+to)
				saymsg2 = threading.Thread(target=saymsg2,daemon='True')
				saymsg2.start()

				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass

				analyzedimage = path+'/ocrfinroi/CapturedSnapshot.jpg'
				beep(338,222)
				if platform.system() == 'Windows':
					os.system(analyzedimage)
				elif platform.system() != 'Windows':
					os.system('firefox '+analyzedimage)

				f = open(path+'/ocrtxts/OCRResults.txt', "rb")
				ocredtext = f.readlines()
				ocredtextlines = []
				for xxx in ocredtext:
					xxx = xxx.decode()
					xxx = xxx.replace('\r','')
					xxx = xxx.replace('\n','')
					xxx = str(xxx)
					text = "".join([c if ord(c) < 128 else "" for c in xxx]).strip()
					ocredtextlines.append(text)
				beep(538,222)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

				print('\n   Quick press to read per line ...   \n   Hold press to quit ...   \n')
				def saymsg3():
					say('Quick press to read per line! Hold press to quit!  ')
				saymsg3 = threading.Thread(target=saymsg3,daemon='True')
				saymsg3.start()
				os.system('cls')

				maintimelimit = time.time() + 1200
				while 1:
					buttonpress = -1
					totaltextlines = len(ocredtext)

					while 1:
						if keyboard.is_pressed('1'):
							beep(538,222)
							buttonpress += 1
							if buttonpress == totaltextlines:
								break
							else:
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								xxx = ocredtextlines[buttonpress]
								xxx = xxx.replace('\r','')
								xxx = xxx.replace('\n','')
								xxx = str(xxx)
								xxx = xxx.strip()
								print(xxx)
								def sayocr():
									say(xxx)
								sayocr = threading.Thread(target=sayocr,daemon='True')
								sayocr.start()

						elif keyboard.is_pressed('2'):
							f.close()
							try:
								waitsnd1.set()
								waitsnd2.set()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return

						elif time.time() > maintimelimit:
							f.close()
							try:
								waitsnd1.set()
								waitsnd2.set()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return


# Parent Thread of Offline OCR Mode
def offlineocr():
				title("  VIsION OCR Mode  ")
				titletext = 'OCR Mode'

				path = os.path.dirname(os.path.realpath(__file__))
				cleanup()
				intromsg(titletext)
				gc.collect()

				vs = WebcamVideoStream(src=0).start()
				window_name = "VIsION_CAM"
				interframe_wait_ms = 800
				cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
				cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

				## Collection of Daemonic Threads

				#  wait sound1
				def waitsound1(waitsnd1,t):
					time.sleep(3)
					beep(338,222)
					print('\n   Quick Press to Take Snapshot ...   ')
					say('Quick press to take snapshot! ')
					beep(338,222)
					print('\n   Hold Press to Deactivate ...   ')
					say('Hold press to deactivate! ')
					beep(338,222)
					print('\n   Or Leave Idle to Auto Deactivate ...   ')
					say('Or, leave idle to auto deactivate! ')

					while not waitsnd1.is_set():
						event_is_set = waitsnd1.wait(t)
						if event_is_set:
							return
						else:
							time.sleep(7)
							beep(338,222)
							say('Waiting for keypress. ')
					return

				waitsnd1 = threading.Event()
				waitsound1 = threading.Thread(target=waitsound1,daemon=True,args=(waitsnd1, 0.03), )

				#  wait sound2
				def waitsound2(waitsnd2,t):
					time.sleep(0.1)
					speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
					psndcounter = -1
					psndcounter2 = -1
					say(random.choice(speakthisnow))
					print('\n   '+random.choice(speakthisnow)+'   \n')
					if platform.system() == 'Windows':
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('clear')
					while not waitsnd2.is_set():
						psndcounter += 25
						psndcounter2 += 0.01
						freq = 338 + psndcounter 
						dur = 66
						beep(freq,dur)
						time.sleep(0.2-psndcounter2)
						event_is_set = waitsnd2.wait(t)
						if event_is_set:
							break
					return

				waitsnd2 = threading.Event()
				waitsound2 = threading.Thread(target=waitsound2,daemon=True,args=(waitsnd2, 0.03), )

				#  wait sound3
				def waitsound3(waitsnd3,t):
					time.sleep(0.1)
					speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']
					psndcounter = -1
					psndcounter2 = -1
					say(random.choice(speakthisnow))
					print('\n   '+random.choice(speakthisnow)+'   \n')
					if platform.system() == 'Windows':
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('clear')
					while not waitsnd3.is_set():
						psndcounter += 25
						psndcounter2 += 0.01
						freq = 338 + psndcounter 
						dur = 66
						beep(freq,dur)
						time.sleep(0.2-psndcounter2)
						event_is_set = waitsnd3.wait(t)
						if event_is_set:
							break
					return

				waitsnd3 = threading.Event()
				waitsound3 = threading.Thread(target=waitsound3,daemon=True,args=(waitsnd3, 0.03), )


				# Processing Sound
				def procsound():
					try:
						# Define Stream Chunk
						chunk = 1024
						# Open WAV
						f = wave.open('takesnapshot.wav', "rb")
						# Instantiate PyAudio
						p = pyaudio.PyAudio()  
						# Open Stream
						stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
						# Read Data from Stream
						data = f.readframes(chunk)  
						# Play Stream
						while data:
							stream.write(data)
							data = f.readframes(chunk)
						# Stop Stream
						stream.stop_stream()
						stream.close()
						# Close PyAudio
						p.terminate()
						gc.collect()
						#sys.exit()
					except Exception as e:
						print(e)
						#deactivatesound()

				procsound = threading.Thread(target=procsound,daemon=True)

				waitsound1.start()
				beep(338,222)
				camviewtimelimit = time.time() + 180
				while 1:
					gc.collect()

					frame = vs.read()
					frame = imutils.resize(frame, width=3264,height=2448)
					#frame = imutils.resize(frame, width=1600,height=1200)
					img_path = 'ocrimgs/capture.jpg'
					cv2.imshow(window_name, frame)
					cv2.waitKey(interframe_wait_ms) 

					## Check BSTATUS
					if keyboard.is_pressed('1'):
						waitsnd1.set()
						beep(538,222)
						procsound.start()
						cv2.imwrite(img_path, frame)
						cv2.destroyAllWindows()
						vs.stop()
						if platform.system() == 'Windows':
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('clear')
						break

					elif keyboard.is_pressed('2'):
						try:
							waitsnd1.set()
							waitsnd2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							waitsnd1.set()
							cv2.destroyAllWindows()
							vs.stop()
							deactivatesound(titletext)
							return

					elif time.time() > camviewtimelimit:
						beep(238,222)
						say('OCR mode auto deactivating now.  ')
						try:
							waitsnd1.set()
							waitsnd2.set()
							cv2.destroyAllWindows()
							vs.stop()
							if platform.system() == 'Windows':
								os.system('taskkill /f /im firefox.exe /t')
								os.system('cls')
							elif platform.system() != 'Windows':
								os.system('kill -9 $(ps -x | grep firefox)')
								os.system('clear')
							deactivatesound(titletext)
							return
						except Exception as e:
							waitsnd1.set()
							cv2.destroyAllWindows()
							vs.stop()
							deactivatesound(titletext)
							return

					else:
						time.sleep(0.001)

				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

				waitsound2.start()
				# Image Post Processing
				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass
				img_path = path+'/ocrimgs/capture.jpg'
				image = img_path
				image = cv2.imread(image)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (5, 5), 0)
				image = cv2.imwrite(img_path, gray)

				if platform.system() == 'Windows':
					path = path.replace('\\','/')
					os.system('magick convert '+img_path+' -unsharp 0x0.55+0.55+0.008 -set density 300 -quality 175 -alpha off '+path+'/ocrfinroi/CapturedSnapshot.jpg')
				elif platform.system() != 'Windows':
					# Install ImageMagick by apt-get install ImageMagick
					os.system('convert '+img_path+' -unsharp 0x0.55+0.55+0.008 -set density 300 -quality 175 -alpha off '+path+'/ocrfinroi/CapturedSnapshot.jpg')

				while 1:
					if platform.system() == 'Windows':
						path = path.replace('\\','/')
					elif platform.system() != 'Windows':
						pass

					if os.path.exists(path+'/ocrfinroi/CapturedSnapshot.jpg'):
						break
					else:
						time.sleep(0.01)

				# Tesseract DL Processing
				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass

				# Install Tesseract 4 ( apt-get install tesseract-ocr or download binary for Microsoft Windows )
				os.system('tesseract '+path+'/ocrfinroi/CapturedSnapshot.jpg '+path+'/ocrtxts/OCRResults --oem 1 --psm 6 /quiet')

				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass

				while 1:
					if os.path.exists(path+'/ocrtxts/OCRResults.txt'):
						break
					else:
						time.sleep(0.01)

				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass

				xx = open(path+'/ocrtxts/OCRResults.txt', "r")
				yy = xx.readlines()
				numln = len(yy)
				lsln = []
				for ln in yy:
					if ln == '' or ln == '\n':
						lsln.append('1')
					else:
						time.sleep(0.01)
				xx.close()

				numempty = len(lsln)
				if numln == numempty:
					if platform.system() == 'Windows':
						path = path.replace('\\','/')
					elif platform.system() != 'Windows':
						pass
					xxx = open(path+'/ocrtxts/OCRResults.txt', "w")
					xxx.write('Recognition error! Please make sure you\'re in a well lit environment. Also try to place the document at least 5 inches from your central view. ')
					xxx.close()
				else:
					pass

				waitsnd2.set()
				beep(538,333)
				print('\n   OCR processing is now complete ...   \n   A text file and the captured snapshot will now be saved in your local OfflineOCRResults directory ...   \n   The text output will also be read out to you in the next few seconds ...   \n')
				def saymsg():
					say('OCR processing is now complete! A text file and the captured snapshot will now be saved in your local OfflineOCRResults directory. The text output will also be read out to you in the next few seconds!  ')
				saymsg = threading.Thread(target=saymsg,daemon='True')
				saymsg.start()

				waitsound3.start()
				now = datetime.datetime.now()
				month = str(now.month)
				day = str(now.day)
				year = str(now.year)
				hour = str(now.hour)
				minute = str(now.minute)

				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass

				# File Details
				textoutput = path+'/ocrtxts/OCRResults.txt'
				newtextoutput = path+'/OfflineOCRResults/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.txt'
				snapshotimg = path+'/ocrfinroi/CapturedSnapshot.jpg'
				newsnapshotimg = path+'/OfflineOCRResults/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.jpg'

				# Saving Files
				os.system('cp '+textoutput+' '+newtextoutput)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')
				os.system('cp '+snapshotimg+' '+newsnapshotimg)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

				waitsnd3.set()
				beep(538,222)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

				print('\n   Text output and captured snapshot saved in local OfflineOCRResults directory ...   \n')
				def saymsg2():
					say('Text output and captured snapshot saved in local OfflineOCRResults directory! ')
				saymsg2 = threading.Thread(target=saymsg2,daemon='True')
				saymsg2.start()

				if platform.system() == 'Windows':
					path = path.replace('\\','/')
				elif platform.system() != 'Windows':
					pass

				analyzedimage = path+'/ocrfinroi/CapturedSnapshot.jpg'
				beep(338,222)
				if platform.system() == 'Windows':
					os.system(analyzedimage)
				elif platform.system() != 'Windows':
					os.system('firefox '+analyzedimage)

				f = open(path+'/ocrtxts/OCRResults.txt', "rb")
				ocredtext = f.readlines()
				ocredtextlines = []
				for xxx in ocredtext:
					xxx = xxx.decode()
					xxx = xxx.replace('\r','')
					xxx = xxx.replace('\n','')
					xxx = str(xxx)
					text = "".join([c if ord(c) < 128 else "" for c in xxx]).strip()
					ocredtextlines.append(text)
				beep(538,222)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')

				print('\n   Quick press to read per line ...   \n   Hold press to quit ...   \n')
				def saymsg3():
					say('Quick press to read per line! Hold press to quit!  ')
				saymsg3 = threading.Thread(target=saymsg3,daemon='True')
				saymsg3.start()
				os.system('cls')

				maintimelimit = time.time() + 1200
				while 1:
					buttonpress = -1
					totaltextlines = len(ocredtext)

					while 1:
						if keyboard.is_pressed('1'):
							beep(538,222)
							buttonpress += 1
							if buttonpress == totaltextlines:
								break
							else:
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								xxx = ocredtextlines[buttonpress]
								xxx = xxx.replace('\r','')
								xxx = xxx.replace('\n','')
								xxx = str(xxx)
								xxx = xxx.strip()
								print(xxx)
								def sayocr():
									say(xxx)
								sayocr = threading.Thread(target=sayocr,daemon='True')
								sayocr.start()

						elif keyboard.is_pressed('2'):
							f.close()
							try:
								waitsnd1.set()
								waitsnd2.set()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return

						elif time.time() > maintimelimit:
							f.close()
							try:
								waitsnd1.set()
								waitsnd2.set()
								if platform.system() == 'Windows':
									os.system('taskkill /f /im firefox.exe /t')
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('kill -9 $(ps -x | grep firefox)')
									os.system('clear')
								deactivatesound(titletext)
								return
							except Exception as e:
								deactivatesound(titletext)
								return


# One-Time Object Recognition Mode
def onetimeobjectrecognition():
	title("  VIsION One-Time Recognition Mode  ")
	titletext = 'One-Time Recognition Mode'

	cleanup()
	intromsg(titletext)

	#  wait sound
	def waitsound(waitsnd,t):
		import pythoncom
		from win32com.client import constants
		import win32com.client
		pythoncom.CoInitialize()
		speaker=win32com.client.Dispatch('SAPI.SpVoice')
		speaker.Volume = 100
		speaker.Rate = 0
		import winsound
		import random

		time.sleep(0.1)
		speakthisnow = ['Processing!  ','Analyzing!  ','Please wait!  ','Processing! Please wait!  ','Analyzing!  One moment!  ','One moment!  ','A moment please!  ']

		psndcounter = -1
		psndcounter2 = -1

		say(random.choice(speakthisnow))
		print('\n   '+random.choice(speakthisnow)+'   \n')
		if platform.system() == 'Windows':
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('clear')

		while not waitsnd.is_set():
			psndcounter += 25
			psndcounter2 += 0.01
			freq = 338 + psndcounter 
			dur = 66
			beep(freq,dur)
			time.sleep(0.2-psndcounter2)
			event_is_set = waitsnd.wait(t)
			if event_is_set:
				break
		return

	waitsnd = threading.Event()
	waitsound = threading.Thread(target=waitsound,daemon=True,args=(waitsnd, 0.03), )


	# Processing Sound
	def procsound():
		try:

			# Define Stream Chunk
			chunk = 1024
			# Open WAV
			f = wave.open('takesnapshot.wav', "rb")
			# Instantiate PyAudio
			p = pyaudio.PyAudio()  
			# Open Stream
			stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
			# Read Data from Stream
			data = f.readframes(chunk)  
			# Play Stream
			while data:

				stream.write(data)
				data = f.readframes(chunk)
			# Stop Stream
			stream.stop_stream()
			stream.close()
			# Close PyAudio
			p.terminate()
			gc.collect()
			#sys.exit()
		except Exception as e:
			print(e)
			#deactivatesound()

	def inst():
		freq = 538
		dur = 333
		beep(freq,dur)
		say('Quick press to take snapshot! Hold press to deactivate! Or leave idle for auto deactivation!  ')
		print('\n   Quick press to take snapshot ...   \n   Hold press to deactivate ...   \n   Or Leave Idle for Auto Deactivation ...   \n')

	inst = threading.Thread(target=inst,daemon=True)
	inst.start()

	# Capture Image
	vs = WebcamVideoStream(src=0).start()

	window_name = "VIsION_CAM"
	interframe_wait_ms = 2500
	cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

	camviewtimelimit = time.time() + 180
	while 1:
		try:
			frame = vs.read()
			frame = imutils.resize(frame, width=3264,height=2448)
			#frame = imutils.resize(frame, width=1600,height=1200)
			img_path = 'otimgs/capture.jpg'
			beep(333,666)
			cv2.imshow(window_name, frame)
			cv2.waitKey(interframe_wait_ms) 
			if time.time() > camviewtimelimit:
				say('One time recognition mode auto deactivating! ')
				print('\n   One-Time Recognition Mode Auto Deactivating ...   \n')
				beep(338,333)
				beep(238,222)
				beep(138,111)
				cv2.destroyAllWindows()
				vs.stop()
				return
			elif keyboard.is_pressed('1'):
				beep(338,222)
				procsound()
				cv2.imwrite(img_path, frame)
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')
				break
			elif keyboard.is_pressed('2'):
				say('Deactivating one time recognition mode! ')
				print('\n   Deactivating One-Time Recognition Mode ...   \n')
				beep(338,333)
				beep(238,222)
				beep(138,111)
				cv2.destroyAllWindows()
				vs.stop()
				return
			else:
				# Get Window Name (for Windows only)
				def window_enum_handler(hwnd, resultList):
					if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
						resultList.append((hwnd, win32gui.GetWindowText(hwnd)))
				def get_app_list(handles=[]):
					mlst=[]
					win32gui.EnumWindows(window_enum_handler, handles)
					for handle in handles:
						mlst.append(handle)
					return mlst
				appwindows = get_app_list()
				for i in appwindows:
					winname = i[1]
					winname = str(winname)
					winname = winname.strip()
					if winname == 'VIsION_CAM':
						win32gui.SetForegroundWindow(i[0])
		except cv2.error as e:
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			break

	# Cam Cleanup
	cv2.destroyAllWindows()
	vs.stop()
	if platform.system() == 'Windows':
		os.system('cls')
	elif platform.system() != 'Windows':
		os.system('clear')

	waitsound.start()

	# Cloudsight API Processing
	img_path = 'otimgs/capture.jpg'

	image = img_path

	def get_token_for_encoded_image(image, onetimerecognition_api_key, locale='en-US'):
		try:
			url = onetimerecognition_api_base_url + '/image_requests'
			files = {'image_request[image]': image}
			response = requests.post(url, headers=_auth_header(onetimerecognition_api_key), data=_locale(locale), files=files)
			return response.json()['token']
		except KeyError:
			Freq = 333
			Dur = 199
			beep(Freq,Dur)
			say('Invalid Cloudsight key! Please correct! ')
			print('\n   Invalid Cloudsight Key ...   \n   Please Correct ...   \n')
			time.sleep(1)
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			deactivatesound()
			return

	def get_results_for_token(token, onetimerecognition_api_key):
		while 1:
			r = requests.get(onetimerecognition_api_base_url + '/image_responses/' + token, headers=_auth_header(onetimerecognition_api_key))
			response_content = r.json()
			if response_content['status'] != 'not completed':
				return response_content

	def _auth_header(onetimerecognition_api_key):
		return {'Authorization': 'CloudSight ' + onetimerecognition_api_key}

	def _locale(locale):
		return {'image_request[locale]': locale}

	with open(img_path, 'rb') as image:
		starttime = time.time()
		image_token = get_token_for_encoded_image(image, onetimerecognition_api_key)

	image_results = get_results_for_token(image_token, onetimerecognition_api_key)
	description = image_results['name']

	waitsnd.set()
	res = str(description)
	res = res.strip()
	time.sleep(0.5)
	freq = 338
	dur = 333
	beep(freq,dur)
	time.sleep(0.3)
	say(res)
	print('\n   '+res+'   \n')

	if ultrasonic == 'true':
		iss.i2c.write(0xE0, 0x01, [0x06])
		iss.i2c.write(0xE0, 0x02, [0xFF])
		while 1:
			iss.i2c.write(0xE0, 0x00, [0x50])
			time.sleep(0.067)
			data = iss.i2c.read(0xE0, 0x03, 1)
			data = data[0]
			data = int(data)
			if data > 0 and data < 24:
				data = str(data)
				freq = 338
				dur = 222
				beep(freq,dur)
				say('Central distance is '+data+' inches! ')
				break
			elif data > 24 and 	data < 108:
				data = int(data) / int(12)
				data = round(data,1)
				data = str(data)
				freq = 338
				dur = 222
				beep(freq,dur)
				say('Central distance is '+data+' feet! ')
				break
			elif data > 108:
				freq = 338
				dur = 222
				beep(freq,dur)
				say('Central distance is beyond nine feet! ')
				break
			elif data == 0:
				freq = 538
				dur = 111
				beep(freq,dur)
				time.sleep(0.067)
			else:
				time.sleep(0.01)
	elif ultrasonic == 'false':
		pass

	time.sleep(0.3)
	deactivatesound()
	return


	#endtime = time.time()
	#totaltime = endtime-starttime
	#totaltime = round(totaltime, 2)
	#totaltime = str(totaltime)
	#os.system('cls')
	#print('\n   Cloudsight Processing Took '+totaltime+' Seconds ...   \n')
	#say('Cloudsight processing took '+totaltime+' seconds!  ')


# Manual Visual Assistance
def manualvisualassistance():
	title('MANUAL_VISUAL_ASSISTANCE')
	titletext = 'Manual Visual Assistance Mode'

	cleanup()
	intromsg(titletext)

	while 1:
		buttonpress = -1
		selectiontimelimit = time.time() + 90
		peerlist = ['mvastart1.bat','mvastart2.bat']
		namelist = ['echo123','visionliveguide','cherry.melencio','Deactivate Manual Visual Assistance']
		noofpeers = len(namelist)

		dur = 333
		freq = 333
		#beep(freq,dur)
		say('Quick press to go through contact list! Hold press to select!  ')
		print('\n   Quick Press to go through contact list ...   \n   Hold Press to Select ...   \n')

		while 1:
			if keyboard.is_pressed('1'):
				freq = 438
				dur = 111
				beep(freq,dur)
				buttonpress += 1
				if buttonpress < noofpeers:
					if platform.system() == 'Windows':
						os.system('cls')
					elif platform.system() != 'Windows':
						os.system('clear')
					say(namelist[buttonpress])
					print(namelist[buttonpress])
				else:
					break

			elif keyboard.is_pressed('2'):
				beep(338,333)
				if buttonpress < noofpeers:
					if buttonpress < (noofpeers-1):
						beep(438,111)
						os.system(peerlist[buttonpress])
						if platform.system() == 'Windows':
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('clear')
						time.sleep(1)
						beep(538,222)
						say('Now contacting '+namelist[buttonpress]+'!  ')
						print('Now Contacting '+namelist[buttonpress]+'!  ')
						time.sleep(1.5)
						pyautogui.hotkey('winleft','r')
						time.sleep(0.3)
						pyautogui.typewrite('narrator')
						time.sleep(0.3)
						beep(538,333)
						pyautogui.press('enter')
						beep(338,222)
						pyautogui.press('ctrlleft')
						print('\n   Quick Press to Tab Through Buttons ...   \n')
						say('Quick press to tab through buttons. ')
						beep(338,222)
						print('\n   Hold Press to Activate Button ...   \n')
						say('Hold press to activate button. ')
						beep(338,222)
						print('\n   Any Time During or After a Video Call, Quick Press to Deactivate ...   \n')
						say('During or after a video call, quick press to deactivate manual visual assistance. ')
						beep(338,222)
						print('\n   Or Leave Idle to Auto Deactivate ...   \n')
						say('Or leave idle to auto deactivate. ')

						tabtimelimit = time.time() + 60
						while 1:
							if time.time() > tabtimelimit:
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								os.system('taskkill /f /im narrator.exe /t')
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								time.sleep(0.3)
								os.system('mvastop.bat')
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								beep(338,444)
								beep(238,333)
								beep(138,222)
								say('Now deactivating manual visual assistance mode!  ')
								print('\n   Deactivating Manual Visual Assistance Mode ...   \n')
								return
							elif keyboard.is_pressed('1'):
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								beep(238,222)
								pyautogui.press('tab')
								time.sleep(0.3)
							elif keyboard.is_pressed('2'):
								beep(238,222)
								pyautogui.press('enter')
								time.sleep(0.3)
								os.system('taskkill /f /im narrator.exe /t')
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								break
						# Get Window Name (for Windows only)
						def window_enum_handler(hwnd, resultList):
							if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
								resultList.append((hwnd, win32gui.GetWindowText(hwnd)))
						def get_app_list(handles=[]):
							mlst=[]
							win32gui.EnumWindows(window_enum_handler, handles)
							for handle in handles:
								mlst.append(handle)
							return mlst
						appwindows = get_app_list()
						for i in appwindows:
							winname = i[1]
							winname = str(winname)
							winname = winname.strip()
							if winname == 'MANUAL_VISUAL_ASSISTANCE':
								win32gui.SetForegroundWindow(i[0])
						calltimelimit = time.time() + 10800
						while 1:
							if keyboard.is_pressed('1'):
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								os.system('mvastop.bat')
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								beep(338,444)
								beep(238,333)
								beep(138,222)
								say('Now deactivating manual visual assistance mode!  ')
								print('\n   Deactivating Manual Visual Assistance Mode ...   \n')
								return
							elif time.time() > calltimelimit:
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								os.system('mvastop.bat')
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								beep(338,444)
								beep(238,333)
								beep(138,222)
								say('Now deactivating manual visual assistance mode!  ')
								print('\n   Deactivating Manual Visual Assistance Mode ...   \n')
								return
							else:
								if platform.system() == 'Windows':
									os.system('cls')
								elif platform.system() != 'Windows':
									os.system('clear')
								time.sleep(0.03)
					elif buttonpress == 3:
						if platform.system() == 'Windows':
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('clear')
						beep(338,444)
						beep(238,333)
						beep(138,222)
						say('Deactivating manual visual assistance!  ')
						print('\n   Deactivating Manual Visual Assistance   \n')
						return
					else:
						if platform.system() == 'Windows':
							os.system('cls')
						elif platform.system() != 'Windows':
							os.system('clear')
						break

			elif time.time() > selectiontimelimit:
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')
				say('Waiting for selection!  ')
				print('\n   Waiting for Selection ...   \n')
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')
				break


# Video Recording Mode
def videorecordingmode():
	## Initialization
	title("  VIsION Video Recording Mode  ")
	titletext = 'Video Recording Mode'

	cleanup()
	intromsg(titletext)

	#  wait sound
	def waitsound(waitsnd,t):
		time.sleep(0.1)
		while not waitsnd.is_set():
			time.sleep(15)
			beep(338,222)
			event_is_set = waitsnd.wait(t)
			if event_is_set:
				break
		return
	
	waitsnd = threading.Event()
	waitsound = threading.Thread(target=waitsound,daemon=True,args=(waitsnd, 0.03), )
	
	beep(338,333)
	print('\n   Now Recording ...   \n')
	say('Now recording.  ')

	waitsound.start()
	now = datetime.datetime.now()
	month = str(now.month)
	day = str(now.day)
	year = str(now.year)
	hour = str(now.hour)
	minute = str(now.minute)

	path = os.path.dirname(os.path.realpath(__file__))
	if platform.system() == 'Windows':
		path = path.replace('\\','/')
	elif platform.system() != 'Windows':
		pass

	#CREATE_NO_WINDOW = 0x08000000
	#subprocess.call('ffmpeg -f dshow -i video="USB Camera2":audio="USBCamMic (USB Audio)" '+path+'/VideoRecordings/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.avi', creationflags=CREATE_NO_WINDOW)
	#subprocess.call('ffmpeg -f dshow -i video="BisonCam, NB Pro":audio="Microphone (Realtek High Definition Audio)" '+path+'/VideoRecordings/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.avi', creationflags=CREATE_NO_WINDOW)

	def vidrecx(vrx,t):
		#os.system('Start /min ffmpeg -f dshow -i video="USB Camera2":audio="USBCamMic (USB Audio)" '+path+'/VideoRecordings/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.avi')
		os.system('Start /min ffmpeg -f dshow -i video="BisonCam, NB Pro":audio="Microphone (Realtek High Definition Audio)" '+path+'/VideoRecordings/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.avi')

		while not vrx.is_set():
			event_is_set = vrx.wait(t)
			if event_is_set:
				if platform.system() == 'Windows':
					os.system('taskkill /f /im ffmpeg.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('killall ffmpeg')
					os.system('clear')
				return
			else:
				time.sleep(0.01)

	vrx = threading.Event()
	vidrecx = threading.Thread(target=vidrecx,daemon=True,args=(vrx, 0.03), )
	vidrecx.start()

	vidrectimelimit = time.time() + 600
	while not time.time() > vidrectimelimit:
		if keyboard.is_pressed('1'):
			beep(538,333)
			waitsnd.set()
			vrx.set()
			break
		elif keyboard.is_pressed('2'):
			beep(538,222)
			waitsnd.set()
			vrx.set()
			break
		else:
			time.sleep(0.01)

	print('\n   Now Saving Video ...   \n')
	say('Now saving video. ')


	deactivatesound(titletext)
	return


# Sound Recording Mode
def soundrecordingmode():
	## Initialization
	title("  VIsION Sound Recording Mode  ")
	titletext = 'Sound Recording Mode'

	cleanup()
	intromsg(titletext)

	#  wait sound
	def waitsound(waitsnd,t):
		time.sleep(0.1)
		while not waitsnd.is_set():
			time.sleep(15)
			beep(338,222)
			event_is_set = waitsnd.wait(t)
			if event_is_set:
				break
		return
	
	waitsnd = threading.Event()
	waitsound = threading.Thread(target=waitsound,daemon=True,args=(waitsnd, 0.03), )
	
	beep(338,333)
	print('\n   Now Recording ...   \n')
	say('Now recording.  ')

	waitsound.start()
	now = datetime.datetime.now()
	month = str(now.month)
	day = str(now.day)
	year = str(now.year)
	hour = str(now.hour)
	minute = str(now.minute)

	path = os.path.dirname(os.path.realpath(__file__))
	if platform.system() == 'Windows':
		path = path.replace('\\','/')
	elif platform.system() != 'Windows':
		pass

	#CREATE_NO_WINDOW = 0x08000000
	#subprocess.call('ffmpeg -f dshow -i audio="USBCamMic (USB Audio)" '+path+'/SoundRecordings/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.wav', creationflags=CREATE_NO_WINDOW)
	#subprocess.call('ffmpeg -f dshow -i audio="Microphone (Realtek High Definition Audio)" '+path+'/SoundRecordings/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.wav', creationflags=CREATE_NO_WINDOW)

	def sndrecx(srx,t):
		#os.system('Start /min ffmpeg -f dshow -i audio="USBCamMic (USB Audio)" '+path+'/SoundRecordings/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.wav')

		os.system('Start /min ffmpeg -f dshow -i audio="Microphone (Realtek High Definition Audio)" '+path+'/SoundRecordings/'+hour+'_'+minute+'_'+month+'_'+day+'_'+year+'.wav')

		while not srx.is_set():
			event_is_set = srx.wait(t)
			if event_is_set:
				if platform.system() == 'Windows':
					os.system('taskkill /f /im ffmpeg.exe /t')
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('killall ffmpeg')
					os.system('clear')
				return
			else:
				time.sleep(0.01)

	srx = threading.Event()
	sndrecx = threading.Thread(target=sndrecx,daemon=True,args=(srx, 0.03), )
	sndrecx.start()

	srectimelimit = time.time() + 600
	while not time.time() > srectimelimit:
		if keyboard.is_pressed('1'):
			beep(538,333)
			waitsnd.set()
			srx.set()
			break
		elif keyboard.is_pressed('2'):
			beep(538,222)
			waitsnd.set()
			srx.set()
			break
		else:
			time.sleep(0.01)

	print('\n   Now Saving Audio Recording ...   \n')
	say('Now saving audio recording. ')

	deactivatesound(titletext)
	return


# VIsION Options
startupcounter = 0
while 1:
	title("   VIsION Open Source DIY AI Glasses   ")
	try:
		cv2.destroyAllWindows()
		vs.stop()
		if platform.system() == 'Windows':
			os.system('taskkill /f /im firefox.exe /t')
			os.system('cls')
			os.system('taskkill /f /im ffmpeg.exe /t')
			os.system('cls')
		elif platform.system() != 'Windows':
			os.system('kill -9 $(ps -x | grep firefox)')
			os.system('clear')
			os.system('killall ffmpeg')
			os.system('clear')
	except Exception as e:
		pass

	startupcounter += 1
	while 1:
		if startupcounter %5 == 0:
			checkultrasonic()
			checkinternet()
			checkcam()
			break
		else:
			break

	buttonpress = -1
	maintimelimit = time.time() + 90
	mainoptions = ['SeeingWithSound mode!','Navigation mode!', 'OCR mode!', 'One-time recognition mode!', 'Manual visual assistance mode!', 'Video recording mode!', 'Sound recording mode!', 'Pocket PC mode!  ', 'Restart vision!', 'Turn off vision!']
	mainoptionstext = ['   SeeingWithSound Mode   ','   Navigation Mode   ', '   OCR Mode   ', '   One-Time Recognition Mode   ', '   Manual Visual Assistance Mode   ', '   Video Recording Mode   ', '   Sound Recording Mode   ', '   Pocket PC Mode   ', '   Restart VIsION   ', '   Turn Off VIsION   ']

	beep(333,333)
	print('\n   Quick Press to Go Through Options ...   \n   Hold Press to Select Current Option ...   \n')
	say('Quick press to go through options! ')

	def isayint(optsaystop,t):
		event_is_set = optsaystop.wait(t)
		if event_is_set:
			return
		say('Hold press to select current option!  ')

	optsaystop = threading.Event()
	isayint = threading.Thread(target=isayint,daemon=True,args=(optsaystop, 0.03), )

	isayint.start()

	while 1:
		if keyboard.is_pressed('1'):
			optsaystop.set()
			freq = 438
			dur = 111
			beep(freq,dur)
			buttonpress += 1
			if buttonpress < 10:
				if platform.system() == 'Windows':
					os.system('cls')
				elif platform.system() != 'Windows':
					os.system('clear')
				say(mainoptions[buttonpress])
				print(mainoptionstext[buttonpress])
			else:
				break

		elif keyboard.is_pressed('2'):
			beep(338,333)
			if buttonpress < 9:
				say('Enabling '+mainoptions[buttonpress]+'!  ')
				print('Enabling '+mainoptionstext[buttonpress]+'!  ')

				if buttonpress == 0:
					seeingwithsoundmode()
					break

				elif buttonpress == 1:
					if istatus == 'true' and onlinescenedescriptor_subscription_key != 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here':
						navigationmode()
						break
					elif istatus == 'false' or onlinescenedescriptor_subscription_key == 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here':
						offlinenavigationmode()
						break

				elif buttonpress == 2:
					if istatus == 'true' and onlineocr_subscription_key != 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here':
						onlineocr()
						break
					elif istatus == 'false' or onlineocr_subscription_key == 'Enter-Your-Microsoft-CIS-Computer-Vision-API-Key-Here':
						beep(238,333)
						say('Offline OCR in experimental stage. Currently being improved. ')
						offlineocr()
						break

				elif buttonpress == 3:
					if onetimerecognition_api_key != 'Enter-Your-Cloudsight-API-Key-Here' and istatus == 'true':
						onetimeobjectrecognition()
						break
					elif onetimerecognition_api_key == 'Enter-Your-Cloudsight-API-Key-Here' or istatus == 'false':
						print('\n   Offline Mode Only ...   \n   No Cloudsight API Credentials Found ...   \n   To enable one-time recognition mode, open vision.py File. Go to lines 312 and 313. Supply your API keys ...   \n')
						beep(238,333)
						say('Offline mode only. No Cloudsight API credentials found. To enable one time recognition mode, open vision.py file. Go to lines 312 and 313. Supply your API keys. ')
						break

				elif buttonpress == 4:
					if platform.system() == 'Windows' and istatus == 'true':
						manualvisualassistance()
						break
					elif platform.system() != 'Windows' and istatus == 'true':
						print('\n   Manual Visual Assistance Mode soon to be Implemented in Non-Windows Platforms ...   \n')
						beep(238,333)
						say('Manual visual assistance mode for non Windows platforms will be implemented soon. ')
						os.system('clear')
						break
					elif istatus == 'false':
						print('\n   Manual Visual Assistance Mode Requires Internet Connection ...   \n')
						beep(238,333)
						say('Manual visual assistance mode requires Internet connection. ')
						os.system('clear')
						break

				elif buttonpress == 5:
					videorecordingmode()
					break

				elif buttonpress == 6:
					soundrecordingmode()
					break

				elif buttonpress == 7:
					if platform.system() == 'Windows':
						print('\n   Initializing Pocket PC Mode.   \n   Deactivating VIsION ...   \n')
						say('Initializing pocket PC mode. ')
						try:
							import pyautogui
							pyautogui.FAILSAFE = False
							pyautogui.hotkey('winleft','r')
							time.sleep(1)
							pyautogui.typewrite('nvda')
							pyautogui.press('enter')
							time.sleep(5)
							pyautogui.press(['ctrlleft'])
							pyautogui.press(['esc','esc','esc','esc','esc'])
							beep(338,333)
							beep(238,222)
							beep(138,111)
							say('Now deactivating vision. ')
							os.system('cls')
							sys.exit()
						except Exception as e:
							print('\n   No NVDA installation found.   \n   Please install NVDA.   \n   Then make sure its main executable is in the system path ...   \n')
							beep(238,333)
							say('NVDA not found. Please install. And make sure its main executable is in the system path. ')
							os.system('cls')
							break
					elif platform.system() != 'Windows':
						print('\n   Initializing Pocket PC Mode.   \n   Deactivating VIsION ...   \n')
						say('Initializing pocket PC mode. ')
						beep(338,333)
						beep(238,222)
						beep(138,111)
						say('Now deactivating vision. ')
						os.system('clear')
						sys.exit()

				elif buttonpress == 8:
					print('\n   VIsION Restarting Now ...   \n')
					say('Vision restarting now!  ')
					beep(538,555)
					beep(438,444)
					beep(338,333)
					beep(238,222)
					beep(138,111)
					if platform.system() == 'Windows':
						os.system('shutdown /r /t 0')
					elif platform.system() != 'Windows':
						os.system('reboot now')

				elif buttonpress == 9:
					say('Vision powering down! ')
					print('\n   VIsION Powering Down ...   \n')
					beep(538,555)
					beep(438,444)
					beep(338,333)
					beep(238,222)
					beep(138,111)
					if platform.system() == 'Windows':
						os.system('cls')
						os.system('shutdown /s /t 0')
					elif platform.system() != 'Windows':
						os.system('clear')
						os.system('shutdown -h now')

			else:
				break

		elif time.time() > maintimelimit:
			say('Waiting for selection!  ')
			print('\n   Waiting for Selection ...   \n')
			if platform.system() == 'Windows':
				os.system('cls')
			elif platform.system() != 'Windows':
				os.system('clear')
			break


if __name__ == "__main__":
	import os
	if platform.system() == 'Windows':
		os.system('cls')
	elif platform.system() != 'Windows':
		os.system('clear')
	main()
