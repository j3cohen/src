import sys
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_channel_id_by_name(api_key, name):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.channels().list(
            part='id',
            forUsername=name  # Use 'forUsername' if you know the username
        )
        response = request.execute()
        if 'items' in response and response['items']:
            return response['items'][0]['id']
        else:
            return None
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None

def search_channel_by_keyword(api_key, keyword):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.search().list(
            part='snippet',
            q=keyword,  # Search query
            type='channel',  # Look for channels only
            maxResults=1
        )
        response = request.execute()
        print(response)  # Print the entire response
        if 'items' in response and response['items']:
            return response['items'][0]['snippet']['channelId']
        else:
            return None
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python YouTube_Get_Channel_Id.py <mode> <name_or_keyword>")
        sys.exit(1)

    mode = sys.argv[1].lower()
    name_or_keyword = sys.argv[2]
    api_key = os.getenv('YOUTUBE_API_KEY')

    if not api_key:
        print("API Key not found. Please set the YOUTUBE_API_KEY environment variable.")
        sys.exit(1)

    if mode == 'name':
        channel_id = get_channel_id_by_name(api_key, name_or_keyword)
    elif mode == 'keyword':
        channel_id = search_channel_by_keyword(api_key, name_or_keyword)
    else:
        print("Invalid mode. Use 'name' or 'keyword'.")
        sys.exit(1)

    if channel_id:
        print(f"Channel ID for '{name_or_keyword}': {channel_id}")
    else:
        print(f"No channel found for the specified {mode} '{name_or_keyword}'.")

if __name__ == '__main__':
    main()
