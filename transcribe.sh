#!/bin/bash

# Whisper Transcription Script for ng-news
# Usage: ./transcribe.sh <mp4-file>
# Example: ./transcribe.sh episode-26-01.mp4

set -e

# Check if file argument is provided
if [ -z "$1" ]; then
    echo "❌ Error: No file specified"
    echo ""
    echo "Usage: ./transcribe.sh <mp4-file>"
    echo "Example: ./transcribe.sh episode-26-01.mp4"
    exit 1
fi

INPUT_FILE="$1"

# Check if file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: File not found: $INPUT_FILE"
    exit 1
fi

# Extract filename without extension for output naming
FILENAME=$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//')

echo "🎙️  Transcribing: $INPUT_FILE"
echo "📝 Output filename: $FILENAME"
echo ""

# Run Whisper in Docker
docker run -it --rm \
  -v "$(pwd):/workspace" \
  ng-news-whisper \
  whisper "/workspace/$INPUT_FILE" \
    --model base \
    --language en \
    --output_format all \
    --output_dir "/workspace" \
    --verbose

echo ""
echo "✅ Transcription complete!"
echo "📊 Generated files:"
echo "   - $FILENAME.srt"
echo "   - $FILENAME.vtt"
echo "   - $FILENAME.txt"
echo "   - $FILENAME.json"
echo "   - $FILENAME.tsv"
