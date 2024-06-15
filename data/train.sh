#!/bin/bash

CHANNEL_URL="https://www.youtube.com/@TomBilyeu"

# Function to log messages
log() {
  local message="$1"
  echo "$(date +'%Y-%m-%d %H:%M:%S') - $message"
}

log "Starting script"

# Extract channel name from the CHANNEL_URL
channel_name=$(echo "$CHANNEL_URL" | sed 's|.*@||' | sed 's|/.*||' | sed 's/ /_/g')
log "Channel name: $channel_name"

TRANSCRIPT_DIR="transcripts/$channel_name"
METADATA_FILE="$TRANSCRIPT_DIR/metadata.json"

# Ensure transcript directory exists
log "Creating transcript directory: $TRANSCRIPT_DIR"
mkdir -p "$TRANSCRIPT_DIR"

# Initialize metadata JSON file
log "Initializing metadata file: $METADATA_FILE"
echo "[]" > "$METADATA_FILE"

# Get all video URLs from the channel
log "Fetching video URLs from channel: $CHANNEL_URL"
video_infos=$(yt-dlp -j --flat-playlist "$CHANNEL_URL" 2>&1)

# Check for errors
if echo "$video_infos" | grep -q "ERROR"; then
  log "Failed to fetch video information: $video_infos"
  exit 1
fi

# Loop through each video URL
log "Processing video URLs"
echo "$video_infos" | jq -c '. | {id: .id, title: .title, url: ("https://www.youtube.com/watch?v=" + .id)}' | while read -r video_info; do
  log "Processing video info: $video_info"

  video_id=$(echo "$video_info" | jq -r '.id')
  video_title=$(echo "$video_info" | jq -r '.title' | sed 's/[^a-zA-Z0-9]/_/g')
  video_url=$(echo "$video_info" | jq -r '.url')
  log "Video ID: $video_id, Title: $video_title, URL: $video_url"

  # Get the transcript using yt-dlp
  log "Fetching transcript for video: $video_url"
  transcript=$(yt-dlp --write-auto-sub --skip-download "$video_url" -o "$TRANSCRIPT_DIR/${video_id}_${video_title}.vtt" 2>&1)

  if [ -z "$transcript" ]; then
    log "No transcript available for $video_url"
    continue
  fi

  # Save transcript to a JSON file
  transcript_file="$TRANSCRIPT_DIR/${video_id}_${video_title}.json"
  log "Saving transcript to file: $transcript_file"
  echo "$transcript" | jq -R -s '{transcript: .}' > "$transcript_file"

  # Append metadata to metadata.json
  log "Appending metadata to $METADATA_FILE"
  metadata=$(echo "$video_info" | jq --arg transcript_file "$transcript_file" '. + {transcript_file: $transcript_file}')
  echo "$metadata" >> "$METADATA_FILE"
done

# Save all data in JSONL format
log "Saving all data in JSONL format to $METADATA_FILE"
jq -c '.[]' "$METADATA_FILE" > "${METADATA_FILE%.json}_all.jsonl"

log "Script completed"
