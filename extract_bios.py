#!/usr/bin/env python3
"""
Extract candidate bios from Aggregate Mini Wiki.docx and save them as individual text files.
"""

from docx import Document
import os
import re

def extract_bios(docx_path, output_dir):
    """
    Extract bios from the Word document and save them as individual text files.
    Each bio is identified by a numbered format like "1. Name" or "2. Name"
    
    Args:
        docx_path: Path to the Word document
        output_dir: Directory to save the bio text files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the document
    doc = Document(docx_path)
    
    # Pattern to match numbered entries like "1. Adam Frisch" or "2. Tom Barrett"
    number_pattern = re.compile(r'^\d+\.\s+(.+)$')
    
    current_name = None
    current_bio = []
    bios_dict = {}
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Check if this line starts with a number pattern (e.g., "1. Name")
        match = number_pattern.match(text)
        
        if match:
            # This is a new candidate - save previous bio if exists
            if current_name and current_bio:
                bios_dict[current_name] = '\n\n'.join(current_bio).strip()
            
            # Start new bio
            current_name = match.group(1).strip()  # Extract the name after the number
            current_bio = []
            print(f"Found candidate: {current_name}")
        elif current_name:
            # This is part of the current bio
            current_bio.append(text)
    
    # Save the last bio
    if current_name and current_bio:
        bios_dict[current_name] = '\n\n'.join(current_bio).strip()
    
    print(f"\nFound {len(bios_dict)} candidate bios")
    
    # Save each bio to a file
    for name, bio in bios_dict.items():
        # Create filename from name (replace spaces with underscores, remove special chars)
        filename = name.replace(' ', '_').replace('.', '').replace(',', '')
        filename = re.sub(r'[^\w_-]', '', filename)
        filename = f"{filename}.txt"
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(bio)
        
        print(f"Saved: {filename}")
    
    print(f"\nTotal files saved: {len(bios_dict)}")
    return bios_dict

if __name__ == "__main__":
    docx_path = "Aggregate Mini Wiki.docx"
    output_dir = "bio"
    
    extract_bios(docx_path, output_dir)
