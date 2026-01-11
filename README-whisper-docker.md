# Whisper Docker Setup

This Docker setup runs OpenAI Whisper locally with ffmpeg support for audio/video transcription.

## Build the Docker Image

```bash
docker build -t ng-news-whisper .
```

Or use docker-compose:

```bash
docker-compose build
```

## Usage

### Option 1: Run with docker-compose (Recommended)

```bash
# Start interactive container
docker-compose run --rm whisper bash

# Inside the container, transcribe files:
whisper audio.mp3 --model base --output_format srt
```

### Option 2: Run with docker directly

```bash
# Run interactive container
docker run -it --rm \
  -v $(pwd):/workspace \
  ng-news-whisper

# Or run a single command
docker run -it --rm \
  -v $(pwd):/workspace \
  ng-news-whisper \
  whisper audio.mp3 --model base --output_format srt
```

### Option 3: Run transcription directly (non-interactive)

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  ng-news-whisper \
  whisper episode-26-01.mp3 \
    --model base \
    --output_format srt \
    --output_dir /workspace
```

## Available Models

Whisper models (from smallest/fastest to largest/most accurate):

- `tiny` - Fastest, least accurate
- `base` - Good balance (recommended for most use cases)
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Best accuracy, slowest

**Example with different model:**

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  ng-news-whisper \
  whisper audio.mp3 --model large --output_format srt
```

## Output Formats

Supported output formats:

- `txt` - Plain text
- `vtt` - WebVTT
- `srt` - SubRip
- `tsv` - Tab-separated values
- `json` - JSON with timestamps

**Example generating multiple formats:**

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  ng-news-whisper \
  whisper audio.mp3 \
    --model base \
    --output_format all \
    --output_dir /workspace
```

## Language Specification

By default, Whisper auto-detects the language. To specify a language:

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  ng-news-whisper \
  whisper audio.mp3 \
    --model base \
    --language en \
    --output_format srt
```

## Complete Example for ng-news Episode

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  ng-news-whisper \
  whisper episode-26-01.mp3 \
    --model base \
    --language en \
    --output_format all \
    --output_dir /workspace \
    --verbose
```

This will generate:

- `episode-26-01.srt` - SubRip subtitles
- `episode-26-01.vtt` - WebVTT subtitles
- `episode-26-01.txt` - Plain text transcript
- `episode-26-01.tsv` - Tab-separated values
- `episode-26-01.json` - Full JSON with timestamps

## Notes

- Audio/video files must be in the workspace directory (mounted volume)
- Output files will be saved in the workspace directory
- First run will download the model (~140MB for base, ~1.5GB for large)
- Models are cached in Docker image for faster subsequent runs
- For GPU support, use `nvidia-docker` instead of `docker`
