from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import datetime
import time
import os.path


def trimVideo(filename):
	print("Choose which part of the video to keep. The rest of the video will be cut off")

	start_time = input("[+] Start time (HH:MM:SS): ")
	end_time = input("[+] End time (HH:MM:SS): ")

	try:
		x = time.strptime(start_time, "%H:%M:%S")
		start_seconds = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

		y = time.strptime(end_time, "%H:%M:%S")
		end_seconds = datetime.timedelta(hours=y.tm_hour,minutes=y.tm_min,seconds=y.tm_sec).total_seconds()

		ffmpeg_extract_subclip(filename, start_seconds, end_seconds, targetname=filename.split(".ts")[0]+"_trimmed.ts")
		return True

	except Exception as e:
		print("[!!] ERROR - %s"%e)
		return False