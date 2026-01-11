#!/usr/bin/env python3
"""
Match transcript segments from markdown with timestamps from Premiere project.
Since we don't have direct transcript text in Premiere, we'll use clip timing
and create a mapping based on segment order and estimated durations.
"""
import xml.etree.ElementTree as ET
import gzip
import re
from pathlib import Path

def parse_premiere_ticks(ticks_str):
    """Convert Premiere ticks to seconds.
    Premiere uses 254016000000 ticks per hour at 25.4 fps base rate.
    """
    if not ticks_str:
        return None
    try:
        ticks = int(ticks_str)
        # Base rate: 254016000000 ticks/hour = 25.4 * 3600 * 1000000 / 100
        # Actually: ticks are in 1/254016000000 of an hour
        seconds = (ticks / 254016000000) * 3600
        return seconds
    except:
        return None

def format_timestamp(seconds):
    """Format seconds as MM:SS or HH:MM:SS"""
    if seconds is None:
        return None
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"

def extract_clip_timings(prproj_path):
    """Extract all clip timing information from Premiere project"""
    with gzip.open(prproj_path, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
    
    clips = []
    
    def find_clips(elem):
        """Find ClipTrackItem elements with timing"""
        # Look for clips on tracks
        if 'ClipTrackItem' in elem.tag or ('Clip' in elem.tag and 'Item' in elem.tag):
            clip = {
                'start_ticks': None,
                'end_ticks': None,
                'start': None,
                'end': None,
                'duration': None,
                'name': None
            }
            
            for child in elem.iter():
                if child.tag == 'Start' and child.text:
                    clip['start_ticks'] = child.text
                    clip['start'] = parse_premiere_ticks(child.text)
                elif child.tag == 'End' and child.text:
                    clip['end_ticks'] = child.text
                    clip['end'] = parse_premiere_ticks(child.text)
                elif child.tag == 'Duration' and child.text:
                    clip['duration'] = parse_premiere_ticks(child.text)
                elif child.tag == 'Name' and child.text:
                    name = child.text.strip()
                    if len(name) > 3:
                        clip['name'] = name
            
            if clip['start'] is not None or clip['end'] is not None:
                clips.append(clip)
        
        for child in elem:
            find_clips(child)
    
    find_clips(root)
    
    # Filter and sort valid clips
    valid_clips = [c for c in clips if c['start'] is not None and c['start'] >= 0 and c['start'] < 7200]  # Less than 2 hours
    valid_clips.sort(key=lambda x: x['start'] if x['start'] else float('inf'))
    
    return valid_clips

def parse_markdown_segments(md_path):
    """Parse markdown file to extract segments"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = []
    current_segment = None
    
    # Find all <segment> blocks
    segment_pattern = r'<segment topic="([^"]+)">(.*?)</segment>'
    
    for match in re.finditer(segment_pattern, content, re.DOTALL):
        topic = match.group(1)
        segment_content = match.group(2).strip()
        
        # Extract text content (remove markdown cards)
        # Remove card blocks
        text = re.sub(r'<card>.*?</card>', '', segment_content, flags=re.DOTALL)
        # Remove markdown links
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove markdown formatting
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^\*]+)\*', r'\1', text)
        # Clean up whitespace
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        segments.append({
            'topic': topic,
            'text': text,
            'raw': segment_content
        })
    
    # Also extract sections
    section_pattern = r'^## (.+?)$\n(.*?)(?=^## |\Z)'
    for match in re.finditer(section_pattern, content, re.MULTILINE | re.DOTALL):
        section_title = match.group(1)
        section_content = match.group(2).strip()
        
        # Skip if already captured as segment
        if not any(seg['topic'] == section_title for seg in segments):
            text = re.sub(r'<card>.*?</card>', '', section_content, flags=re.DOTALL)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
            text = re.sub(r'\n+', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            
            segments.append({
                'topic': section_title,
                'text': text,
                'raw': section_content
            })
    
    return segments

def estimate_duration(text):
    """Estimate duration based on text length (average speaking rate ~150 words/min)"""
    word_count = len(text.split())
    # Assume ~2.5 words per second (150 words/min)
    return word_count / 2.5

def create_timestamp_mapping(segments, clips):
    """Create timestamp mapping for segments using clip timings"""
    if not clips:
        # Fallback: estimate timestamps based on text length
        current_time = 0
        result = []
        for seg in segments:
            duration = estimate_duration(seg['text'])
            result.append({
                'topic': seg['topic'],
                'text': seg['text'],
                'start': format_timestamp(current_time),
                'start_seconds': current_time,
                'duration': duration
            })
            current_time += duration
        return result
    
    # Use clip timings - map segments to clips
    result = []
    clip_idx = 0
    
    for seg in segments:
        if clip_idx < len(clips):
            clip = clips[clip_idx]
            result.append({
                'topic': seg['topic'],
                'text': seg['text'][:200] + '...' if len(seg['text']) > 200 else seg['text'],
                'start': format_timestamp(clip['start']),
                'start_seconds': clip['start'],
                'end': format_timestamp(clip['end']) if clip['end'] else None,
                'duration': (clip['end'] - clip['start']) if (clip['end'] and clip['start']) else estimate_duration(seg['text'])
            })
            clip_idx += 1
        else:
            # Fallback for remaining segments
            duration = estimate_duration(seg['text'])
            last_time = result[-1]['start_seconds'] + result[-1]['duration'] if result else 0
            result.append({
                'topic': seg['topic'],
                'text': seg['text'][:200] + '...' if len(seg['text']) > 200 else seg['text'],
                'start': format_timestamp(last_time),
                'start_seconds': last_time,
                'duration': duration
            })
    
    return result

def main():
    prproj_path = Path('/Users/rainerh/programming/ng-news-1/ng-news 26-01.prproj')
    md_path = Path('/Users/rainerh/programming/ng-news-1/26-01.md')
    
    print("Extracting clip timings from Premiere project...")
    clips = extract_clip_timings(prproj_path)
    print(f"Found {len(clips)} clips with timing\n")
    
    if clips:
        print("First 10 clips:")
        for i, clip in enumerate(clips[:10], 1):
            start_str = format_timestamp(clip['start']) if clip['start'] else 'N/A'
            print(f"  {i}. {start_str}")
    
    print("\nParsing markdown segments...")
    segments = parse_markdown_segments(md_path)
    print(f"Found {len(segments)} segments\n")
    
    print("Creating timestamp mapping...")
    mapping = create_timestamp_mapping(segments, clips)
    
    print("\n" + "="*80)
    print("TIMESTAMP MAPPING")
    print("="*80 + "\n")
    
    for item in mapping:
        print(f"[{item['start']}] {item['topic']}")
        print(f"  {item['text']}")
        if item.get('end'):
            print(f"  End: {item['end']}")
        print()

if __name__ == '__main__':
    main()

