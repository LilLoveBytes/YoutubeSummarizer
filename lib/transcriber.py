import re
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


def get_video_transcript(video_id):
  pattern = r'\[.*?\]'
  response = YouTubeTranscriptApi.get_transcript(video_id)
  transcripts = [item['text'] for item in response]
  transcripts_string = re.sub(pattern, '', ''.join(transcripts))
  return transcripts_string

def summarize_transcript(api_key, transcript):
  client = OpenAI(api_key=api_key)
  prompt = 'Please summarize the transcript below into bullet points \n---\n"{0}"'.format(transcript)
  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      temperature=0.1,
      max_tokens=1000,
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
  return response.choices[0].message.content
