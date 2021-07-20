# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/guides/code_samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os

import google_auth_oauthlib.flow
import google.oauth2.credentials

import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
import ast

scopes = ["https://www.googleapis.com/auth/youtube.upload"]
default_description = "Thanks for watching. Please Subscribe."
default_categoryId = "20"

def upload(filename, title, description, tags, categoryId, privacyStatus):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"


    try:
        body=dict(snippet=dict(title=title,description=description,tags=tags,
            categoryId=categoryId
        ),
        status=dict(privacyStatus=privacyStatus))

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)


        f = open('credentials.txt','r')
        creds = ast.literal_eval(f.read())
        f.close()
        credentials = google.oauth2.credentials.Credentials(**creds)
        # credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.videos().insert(
            notifySubscribers=True,
            part=",".join(body.keys()),
            body=body,
            
            # TODO: For this request to work, you must replace "YOUR_FILE"
            #       with a pointer to the actual file you are uploading.
            media_body=MediaFileUpload(filename)
        )
        response = request.execute()
        print(response)
        # videoId = ast.literal_eval(response)['id']
        videoId = response['id']
        return videoId

    except Exception as e:
        print("[!!] ERROR - %s"%e)
        return None



def manual_upload():
    filename = input("[+] File path: ")
    yt_title = input("[+] Video Title: ")
    yt_description = input("[+] Video Description (leave empty for default description)")
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


    yt_description+="\n"+yt_credits

    upload(filename, yt_title, yt_description, yt_tags, yt_categoryId, yt_privacyStatus)


if __name__ == "__main__":
    manual_upload()