## Twitch Stream Highlights to YT Automatic Uploader (AutoBot Clipper)

This script can be used to automatically extract highlights (or clips) from a twitch stream (with rewind enabled) and then upload the same to a YouTube channel. It can be used to completely automate a twitch highlights channel.

It needs the following manual input to work:
1. Provide timestamps of the clip to be extracted from a stream.
2. Set the title, description, tags and privacy status of the video when uploading to YouTube


## Setup
Clone the script

    git clone https://github.com/teja156/autobot-clipper

Install the requirements with pip

    pip install -r requirements.txt

## YouTube API Setup

You need to first create an account on Google Cloud Platform in-order to use the YouTube Data API v3 (which is required to programatically upload videos to YouTube). Follow these steps to do so:
1.  Create an account on the  [Google Developers Console](https://console.developers.google.com/)
2.  Register a new app there
3.  Enable the Youtube API (APIs & Services -> Enable APIs and Services)
4. Go to APIs & Services -> OAuth Consent screen.
5. Configure your App name, developer email, etc and go to **Scopes**
6. Add the scope '**youtube.upload**', and then 'Save and Continue'
7. Add the email address of the channel in 'Test Users' and Save.
8.  Create Client ID (APIs & Services -> Credentials -> Create Credentials), select 'Oauth client ID', select type 'Web application'
9.  Add an 'Authorized redirect URI' of '[https://localhost:8080/oauth2callback](http://localhost:8080/oauth2callback)'
10.  Download the client secrets JSON file (click download icon next to newly created client ID) and save it as file  `client_secrets.json`  in the same directory as the script.

## Run
1. First run `config.py` to authenticate your channel with YouTube API. This will create a file named **credentials.txt** in the same directory. You only need to run this once.
 `python config.py`
2. Run `bot.py` to start the script. 
`python bot.py`

***NOTE:*** For *Twitch VOD URL*, make sure you enter the URL of the video and not the live stream. For example, `https://twitch.tv/shroud` is an invalid input, you must enter something like `https://www.twitch.tv/videos/1088769006` 
You can find the VOD URL by going to `https://twitch.tv/username/videos` and open the most recent video, this is same as the current live stream but here you can also rewind the stream. However, the vod will be available in the videos page only if the streamer enables "*past broadcasts*" option on his/her channel.

If your video belongs to any category other than Gaming, you need to mention the appropriate category ID. You can find the list of categoy IDs [here.](https://gist.github.com/dgp/1b24bf2961521bd75d6c)

You can also use a constant description for all your uploads by changing the text in ***constdesc.txt*** file. The credits text will be automatically appended to the description while uploading the video. You can also specify hashtags to include in the description.
 

### Using YouTube Upload Utility Manually
You can also upload a video manually with `ytupload_util.py`

    python ytupload_util.py
Fill the required inputs (video file, title, description, tags, privacy status) and the video will be uploaded!
