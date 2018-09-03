import apiclient.discovery
import apiclient.errors
from googleapiclient.discovery import build
from oauth2client.tools import argparser
import configparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

inifile = configparser.ConfigParser()
inifile.read('./settings.ini', 'UTF-8')
token = inifile.get('GoogleDataAPI', 'token')
DEVELOPER_KEY = token
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def search(channel_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified
    #  query term.
    search_response = youtube.search().list(
        part='id,snippet',
        maxResults=1,
        channelId=channel_id,
        order='date'
    ).execute()
    video = []

    # Add each result to the appropriate list, and then display the lists of
    #  matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            video.append(search_result["snippet"]["title"])
            video.append("https://www.youtube.com/watch?v=%s" % (search_result["id"]["videoId"]))
    return video

