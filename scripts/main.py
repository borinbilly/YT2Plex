#!/mnt/user/appdata/xteve/scripts/yt2p/bin/python3

import os
import subprocess
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Replace with your own API key
API_KEY = 'INSERT API KEY HERE'

# List of channels, Channel IDs via https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/
#icon should be links to images you want displayed in Plex for each channel
channels = [
    {
        'id': 'UCeY0bbntWzzVIaj2z3QigXg',
        'name': 'NBC',
        'icon': 'https://yt3.googleusercontent.com/Iyl3USdPKmYU1klQW1El44iCAsRZtfHobgBkIhdwm8sjgZXIfsVttGob8_cTXhU1rSWIMUEDaw=s900-c-k-c0x00ffffff-no-rj'
    },
     {
         'id': 'UC52X5wxOL_s5yw0dQk7NtgA',
         'name': 'AP',
         'icon': 'https://yt3.googleusercontent.com/eYjjY5MUJ422vBuGFg--wNR1b093BaAFzJhbZYLhp8rye5gcwXyPQAtNz2j_4wXSf-Qc5J3UsA=s160-c-k-c0x00ffffff-no-rj'
    },
     {
         'id': 'UCyUTC3jCAaLd639lo9n9Bqw',
         'name': 'CAFE',
         'icon': 'https://yt3.googleusercontent.com/kj9VngnbnhkmZrqHJPnxvbh7KaNkLp_UYu3UMI-7G1FoPsRqwObpgRWAhi1gbZ4_vEIW15Yuhw=s160-c-k-c0x00ffffff-no-rj'
     },
    # Add more channels here
    # {
    #     'id': 'CHANNEL_ID_2',
    #     'name': 'CHANNEL_NAME_2',
    #     'icon': 'CHANNEL_ICON_2'
    # },
]

# Build the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

output_dir = '/mnt/user/appdata/xteve/scripts/'

# Create M3U and XMLTV file content placeholders
m3u_content = "#EXTM3U\n"
xmltv_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'

for channel in channels:
    CHANNEL_ID = channel['id']
    CHANNEL_NAME = channel['name']
    CHANNEL_ICON = channel['icon']

    # Search for live broadcasts on the specified channel
    request = youtube.search().list(
        part='snippet',
        channelId=CHANNEL_ID,
        eventType='live',
        type='video'
    )
    response = request.execute()

    # Extract live stream URL from the response
    live_stream_url = None
    if 'items' in response and len(response['items']) > 0:
        live_stream_url = f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"

    if live_stream_url:
        print(f"Live stream URL for {CHANNEL_NAME}: {live_stream_url}")

        # Fetch HLS stream URL using yt-dlp
        try:
            result = subprocess.run(
                ['/mnt/user/appdata/xteve/scripts/yt2p/bin/yt-dlp', '-g', live_stream_url],
                capture_output=True,
                text=True,
                check=True
            )
            hls_url = result.stdout.strip()
            print(f"HLS Stream URL for {CHANNEL_NAME}: {hls_url}")

            if hls_url:
                # Append to M3U file content
                m3u_content += f"""#EXTINF:-1 tvg-id="{CHANNEL_ID}" tvg-name="{CHANNEL_NAME}" tvg-logo="{CHANNEL_ICON}", {CHANNEL_NAME}
{hls_url}
"""

                # Append to XMLTV file content
                current_time = datetime.utcnow()
                program_start = current_time.strftime('%Y%m%d%H%M%S +0000')
                program_end = (current_time + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')  # Assuming a 1-hour program

                xmltv_content += f"""    <channel id="{CHANNEL_ID}">
        <display-name>{CHANNEL_NAME}</display-name>
        <icon src="{CHANNEL_ICON}"/>
    </channel>
    <programme start="{program_start}" stop="{program_end}" channel="{CHANNEL_ID}">
        <title>{CHANNEL_NAME} Live Stream</title>
        <desc>Live stream from {CHANNEL_NAME} on YouTube</desc>
    </programme>
"""
            else:
                print(f"No valid HLS stream URL found for {CHANNEL_NAME}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch HLS URL for {CHANNEL_NAME}: {e}")
    else:
        print(f"No live stream found for {CHANNEL_NAME}.")

# Finalize XMLTV content
xmltv_content += '</tv>'

# Save M3U file
m3u_path = os.path.join(output_dir, 'playlist.m3u')
with open(m3u_path, 'w') as m3u_file:
    m3u_file.write(m3u_content)
print(f"M3U file created: {m3u_path}")

# Save XMLTV file
xmltv_path = os.path.join(output_dir, 'guide.xml')
with open(xmltv_path, 'w') as xmltv_file:
    xmltv_file.write(xmltv_content)
print(f"XMLTV file created: {xmltv_path}")

