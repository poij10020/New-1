import pandas as pd
import requests
from time import sleep

# Define your credentials and parameters
access_token = 'EAAOAouTfDpsBOzh6FvqZAl1W4Lk6mUSoNjhaA6hSSEhKfqQCEAQLJsMFNiIZBJritSNyK3MSfOy3Y18Jdj837yYb6Ox6LKQ7LuEvTZB1RxPqUm8aLSGZArNZChoNhSRewZAkSVI2IZCZBupXGGu8vHR9t2xPQq19jA0ZCVZB7SjWltyQxfl3es0zCa51tKSRZCW9lsZD'
page_id = '247607515094289'

def upload_video_to_facebook(video_url, description):
    # Construct the Google Drive file URL for download
    file_id = video_url.split('/')[-2]  # Extract file ID from URL
    file_url = f'https://drive.google.com/uc?export=download&id={file_id}'

    # Download the video file
    video_file_path = '/content/video.mp4'
    response = requests.get(file_url)
    with open(video_file_path, 'wb') as file:
        file.write(response.content)

    # Define the Facebook API URL for video upload
    upload_url = f'https://graph.facebook.com/v20.0/{page_id}/videos'

    # Upload the video to Facebook
    with open(video_file_path, 'rb') as video_file:
        upload_response = requests.post(upload_url, files={'file': video_file}, data={
            'access_token': access_token,
            'description': description
        })

    # Check the response
    if upload_response.status_code == 200:
        print(f'Video uploaded successfully from URL: {video_url}')
    else:
        print(f'Error uploading video from URL {video_url}: {upload_response.text}')

def process_csv_and_upload(csv_file_path):
    df = pd.read_csv(csv_file_path)
    for _, row in df.iterrows():
        video_url = row['video_url']
        description = row['description'] if 'description' in row else 'Default description'
        upload_video_to_facebook(video_url, description)
        sleep(120)  # Wait for 2 minutes before uploading the next video

# Path to your CSV file
csv_file_path = 'drive (4).csv'

process_csv_and_upload(csv_file_path)
