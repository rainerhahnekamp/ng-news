#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import gzip
from pathlib import Path

prproj_path = Path('ng-news 26-01.prproj')

with gzip.open(prproj_path, 'rt', encoding='utf-8') as f:
    tree = ET.parse(f)
    root = tree.getroot()

# Look for any elements that have both Name and Start/Time properties
marker_candidates = []

def search_for_markers(elem, path='', depth=0, max_depth=15):
    if depth > max_depth:
        return
    
    name_val = None
    time_val = None
    comment_val = None
    
    for child in elem:
        if child.tag == 'Name' and child.text and child.text.strip():
            name_val = child.text.strip()
        elif child.tag in ['Start', 'Time', 'In', 'InPoint', 'StartTime'] and child.text:
            try:
                time_val = int(child.text)
            except:
                pass
        elif child.tag in ['Comment', 'Description'] and child.text:
            comment_val = child.text.strip()
    
    # If we have both name and time, it might be a marker
    if name_val and time_val is not None:
        child_tags = [c.tag for c in elem]
        simple_tags = ['Name', 'Start', 'Time', 'In', 'Comment', 'Description', 'Node', 'Properties']
        is_simple = all(tag in simple_tags for tag in child_tags)
        
        if is_simple or len(child_tags) < 10:
            marker_candidates.append({
                'name': name_val,
                'time_ticks': time_val,
                'time_seconds': time_val / 70560000.0,
                'comment': comment_val,
                'tag': elem.tag,
                'path': path,
                'child_count': len(child_tags)
            })
    
    for child in elem:
        new_path = f"{path}/{elem.tag}" if path else elem.tag
        search_for_markers(child, new_path, depth+1, max_depth)

search_for_markers(root)

# Filter reasonable markers (between 0 and video duration)
valid_markers = [m for m in marker_candidates if 0 <= m['time_seconds'] < 600]

print(f"Found {len(valid_markers)} potential markers:")
if valid_markers:
    for i, m in enumerate(sorted(valid_markers, key=lambda x: x['time_seconds']), 1):
        mins = int(m['time_seconds'] // 60)
        secs = int(m['time_seconds'] % 60)
        print(f"{i}. {mins:02d}:{secs:02d} - '{m['name']}' (tag: {m['tag']})")
else:
    print("No markers found. Make sure:")
    print("  1. Markers are added to the timeline (press M or right-click)")
    print("  2. Markers are on the main sequence")
    print("  3. The project file is saved after adding markers")

