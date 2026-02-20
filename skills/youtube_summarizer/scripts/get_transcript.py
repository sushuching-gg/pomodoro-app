import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    if len(url) == 11:
        return url
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python get_transcript.py <youtube_url_or_id>")
        sys.exit(1)

    input_url = sys.argv[1]
    video_id = get_video_id(input_url)

    if not video_id:
        print(f"Error: Could not extract video ID from '{input_url}'")
        sys.exit(1)

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        # Convert FetchedTranscript object to list of dicts
        data = transcript.to_raw_data()
        
        # Manual formatting
        text = "\n".join([item['text'] for item in data])
        print(text)

    except Exception as e:
        print(f"Error fetching transcript: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
