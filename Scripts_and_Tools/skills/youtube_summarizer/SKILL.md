---
name: youtube_summarizer
description: A skill to summarize YouTube videos using their transcripts.
---

# YouTube Summarizer

This skill allows you to summarize YouTube videos.

## Usage

When the user asks to summarize a YouTube video (provided via URL or ID), use this skill.

## Steps

1.  Identify the YouTube Video URL or ID.
2.  Run the python script `scripts/get_transcript.py` with the URL/ID as an argument.
3.  Capture the output (transcript).
4.  Summarize the transcript in a bulleted list, highlighting key points.

## Example

User: "Summarize this video https://www.youtube.com/watch?v=dQw4w9WgXcQ"
Agent: Runs `python scripts/get_transcript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ`
Agent: (Reads output)
Agent: "Here is the summary of the video..."
