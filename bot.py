# Input Twitch vod URL
# Input timestamps of the clip
# Retrieve the clip from the twitch live stream
# Show the clip for preview
# Open Video trimmer for editting the clip
# Input Title, Description, Tags
# Input credits
# Upload to YT
# Show YT link


import os
import os.path
import re
import sys
from datetime import datetime
import pytz
import videotrim_util
import ytupload_util
import webbrowser
import time


default_description = ""
default_categoryId = "20"

try:
	f=open("constdesc.txt")
	default_description=f.read()
	f.close()
except Exception as e:
	default_description=""



def credits():
	print("[~] Written by Teja Swaroop (https://techraj156.com)")
	print("[~] Thanks to streamlink CLI (https://streamlink.github.io)")
	print()


def checks():
	# check if client_secret.json and credentials.txt files are present
	if not os.path.isfile("client_secrets.json"):
		print("[!] Client Secret file is missing. Make sure you download it from your GCP dashboard and place it in the current directory")
		sys.exit(0)

	if not os.path.isfile("credentials.txt"):
		# Trigger flask server to enable use to authenticate with their account
		print("[!] credentials.txt is missing!")
		print("[!] You need to initially authenticate with your Google Account so that the video can be uploaded to your channel. Don't worry, you only need to do this once.")
		print("[-] Run config.py to authenticate with your google account and create credentials.txt")

def validateInput(inp, pattern):
	if re.search(pattern, inp):
		return True
	return False


def getOffsetAndDuration(start_time, end_time):
	start_do = datetime.strptime(start_time, "%H:%M:%S")
	end_do = datetime.strptime(end_time, "%H:%M:%S")
	offset = start_time
	duration = str(end_do-start_do).split(".")[0]
	return [offset,duration]


def getTwitchClip(creator_name, twitch_url, offset, duration):
	print("[*] Getting clip from Twitch Live Stream with streamlink..")
	# Use Streamlink to get the clip
	filename = os.path.join("clips",creator_name+(datetime.now(pytz.timezone('Asia/Kolkata'))).strftime("%m%d%Y-%H_%M_%S")+".ts")

	cmd = "streamlink %s best --hls-start-offset %s --hls-duration %s -o %s"%(twitch_url,offset,duration,filename)
	print("[*] %s"%cmd)
	os.system(cmd)
	return filename
	

def main():
	credits()
	creator_name = input("[+] Twitch Creator name: ").replace(" ","")
	twitch_url = input("[+] Twitch VOD URL: ")
	if not validateInput(twitch_url,r"^https://www.twitch.tv/videos/.*$"):
		print("[!] Bad Input. Make sure you input twitch VOD URL and not the live stream URL.")
		sys.exit()
	start_time = input("[+] Clip Start time (HH:MM:SS): ")
	if not validateInput(start_time,r"^[0-9][0-9]:[0-6][0-9]:[0-6][0-9]$"):
		print("[!] Bad Input. Make sure you follow the input format correctly.")
		sys.exit()
	end_time = input("[+] Clip End time (HH:MM:SS): ")
	if not validateInput(end_time,r"^[0-9][0-9]:[0-6][0-9]:[0-6][0-9]$"):
		print("[!] Bad Input. Make sure you follow the input format correctly.")
		sys.exit()


	offset, duration = getOffsetAndDuration(start_time, end_time)


	if not os.path.isdir("clips"):
		os.mkdir("clips")


	filename = getTwitchClip(creator_name, twitch_url, offset, duration)

	# Check if the download is successful
	if os.path.isfile(filename):
		print("[*] Downloaded clip succesfully! - %s"%filename)
	else:
		print("[!] Download failed!")
		sys.exit(0)


	print("[*] Opening clip in video player..")
	os.startfile(filename)

	op = input("[+] Do you want to trim the video? (Y/n): ")
	if(op in ["Y","y",""]):
		# Open video trimming util
		if (videotrim_util.trimVideo(filename)):
			print("[*] Video trimmed successfully!")
			filename = filename.split(".ts")[0]+"_trimmed.ts"
		else:
			print("[!] Video trim failed!")
			op = input("Do you want to (E)xit or (C)ontinue?")
			if op in ["E","e",""]:
				sys.exit()

	elif op in ["N","n"]:
		# Do not open video trimming util
		pass


	op = input("[+] Upload to YouTube? (Y/n): ")

	if op in ["Y","y",""]:
		# Upload created clip to YT

		yt_title = input("[+] Video Title: ")
		yt_description = input("[+] Video Description (leave empty for default description): ")
		yt_tags = input("[+] Video Tags (seperated by comas): ")
		yt_categoryId = input("[+] Category ID (Leave empty for Gaming): ")
		yt_privacyStatus = input("[+] Privacy Status (public/private/unlisted): ")
		yt_credits = input("[+] Credits for Original Creator: ")

		if yt_title=="":
			print("[!] Title can't be empty")

		if yt_privacyStatus.lower() not in ["public","private","unlisted"]:
			print("[!] Invalid privacy status")

		if yt_description=="":
			yt_description = default_description

		if yt_categoryId=="":
			yt_categoryId = default_categoryId


		yt_description+="\n"+"Credits: \n"+yt_credits

		print("[*] Uploading video to YouTube. This might take a while..be patient, do not close the script.")
		videoId = ytupload_util.upload(filename, yt_title, yt_description, yt_tags, yt_categoryId, yt_privacyStatus)
		
		if videoId is not None:
			print("[*] Succesfully uploaded video. ")
			print("[*] https://www.youtube.com/watch?v=%s"%videoId)

		else:
			print("[!] Video upload failed.")
			


if __name__ == "__main__":
	checks()
	main()





