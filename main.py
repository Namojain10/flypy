import numpy as np
import time
import cv2
import os
import imutils
import subprocess
from gtts import gTTS 
import pyttsx3
import pyttsx3
import speech_recognition as sr 
import webbrowser as Web 
import pywhatkit
import winsound 
import requests
from geopy.distance import great_circle 
from geopy.geocoders import Nominatim
import geocoder
from art import *
import datetime


def say(text):
    engine = pyttsx3.init('sapi5')
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.setProperty('rate',100)
    print("  ")
    print(f"flypy : {text}")
    engine.say(text=text)
    engine.runAndWait()
    print("  ")
def realtime():

	
	LABELS = open("coco.names").read().strip().split("\n")
	print("[INFO] loading YOLO from disk...")
	net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "..\jarvis\yolov3.weights")

	ln = net.getLayerNames()
	ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

	
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

	frame_count = 0
	start = time.time()
	first = True
	frames = []

	while True:
		frame_count += 1
		
		ret, frame = cap.read()
		frame = cv2.flip(frame,1)
		frames.append(frame)

		if frame_count == 300:
			break
		if ret:
			
			key = cv2.waitKey(1)
			
			if frame_count % 60 == 0:
				end = time.time()
				
				(H, W) = frame.shape[:2]
				blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
					swapRB=True, crop=False)
				net.setInput(blob)
				layerOutputs = net.forward(ln)
				boxes = []
				confidences = []
				classIDs = []
				centers = []

				for output in layerOutputs:
					for detection in output:
						scores = detection[5:]
						classID = np.argmax(scores)
						confidence = scores[classID]
						if confidence > 0.5:
							box = detection[0:4] * np.array([W, H, W, H])
							(centerX, centerY, width, height) = box.astype("int")
							x = int(centerX - (width / 2))
							y = int(centerY - (height / 2))
							w = int(width)
							h = int(height)
							boxes.append([x, y, int(width), int(height)])
							confidences.append(float(confidence))
							classIDs.append(classID)
					
							centers.append((centerX, centerY))
							
							frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,250,0), 1)
							cv2.imshow("Live Detection", frame)

				idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

				texts = []
				if len(idxs) > 0:
					for i in idxs.flatten():
						centerX, centerY = centers[i][0], centers[i][1]
						
						if centerX <= W/3:
							W_pos = "left "
						elif centerX <= (W/3 * 2):
							W_pos = "center "
						else:
							W_pos = "right "
						
						if centerY <= H/3:
							H_pos = "top "
						elif centerY <= (H/3 * 2):
							H_pos = "mid "
						else:
							H_pos = "bottom "
				
						texts.append(H_pos + W_pos + LABELS[classIDs[i]])
					
				
				print(texts)
				say(texts)
	cap.release()
	cv2.destroyAllWindows()
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,0,5)
    try:
        print("Recognizing..")
        query = r.recognize_google(audio,language="en-in")
        print(f"You Said : {query}")
    except:
        return
    query = str(query)
    return query.lower()
def beep(duration=500) :
	frequency = 2500  # Set Frequency To 2500 Hertz
	winsound.Beep(frequency, duration)
def Taskexe():
	def play():
		playname=listen()
	
		pywhatkit.playonyt(playname)
	def Mylocation():
		ip_add = requests.get('https://api.ipify.org').text
		url = 'https://get.geojs.io/v1/ip/geo/'+ip_add+'.json'
		geo_q=requests.get(url)
		geo_d=geo_q.json()
		state=geo_d['city']
		country =geo_d['country']
		say(f"you are in {state,country}")
	def googlemaps(Place):
		URL="https://www.google.com/maps/place/"+str(Place)
		geolocator = Nominatim(user_agent="myGeocoder")
		location = geolocator.geocode(Place, addressdetails=True)
		target_latlon=location.latitude , location.longitude
		location = location.raw['address']
		target = {'city': location.get('city',' '),
					'state':location.get('state',''),
					'country': location.get('country','')}
		current_loca = geocoder.ip('me')
		current_latlon = current_loca.latlng
		distance = str(great_circle(current_latlon,target_latlon))
		distance=str(distance.split(' ',1)[0])
		distance=int(float(distance))
		Web.open(url=URL)
		say(target)
		say(f"sir,{Place} is {distance} km  away from your location")
	
	while True:
		try:
			query=listen()
			if "hello" in query:
				beep() 
				say("welcome to fly py third eye of your life")
			elif "how are you" in query:
				beep()
				say("i am fine what about you?")
			elif "i am fine" in query:
				beep()
				say("Great")
			elif "i am not well" in query:
				beep()
				say("take break")
				break
			elif "youtube search" in query:
				beep()
				say("this is what i found")
				query=query.replace("youtube search"," ")
				query=query.replace("fly py"," ")
				web="https://www.youtube.com/results?search_query="+ query
				Web.open(web)
				say("done")
			elif "google search" in query:
				beep()
				say("this is what i found")
				query=query.replace("google search"," ")
				query=query.replace("flypy"," ")
				pywhatkit.search(query)
				say("done")

			elif "detection" in query:
				beep()
				say("fly py starts real time detection ")
				query = realtime()
				say("done")
			elif "bye" in query:
				say("have a nice day")
				break
			elif "time" in query:
				time_Ac =datetime.datetime.now()
				now=time_Ac.strftime("%H:%M")
				say(now)

			elif "play" in query:
				say("tell me your song name")
				beep()
				play()
			elif "where is " in query :
				beep()
				query=query.replace("where is"," ")
				googlemaps(query)
			elif "location" in query :
				beep()
				Mylocation()
			elif "  " in query :
				say("TAKING BREAK")
				break
			elif "owner" in query:
				say("Namo and team is my owner")
			elif "alarm" in query :
				say("say the time")
				time=listen()
				while True:
					time_Ac =datetime.datetime.now()
					now=time_Ac.strftime("%H%M")
					if now==time:
						say("time to wake up")
						beep()
					elif now>time:
						break


			else:
				say("not a valid command")
		except TypeError:
			say('going to sleep')
			break

tprint("Ocular Saorga", font="rounded")
tprint("By  FLY PY", font="rounded")
say("Welcome to fly py third eye of your life")
beep()
Taskexe()
