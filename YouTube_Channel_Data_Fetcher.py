import csv
import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Function to fetch videos from a YouTube channel
def fetch_videos(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.search().list(
            part='snippet', channelId=channel_id, maxResults=50, type='video', order='date'
        )
        videos = []
        while request:
            response = request.execute()
            for item in response['items']:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                print(f"Fetching details for video: {video_title} (ID: {video_id})")
                video_data = fetch_video_details(api_key, video_id)
                if video_data:  # Ensure data is valid before appending
                    videos.append(video_data)
            request = youtube.search().list_next(request, response)
        return videos
    except HttpError as e:
        print(f"An error occurred while fetching videos: {e}")
        return []

# Function to fetch specific details of each video
def fetch_video_details(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        )
        response = request.execute()
        for item in response['items']:
            video_details = {
                'id': item['id'],
                'title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'views': item['statistics']['viewCount'],
                'likes': item['statistics'].get('likeCount', '0'),
                'comments': item['statistics'].get('commentCount', '0')
            }
            print(f"Video details retrieved: {video_details['title']}")
            return video_details
    except HttpError as e:
        print(f"Failed to fetch details for video ID {video_id}: {e}")
        return {}

# Write videos data to CSV file
def write_to_csv(videos, filename='videos.csv'):
    if videos:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'title', 'published_at', 'views', 'likes', 'comments']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(videos)
            print(f"Data successfully written to {filename}.")
    else:
        print("No data to write to file.")

# Main function to run the script
def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <channel_id>")
        sys.exit(1)

    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("API Key is not found. Please set the YOUTUBE_API_KEY environment variable.")
        sys.exit(1)

    channel_id = sys.argv[1]
    print(f"Starting video fetch for channel ID: {channel_id}")
    videos = fetch_videos(api_key, channel_id)
    write_to_csv(videos)

if __name__ == '__main__':
    main()
