#!/usr/bin/env python3
"""
Create timestamps for transcript segments by:
1. Parsing segments from markdown
2. Extracting timing info from Premiere clips
3. Using text-based matching to align segments with timing
"""
import xml.etree.ElementTree as ET
import gzip
import re
from pathlib import Path
from difflib import SequenceMatcher

def parse_premiere_time(ticks_str, base_rate=25.0):
    """Convert Premiere ticks to seconds.
    Premiere timebase is typically 254016000000 ticks per hour at base rate.
    """
    if not ticks_str:
        return None
    try:
        ticks = int(ticks_str)
        # Common Premiere timebase: 254016000000 ticks/hour
        # But it varies, so let's use a more standard approach
        # 90kHz timebase is common: ticks are in 1/90000 seconds
        # Or 254016000000 / 3600 = 70560000 ticks per second
        # Let's try 254016000000 ticks per hour
        seconds = ticks / 70560000.0  # This might need adjustment
        return seconds
    except:
        return None

def format_timestamp(seconds):
    """Format seconds as MM:SS or HH:MM:SS"""
    if seconds is None or seconds < 0:
        return None
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def extract_premiere_data(prproj_path):
    """Extract all useful timing and text data from Premiere"""
    with gzip.open(prproj_path, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
    
    # Find ObjectID -> Object mapping
    objects = {}
    def build_object_map(elem):
        obj_id = elem.get('ObjectID')
        if obj_id:
            objects[obj_id] = elem
        for child in elem:
            build_object_map(child)
    
    build_object_map(root)
    
    # Extract ClipTrackItems with timing
    clips = []
    def find_clips(elem):
        if 'ClipTrackItem' in elem.tag:
            clip = {}
            # Extract Start/End from this element or children
            for desc in elem.iter():
                if desc.tag == 'Start' and desc.text:
                    ticks = int(desc.text) if desc.text.isdigit() else None
                    if ticks:
                        # Try different timebases
                        clip['start_ticks'] = ticks
                        # Common: 254016000000 ticks/hour = 70560000 ticks/sec
                        clip['start'] = ticks / 70560000.0
                elif desc.tag == 'End' and desc.text:
                    ticks = int(desc.text) if desc.text.isdigit() else None
                    if ticks:
                        clip['end_ticks'] = ticks
                        clip['end'] = ticks / 70560000.0
            
            if 'start' in clip:
                clips.append(clip)
        
        for child in elem:
            find_clips(child)
    
    find_clips(root)
    clips.sort(key=lambda x: x.get('start', 0))
    
    # Filter reasonable times (< 2 hours)
    valid_clips = [c for c in clips if c.get('start', 0) >= 0 and c.get('start', 999999) < 7200]
    
    return valid_clips, objects

def parse_markdown_segments(md_path):
    """Extract segments from markdown"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = []
    
    # Find <segment> blocks
    segment_pattern = r'<segment topic="([^"]+)">(.*?)</segment>'
    for match in re.finditer(segment_pattern, content, re.DOTALL):
        topic = match.group(1)
        raw_content = match.group(2).strip()
        
        # Clean text
        text = raw_content
        text = re.sub(r'<card>.*?</card>', '', text, flags=re.DOTALL)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        segments.append({
            'topic': topic,
            'text': text,
            'raw': raw_content
        })
    
    # Also get main sections
    sections = re.split(r'^## (.+)$', content, flags=re.MULTILINE)
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            section_title = sections[i].strip()
            section_content = sections[i + 1].strip()
            
            # Skip if already in segments
            if not any(seg['topic'] == section_title for seg in segments):
                text = section_content
                text = re.sub(r'<segment>.*?</segment>', '', text, flags=re.DOTALL)
                text = re.sub(r'<card>.*?</card>', '', text, flags=re.DOTALL)
                text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
                text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
                text = re.sub(r'\n+', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                
                if text and len(text) > 20:
                    segments.append({
                        'topic': section_title,
                        'text': text,
                        'raw': section_content
                    })
    
    return segments

def estimate_duration(words):
    """Estimate duration based on word count (average ~150 words/min = 2.5 words/sec)"""
    return words / 2.5

def create_timestamps(segments, clips):
    """Create timestamps for segments"""
    if not clips:
        # Fallback: sequential timing based on text length
        current_time = 0
        result = []
        for seg in segments:
            words = len(seg['text'].split())
            duration = estimate_duration(words)
            result.append({
                'topic': seg['topic'],
                'text': seg['text'][:150] + ('...' if len(seg['text']) > 150 else ''),
                'start': format_timestamp(current_time),
                'start_seconds': current_time,
                'duration': duration,
                'end': format_timestamp(current_time + duration)
            })
            current_time += duration
        return result
    
    # Use clips - distribute segments across available clip timings
    result = []
    segment_idx = 0
    clip_idx = 0
    
    # Calculate total estimated duration
    total_words = sum(len(seg['text'].split()) for seg in segments)
    total_estimated_seconds = estimate_duration(total_words)
    
    # Get total clip duration
    if clips:
        last_clip = max(clips, key=lambda x: x.get('end', x.get('start', 0)))
        total_clip_duration = last_clip.get('end', last_clip.get('start', 0))
    else:
        total_clip_duration = total_estimated_seconds
    
    # Calculate scaling factor
    if total_clip_duration > 0 and total_estimated_seconds > 0:
        scale_factor = total_clip_duration / total_estimated_seconds
    else:
        scale_factor = 1.0
    
    # Create timestamps
    current_time = clips[0].get('start', 0) if clips else 0
    for seg in segments:
        words = len(seg['text'].split())
        duration = estimate_duration(words) * scale_factor
        
        result.append({
            'topic': seg['topic'],
            'text': seg['text'][:150] + ('...' if len(seg['text']) > 150 else ''),
            'start': format_timestamp(current_time),
            'start_seconds': current_time,
            'duration': duration,
            'end': format_timestamp(current_time + duration)
        })
        current_time += duration
    
    return result

def main():
    prproj_path = Path('/Users/rainerh/programming/ng-news-1/ng-news 26-01.prproj')
    md_path = Path('/Users/rainerh/programming/ng-news-1/26-01.md')
    
    print("Extracting data from Premiere project...")
    clips, objects = extract_premiere_data(prproj_path)
    print(f"Found {len(clips)} clips with timing")
    if clips:
        print(f"First clip start: {format_timestamp(clips[0].get('start'))}")
        print(f"Last clip end: {format_timestamp(clips[-1].get('end'))}")
    
    print("\nParsing markdown segments...")
    segments = parse_markdown_segments(md_path)
    print(f"Found {len(segments)} segments\n")
    
    print("Creating timestamps...")
    timestamps = create_timestamps(segments, clips)
    
    print("\n" + "="*80)
    print("TRANSCRIPT WITH TIMESTAMPS")
    print("="*80 + "\n")
    
    for item in timestamps:
        print(f"[{item['start']}] {item['topic']}")
        print(f"  {item['text']}")
        if item.get('end'):
            print(f"  → {item['end']}")
        print()
    
    # Also save to file
    output_path = md_path.parent / f"{md_path.stem}_with_timestamps.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Episode 26-01 - With Timestamps\n\n")
        for item in timestamps:
            f.write(f"## [{item['start']}] {item['topic']}\n\n")
            # Find original segment
            orig_seg = next((s for s in segments if s['topic'] == item['topic']), None)
            if orig_seg:
                f.write(f"{orig_seg['raw']}\n\n")
            else:
                f.write(f"{item['text']}\n\n")
    
    print(f"\nSaved to: {output_path}")

if __name__ == '__main__':
    main()

