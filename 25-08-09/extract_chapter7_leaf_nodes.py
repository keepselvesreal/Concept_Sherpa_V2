#!/usr/bin/env python3
"""
Chapter 7 Leaf Node Text Extraction Script
Extracts text for each leaf node based on start/end markers
"""

import json
import os
import re

def clean_text(text):
    """Clean extracted text by removing unnecessary whitespace and formatting"""
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Remove trailing whitespace from each line
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    return text.strip()

def extract_text_between_markers(full_text, start_marker, end_marker):
    """Extract text between start and end markers"""
    
    # Find start position
    start_pos = full_text.find(start_marker)
    if start_pos == -1:
        print(f"Warning: Start marker not found: {start_marker[:100]}...")
        return ""
    
    # Start extraction from after the start marker
    start_pos += len(start_marker)
    
    # Find end position
    end_pos = full_text.find(end_marker, start_pos)
    if end_pos == -1:
        print(f"Warning: End marker not found: {end_marker[:100]}...")
        # If no end marker, extract to end of text
        extracted = full_text[start_pos:]
    else:
        extracted = full_text[start_pos:end_pos]
    
    return clean_text(extracted)

def main():
    # File paths
    source_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md"
    leaf_nodes_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/chapter7_basic_data_validation_leaf_nodes.json"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/chapter7_leaf_nodes"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the source text
    print("Reading source file...")
    with open(source_file, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # Read leaf nodes configuration
    print("Loading leaf nodes configuration...")
    with open(leaf_nodes_file, 'r', encoding='utf-8') as f:
        leaf_nodes = json.load(f)
    
    print(f"Found {len(leaf_nodes)} leaf nodes to process")
    
    # Process each leaf node
    results = []
    for i, node in enumerate(leaf_nodes):
        node_id = node['id']
        title = node['title']
        level = node['level']
        start_text = node['start_text']
        end_text = node['end_text']
        
        print(f"\nProcessing node {i+1}/{len(leaf_nodes)}: {title}")
        
        # Extract text for this node
        if start_text and end_text:
            extracted_text = extract_text_between_markers(full_text, start_text, end_text)
            
            if extracted_text:
                # Create output filename
                safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')
                filename = f"{node_id:03d}_{safe_title}.md"
                output_path = os.path.join(output_dir, filename)
                
                # Create content with metadata
                content = f"# {title}\n\n"
                content += f"**Node ID:** {node_id}\n"
                content += f"**Level:** {level}\n"
                content += f"**Source:** Chapter 7 - Basic data validation\n\n"
                content += "---\n\n"
                content += extracted_text
                
                # Save to file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                results.append({
                    'node_id': node_id,
                    'title': title,
                    'output_file': filename,
                    'text_length': len(extracted_text),
                    'status': 'success'
                })
                
                print(f"  ✓ Extracted {len(extracted_text)} characters")
                print(f"  ✓ Saved to: {filename}")
            else:
                results.append({
                    'node_id': node_id,
                    'title': title,
                    'status': 'failed - no text extracted'
                })
                print(f"  ✗ Failed to extract text")
        else:
            results.append({
                'node_id': node_id,
                'title': title,
                'status': 'skipped - no start/end markers'
            })
            print(f"  - Skipped (no start/end markers)")
    
    # Save extraction summary
    summary = {
        'source_file': source_file,
        'total_nodes': len(leaf_nodes),
        'successful_extractions': len([r for r in results if r['status'] == 'success']),
        'failed_extractions': len([r for r in results if 'failed' in r['status']]),
        'skipped_extractions': len([r for r in results if 'skipped' in r['status']]),
        'output_directory': output_dir,
        'extraction_results': results
    }
    
    summary_path = os.path.join(output_dir, 'extraction_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Print final summary
    print(f"\n{'='*60}")
    print("EXTRACTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total nodes processed: {summary['total_nodes']}")
    print(f"Successful extractions: {summary['successful_extractions']}")
    print(f"Failed extractions: {summary['failed_extractions']}")
    print(f"Skipped extractions: {summary['skipped_extractions']}")
    print(f"Output directory: {output_dir}")
    print(f"Summary saved to: extraction_summary.json")
    
    if summary['failed_extractions'] > 0:
        print(f"\n⚠️  {summary['failed_extractions']} extractions failed. Check markers in leaf nodes JSON.")

if __name__ == "__main__":
    main()