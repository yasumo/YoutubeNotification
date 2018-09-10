from googleapiclient.discovery import build
import os
import traceback

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

DEVELOPER_KEY = os.environ['GOOGLEDATAAPI_TOKEN']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search(channel_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified
    #  query term.
    while True:
        try:
            search_response = youtube.search().list(
                part='id,snippet',
                fields='items(id,snippet/liveBroadcastContent)',
                maxResults=5,
                type='video',
                channelId=channel_id,
                order='date'
            ).execute()
            break
        except:
            print(traceback.format_exc())
            return []

    # Add each result to the appropriate list, and then display the lists of
    #  matching videos, channels, and playlists.
    ret_msgs = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            ret_msg = 'https://www.youtube.com/watch?v=%s' % (search_result['id']['videoId'])
            live_status = search_result['snippet']['liveBroadcastContent']
            if live_status == 'upcoming':
                ret_msg = '(upcoming) : '+ret_msg
            ret_msgs.append(ret_msg)
    return reversed(ret_msgs)

