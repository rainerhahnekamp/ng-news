#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import sys
import gzip
import re
from datetime import timedelta

def parse_timecode(tc_str):
    """Parse Premiere timecode format (ticks or timecode string)"""
    if not tc_str:
        return None
    # Try to parse as ticks (integer)
    try:
        ticks = int(tc_str)
        # Premiere uses 254016000000 ticks per hour (25.4 fps * 60 * 60 * 1000000)
        # Actually it's more complex, but let's try simple conversion
        hours = ticks / (25.4 * 3600 * 1000000)
        return hours * 3600  # Convert to seconds
    except:
        pass
    
    # Try to parse as timecode string (HH:MM:SS:FF or similar)
    match = re.match(r'(\d+):(\d+):(\d+):(\d+)', tc_str)
    if match:
        h, m, s, f = map(int, match.groups())
        return h * 3600 + m * 60 + s + f / 25.4
    return None

def format_timecode(seconds):
    """Format seconds as MM:SS or HH:MM:SS"""
    if seconds is None:
        return None
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def extract_transcript_data(xml_file):
    """Extract transcript clips with their timing and text"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    transcripts = []
    
    def process_transcript_clip(elem):
        """Process a TranscriptClip element"""
        clip_data = {
            'start_ticks': None,
            'end_ticks': None,
            'start': None,
            'end': None,
            'text': None,
            'name': None
        }
        
        # Traverse all children to find properties
        for child in elem.iter():
            if child.tag == 'Start' and child.text:
                clip_data['start_ticks'] = child.text
                clip_data['start'] = parse_timecode(child.text)
            elif child.tag == 'End' and child.text:
                clip_data['end_ticks'] = child.text
                clip_data['end'] = parse_timecode(child.text)
            elif child.tag == 'Text' and child.text:
                clip_data['text'] = child.text.strip()
            elif child.tag == 'Name' and child.text:
                clip_data['name'] = child.text.strip()
        
        if clip_data['start_ticks'] or clip_data['text']:
            transcripts.append(clip_data)
    
    def find_transcript_clips(elem):
        """Find all TranscriptClip elements"""
        if 'TranscriptClip' in elem.tag:
            process_transcript_clip(elem)
        for child in elem:
            find_transcript_clips(child)
    
    find_transcript_clips(root)
    
    # Sort by start time
    transcripts.sort(key=lambda x: x['start'] if x['start'] else 0)
    
    return transcripts

def extract_clip_timings(xml_file):
    """Extract timing from ClipTrackItem elements"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    clips = []
    
    def process_clip(elem):
        clip_data = {
            'start': None,
            'end': None,
            'name': None
        }
        
        for child in elem.iter():
            if child.tag == 'Start' and child.text:
                clip_data['start'] = parse_timecode(child.text)
            elif child.tag == 'End' and child.text:
                clip_data['end'] = parse_timecode(child.text)
            elif child.tag == 'Name' and child.text and len(child.text.strip()) > 3:
                clip_data['name'] = child.text.strip()
        
        if clip_data['start'] is not None:
            clips.append(clip_data)
    
    def find_clips(elem):
        if 'ClipTrackItem' in elem.tag or ('Clip' in elem.tag and 'Track' in elem.tag):
            process_clip(elem)
        for child in elem:
            find_clips(child)
    
    find_clips(root)
    clips.sort(key=lambda x: x['start'] if x['start'] else 0)
    return clips

if __name__ == '__main__':
    prproj_file = '/Users/rainerh/programming/ng-news-1/ng-news 26-01.prproj'
    
    with gzip.open(prproj_file, 'rt', encoding='utf-8') as f:
        transcripts = extract_transcript_data(f)
        f.seek(0)
        clips = extract_clip_timings(f)
    
    print(f"Found {len(transcripts)} transcript clips")
    print(f"Found {len(clips)} clip items with timing\n")
    
    print("=== Transcript Clips ===")
    for i, t in enumerate(transcripts[:20], 1):
        start_str = format_timecode(t['start']) if t['start'] else 'N/A'
        end_str = format_timecode(t['end']) if t['end'] else 'N/A'
        print(f"{i}. {start_str} - {end_str}")
        if t['text']:
            print(f"   Text: {t['text'][:100]}")
        if t['name']:
            print(f"   Name: {t['name']}")
        print()
    
    print("\n=== Clip Items (first 20) ===")
    for i, c in enumerate(clips[:20], 1):
        start_str = format_timecode(c['start']) if c['start'] else 'N/A'
        end_str = format_timecode(c['end']) if c['end'] else 'N/A'
        print(f"{i}. {start_str} - {end_str}: {c['name']}")

