#!/usr/bin/env python3
"""
Generate timestamps for level 2 headings (##) in markdown file.
Uses markers from Premiere project or estimates duration based on text length.
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_time(timestamp_str):
    """Parse timestamp string like '52:00' or '1:23:45' to seconds"""
    parts = timestamp_str.split(':')
    if len(parts) == 2:  # MM:SS or could be just seconds in MM:SS format
        minutes = int(parts[0])
        seconds = int(parts[1])
        # If minutes > 60, it's likely meant to be seconds (e.g., 52:00 = 52 seconds, not 52 minutes)
        if minutes > 60:
            # Treat as seconds:seconds format (likely error, interpret as MM:SS)
            # But if first part > 60 and second is 00, treat first as seconds
            if seconds == 0 and minutes < 3600:
                return minutes  # 52:00 = 52 seconds
            return minutes * 60 + seconds
        return minutes * 60 + seconds
    elif len(parts) == 3:  # HH:MM:SS
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return None

def format_time(seconds):
    """Format seconds as MM:SS or HH:MM:SS"""
    if seconds is None or seconds < 0:
        return None
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def estimate_speech_duration(text):
    """Estimate speech duration based on text (average 150 words/min = 2.5 words/sec)"""
    words = len(text.split())
    return int(words / 2.5)  # Return integer seconds

def extract_premiere_markers(prproj_path):
    """Extract markers from Premiere project file"""
    try:
        import gzip
        with gzip.open(prproj_path, 'rt', encoding='utf-8') as f:
            tree = ET.parse(f)
            root = tree.getroot()
    except:
        return []
    
    markers = []
    
    def find_markers(elem, depth=0):
        if depth > 20:
            return
        
        tag_lower = elem.tag.lower()
        classid = elem.get('ClassID', '').lower()
        
        # Look for marker elements - various possible names/classids
        is_marker = ('marker' in tag_lower or 
                     'marker' in classid or
                     tag_lower.endswith('marker') or
                     classid.endswith('marker'))
        
        # Also look for elements with Name + Time/Start properties (common marker structure)
        has_name = False
        has_time = False
        marker_data = {
            'name': None,
            'time_ticks': None,
            'time_seconds': None,
            'comment': None
        }
        
        for child in elem:
            if child.tag == 'Name' and child.text:
                marker_data['name'] = child.text.strip()
                has_name = True
            elif child.tag in ['Start', 'Time', 'In', 'InPoint', 'StartTime'] and child.text:
                try:
                    ticks = int(child.text)
                    marker_data['time_ticks'] = ticks
                    # Premiere timebase: 254016000000 ticks/hour = 70560000 ticks/second
                    marker_data['time_seconds'] = ticks / 70560000.0
                    has_time = True
                except:
                    pass
            elif child.tag in ['Comment', 'Description'] and child.text:
                marker_data['comment'] = child.text.strip()
        
        # If it's explicitly a marker OR has name+time properties, it's likely a marker
        if is_marker or (has_name and has_time):
            # Check if it's actually a marker (not a clip or other element)
            # Markers typically don't have too many nested properties
            child_count = len(list(elem))
            if child_count < 20:  # Markers are simpler structures
                if marker_data['time_seconds'] is not None:
                    markers.append(marker_data)
        
        for child in elem:
            find_markers(child, depth+1)
    
    find_markers(root)
    
    # Filter and sort by time
    valid_markers = [m for m in markers if m['time_seconds'] is not None and 0 <= m['time_seconds'] < 7200]
    valid_markers.sort(key=lambda x: x['time_seconds'])
    
    # Remove duplicates (same time)
    unique_markers = []
    seen_times = set()
    for m in valid_markers:
        time_int = int(m['time_seconds'])
        if time_int not in seen_times:
            seen_times.add(time_int)
            unique_markers.append(m)
    
    return unique_markers

def parse_level2_headings(md_path):
    """Extract all level 2 headings (##) and their content"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = []
    
    # Find all level 2 headings
    heading_pattern = r'^## (.+)$'
    headings = list(re.finditer(heading_pattern, content, re.MULTILINE))
    
    # Find existing timestamps in the file
    existing_timestamps = {}
    
    # Pattern 1: [Audio clip at 52: ...]
    pattern1 = r'\[.*?at\s+(\d+:\d+)(?::\d+)?'
    for match in re.finditer(pattern1, content, re.IGNORECASE):
        time_str = match.group(1)
        pos = match.start()
        existing_timestamps[pos] = parse_time(time_str)
    
    # Pattern 2: timestamp: 52:00
    pattern2 = r'timestamp:\s*(\d+:\d+(?::\d+)?)'
    for match in re.finditer(pattern2, content, re.IGNORECASE):
        time_str = match.group(1)
        pos = match.start()
        existing_timestamps[pos] = parse_time(time_str)
    
    # Extract content for each heading
    for i, heading_match in enumerate(headings):
        heading_title = heading_match.group(1).strip()
        heading_pos = heading_match.start()
        
        # Get content from this heading to the next heading (or end of file)
        if i + 1 < len(headings):
            next_heading_pos = headings[i + 1].start()
            section_content = content[heading_match.end():next_heading_pos].strip()
        else:
            section_content = content[heading_match.end():].strip()
        
        # Clean text for duration estimation
        text = section_content
        # Remove card blocks
        text = re.sub(r'<card>.*?</card>', '', text, flags=re.DOTALL)
        # Remove segment blocks (keep content, just remove tags)
        text = re.sub(r'<segment[^>]*>', '', text, flags=re.DOTALL)
        text = re.sub(r'</segment>', '', text)
        # Remove markdown links (keep text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove bold/italic
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^\*]+)\*', r'\1', text)
        # Remove code blocks
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Clean up whitespace
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Check if this section has a timestamp IMMEDIATELY after the heading
        # (within first 100 characters), not buried in the content
        section_timestamp = None
        for pos, ts in existing_timestamps.items():
            # Only use timestamp if it's very close to the heading start (within 100 chars)
            # This avoids using internal reference timestamps
            if heading_pos <= pos <= heading_pos + 100:
                section_timestamp = ts
                break
        
        sections.append({
            'title': heading_title,
            'content': section_content,
            'text': text,
            'position': heading_pos,
            'existing_timestamp': section_timestamp,
            'duration': estimate_speech_duration(text)
        })
    
    return sections

def generate_timestamps(sections, video_duration_seconds=340, markers=None):
    """Generate timestamps for sections
    video_duration_seconds: Total video duration (default 5:40 = 340 seconds)
    markers: List of markers from Premiere project (optional)
    """
    if not sections:
        return []
    
    # Add Introduction at 0:00
    intro_duration = 15
    introduction = {
        'title': 'Introduction',
        'text': 'Episode introduction',
        'start_seconds': 0,
        'duration': intro_duration,
        'calculated_time': 0,
        'existing_timestamp': None
    }
    
    # Use all markers as timestamps - match them sequentially to sections
    if markers and len(markers) > 0:
        # Sort markers by time
        sorted_markers = sorted(markers, key=lambda x: x['time_seconds'])
        
        print(f"\nUsing {len(sorted_markers)} markers as timestamps:")
        for i, marker in enumerate(sorted_markers):
            print(f"  Marker {i+1}: {format_time(marker['time_seconds'])} - {marker['name'] or '(unnamed)'}")
        
        # Match markers to sections sequentially:
        # - First marker: Introduction (if exists) or first section
        # - Remaining markers: match to sections in order
        # - Last marker might be Goodbye or last section
        
        marker_idx = 0
        
        # If first marker is at 0 or very close, use it for Introduction
        if sorted_markers and sorted_markers[0]['time_seconds'] <= 2:
            introduction['calculated_time'] = int(sorted_markers[0]['time_seconds'])
            marker_idx = 1
        
        # Match remaining markers to sections in order
        for section in sections:
            if marker_idx < len(sorted_markers):
                marker = sorted_markers[marker_idx]
                section['calculated_time'] = int(marker['time_seconds'])
                section['marker_name'] = marker['name']
                marker_idx += 1
        
        # If there are more markers than sections, the last one might be for Goodbye
        if marker_idx < len(sorted_markers):
            last_marker = sorted_markers[marker_idx]
            goodbye['calculated_time'] = int(last_marker['time_seconds'])
            goodbye['marker_name'] = last_marker['name']
        
        # Fill in any sections that didn't get markers
        for section in sections:
            if 'calculated_time' not in section:
                # Find previous section's end time
                prev_time = intro_duration + 2
                for prev_section in sections:
                    if prev_section == section:
                        break
                    if 'calculated_time' in prev_section:
                        prev_time = prev_section['calculated_time'] + prev_section['duration'] + 2
                
                section['calculated_time'] = prev_time
    
    # Fallback: Generate sequential timestamps
    goodbye_duration = 15
    current_time = intro_duration + 2
    
    # Calculate total time needed
    total_content_duration = sum(sec['duration'] for sec in sections)
    total_gaps = (len(sections) - 1) * 2
    available_time = video_duration_seconds - intro_duration - goodbye_duration - total_gaps - 4
    
    # Scale if needed to fit video duration
    if total_content_duration > available_time:
        scale_factor = available_time / total_content_duration
        for sec in sections:
            sec['duration'] = int(sec['duration'] * scale_factor)
        total_content_duration = sum(sec['duration'] for sec in sections)
    
    # Assign sequential times
    for section in sections:
        if 'calculated_time' not in section:
            section['calculated_time'] = current_time
        current_time = section['calculated_time'] + section['duration'] + 2
        # Cap at video duration
        if current_time > video_duration_seconds - goodbye_duration - 2:
            break
    
    # Add Goodbye at the end (within video duration)
    last_section_end = sections[-1]['calculated_time'] + sections[-1]['duration']
    goodbye_time = min(last_section_end + 2, video_duration_seconds - goodbye_duration)
    goodbye = {
        'title': 'Goodbye',
        'text': 'Episode closing',
        'start_seconds': goodbye_time,
        'duration': goodbye_duration,
        'calculated_time': goodbye_time,
        'existing_timestamp': None
    }
    
    # Generate result with Introduction first
    result = [{
        'title': introduction['title'],
        'text': introduction['text'],
        'start': format_time(introduction['calculated_time']),
        'start_seconds': introduction['calculated_time'],
        'duration': introduction['duration'],
        'end': format_time(introduction['calculated_time'] + introduction['duration']),
        'has_anchor': False
    }]
    
    # Add all sections
    for section in sections:
        start_time = section['calculated_time']
        end_time = start_time + section['duration']
        
        result.append({
            'title': section['title'],
            'text': section['text'][:200] + ('...' if len(section['text']) > 200 else ''),
            'start': format_time(start_time),
            'start_seconds': start_time,
            'duration': section['duration'],
            'end': format_time(end_time),
            'has_anchor': section['existing_timestamp'] is not None
        })
    
    # Add Goodbye at the end
    result.append({
        'title': goodbye['title'],
        'text': goodbye['text'],
        'start': format_time(goodbye['calculated_time']),
        'start_seconds': goodbye['calculated_time'],
        'duration': goodbye['duration'],
        'end': format_time(goodbye['calculated_time'] + goodbye['duration']),
        'has_anchor': False
    })
    
    return result

def main():
    # Script should be run from the 26-01 folder or specify paths
    # Default to looking for files in parent/26-01 directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    episode_dir = project_root / '26-01'
    
    # Default to 26-01 episode, but could be made configurable
    md_path = episode_dir / '26-01.md'
    prproj_path = episode_dir / 'ng-news 26-01.prproj'
    
    print("Parsing level 2 headings from markdown...")
    sections = parse_level2_headings(md_path)
    print(f"Found {len(sections)} level 2 headings:\n")
    for sec in sections:
        print(f"  - {sec['title']} ({sec['duration']}s estimated)")
    
    # Extract markers from Premiere project
    print("\nExtracting markers from Premiere project...")
    markers = extract_premiere_markers(prproj_path)
    if markers:
        print(f"Found {len(markers)} markers - will use ALL of them as timestamps!")
        print("Markers will be matched sequentially to: Introduction, sections, Goodbye")
        for m in markers:
            print(f"  - {format_time(m['time_seconds'])}: {m['name'] or '(unnamed)'}")
    else:
        print("No markers found yet.")
        print("\n📝 To use markers:")
        print("  1. Add markers in Premiere at the start of each section")
        print("  2. Add them in this order:")
        print("     - First marker: Introduction (at 0:00 or start of video)")
        print("     - Next markers: One for each section in order")
        print("     - Last marker: Goodbye (optional)")
        print("  3. Marker names don't matter - they'll be matched sequentially!")
        print("  4. Save the Premiere project and run this script again")
    
    # Check for existing timestamps
    anchored = [s for s in sections if s['existing_timestamp']]
    if anchored:
        print(f"\nFound {len(anchored)} sections with existing timestamps:")
        for sec in anchored:
            print(f"  - {sec['title']}: {format_time(sec['existing_timestamp'])}")
    
    print("\nGenerating timestamps...")
    # Video duration: 5:40 = 340 seconds
    VIDEO_DURATION = 340
    timestamps = generate_timestamps(sections, VIDEO_DURATION, markers)
    
    print("\n" + "="*80)
    print("YOUTUBE TIMESTAMP FORMAT")
    print("="*80 + "\n")
    
    for item in timestamps:
        print(f"{item['start']} {item['title']}")
    
    # Save enhanced markdown with timestamps in headings
    output_path = md_path.parent / f"{md_path.stem}_with_timestamps.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        with open(md_path, 'r', encoding='utf-8') as orig:
            content = orig.read()
        
        # Replace each level 2 heading with timestamped version
        for item in timestamps:
            # Find the heading in the original content
            heading_pattern = f'^## {re.escape(item["title"])}$'
            replacement = f'## [{item["start"]}] {item["title"]}'
            content = re.sub(heading_pattern, replacement, content, flags=re.MULTILINE)
        
        f.write(content)
    
    print(f"\n✅ Saved timestamps to: {output_path}")
    print(f"\nTotal duration: {format_time(timestamps[-1]['start_seconds'] + timestamps[-1]['duration'])}")

if __name__ == '__main__':
    main()
