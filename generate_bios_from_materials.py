#!/usr/bin/env python3
"""
Read materials.csv, update bio_name to bio/<Candidate>.txt, parse Aggregate Mini Wiki.docx for numbered entries,
match entries to candidate names from materials.csv (case/underscore differences allowed),
extract Educational Background, Career, and Personal information sections, and save per-candidate files to bio/.

Run from repository root where materials.csv and Aggregate Mini Wiki.docx live.
"""

import csv
import os
import re
from docx import Document

MATERIALS = "materials.csv"
DOCX = "Aggregate Mini Wiki.docx"
BIO_DIR = "bio"

SECTION_HEADINGS = [
    "Educational Background",
    "Education",
    "Career",
    "Professional Experience",
    "Personal information",
    "Personal Information",
    "Personal Info",
]

def normalize_name(s: str) -> str:
    # Lowercase, replace non-alphanumeric with underscore, collapse underscores
    s = s or ""
    s = s.strip()
    s = s.replace('\\u2019', "")  # drop fancy apostrophes if any
    s = re.sub(r"[.\\-]", "_", s)
    s = re.sub(r"\\s+", "_", s)
    s = re.sub(r"[^0-9a-zA-Z_]+", "", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_").lower()


def extract_candidate_name_from_path(path: str) -> str | None:
    # path like image/Adam_Frisch.jpeg -> Adam_Frisch
    if not path:
        return None
    base = os.path.basename(path)
    # remove extension
    name, _ext = os.path.splitext(base)
    return name


def read_materials(path=MATERIALS):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for r in reader:
            rows.append(dict(r))
    return headers, rows


def write_materials(headers, rows, path=MATERIALS):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def parse_docx_by_candidate_names(docx_path, candidate_names):
    """
    Search for each candidate name in the document and extract their bio.
    Names appear in underscore format like "Adam_Frisch".
    Returns a dict mapping normalized candidate name to (original_name, bio_text).
    """
    doc = Document(docx_path)
    
    # Get all text with paragraph indices
    all_paragraphs = []
    for idx, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        all_paragraphs.append((idx, text))
    
    mapping = {}
    
    for candidate in candidate_names:
        # The candidate name format matches the document format (underscore)
        # So we can search directly
        norm_candidate = normalize_name(candidate)
        
        # Find paragraph that exactly matches this candidate's name
        found_idx = None
        found_text = None
        
        for idx, text in all_paragraphs:
            # Check for exact match with candidate name
            if text == candidate:
                found_idx = idx
                found_text = text
                break
            # Also try with spaces instead of underscores
            elif text == candidate.replace('_', ' '):
                found_idx = idx
                found_text = text
                break
        
        if found_idx is None:
            # Try case-insensitive match
            for idx, text in all_paragraphs:
                if text.lower() == candidate.lower():
                    found_idx = idx
                    found_text = text
                    break
        
        if found_idx is None:
            continue
        
        # Extract bio content after this name
        # Bio consists of sections: Educational Background, Career, Personal Information
        # Stop when we hit another candidate name (a short line that's just a name)
        bio_lines = []
        
        # Known section headings that are NOT candidate names
        section_headings = ['Educational Background', 'Career', 'Personal Information']
        
        for idx in range(found_idx + 1, len(all_paragraphs)):
            text = all_paragraphs[idx][1]
            
            if not text:
                bio_lines.append('')
                continue
            
            # Don't stop at section headings
            if text in section_headings:
                bio_lines.append(text)
                continue
            
            # Check if this looks like another candidate name
            # Candidate names have underscores (like Adam_Frisch) or are short capitalized names
            if len(text) < 50:
                # If it has underscores, likely a candidate name
                if '_' in text:
                    words = text.replace('_', ' ').split()
                    if len(words) >= 2 and len(words) <= 5:
                        # This is likely another candidate, stop here
                        break
                # If it's just 2-3 capitalized words without underscores, might also be a candidate
                elif len(text.split()) >= 2 and len(text.split()) <= 4:
                    words = text.split()
                    capitalized = sum(1 for w in words if w and w[0].isupper())
                    # All words capitalized and not a known section = likely a candidate
                    if capitalized == len(words):
                        # This is likely another candidate, stop here
                        break
            
            bio_lines.append(text)
        
        bio_text = '\n'.join(bio_lines).strip()
        if bio_text:
            mapping[norm_candidate] = (found_text, bio_text)
    
    return mapping



def extract_sections_from_body(body_text: str) -> dict:
    """
    Extract the three sections: Educational Background, Career, and Personal information.
    Section headings do NOT have colons after them.
    """
    result = {"Educational Background":"", "Career":"", "Personal information":"", "full":""}
    result['full'] = body_text.strip()
    if not body_text:
        return result

    lines = body_text.splitlines()
    
    # Find section headings (exact match, case-insensitive, no colon)
    section_indices = []  # list of (line_idx, section_name)
    
    for idx, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Check for exact matches to section headings
        if re.match(r'^Educational\s+Background$', line_stripped, re.IGNORECASE):
            section_indices.append((idx, 'Educational Background'))
        elif re.match(r'^Career$', line_stripped, re.IGNORECASE):
            section_indices.append((idx, 'Career'))
        elif re.match(r'^Personal\s+[Ii]nformation$', line_stripped, re.IGNORECASE):
            section_indices.append((idx, 'Personal information'))
    
    if section_indices:
        # Extract content between section headings
        section_indices.sort()
        for i, (line_idx, section_name) in enumerate(section_indices):
            start = line_idx + 1
            # End is the start of the next section or end of document
            if i + 1 < len(section_indices):
                end = section_indices[i + 1][0]
            else:
                end = len(lines)
            
            section_lines = lines[start:end]
            section_text = '\n'.join(section_lines).strip()
            result[section_name] = section_text
    else:
        # No clear sections found, return full text
        result['Educational Background'] = body_text
    
    return result


def main():
    os.makedirs(BIO_DIR, exist_ok=True)

    headers, rows = read_materials()

    # 1) Extract candidate names from bio_name column (format: bio/Adam_Frisch.txt)
    candidate_names = []
    for r in rows:
        bio_name = r.get('bio_name', '') or ''
        # Extract candidate name from bio/*.txt format
        if bio_name.startswith('bio/') and bio_name.lower().endswith('.txt'):
            # Extract name from bio/Candidate_Name.txt -> Candidate_Name
            name = os.path.splitext(os.path.basename(bio_name))[0]
            candidate_names.append(name)
    
    print(f"Extracted {len(candidate_names)} candidate names from {MATERIALS}")

    # 2) Parse docx by searching for candidate names
    unique_candidates = sorted(set(candidate_names))
    # Remove the special cases
    unique_candidates = [c for c in unique_candidates if c not in ['*', 'fill_img']]
    
    mapping = parse_docx_by_candidate_names(DOCX, unique_candidates)
    print(f"Found {len(mapping)} candidates in {DOCX}")

    # 3) For each candidate, find match and extract sections
    saved = 0
    unmatched = []
    for candidate in unique_candidates:
        norm_candidate = normalize_name(candidate)
        
        # Look up in mapping
        if norm_candidate not in mapping:
            unmatched.append(candidate)
            continue

        orig_name, body = mapping[norm_candidate]
        sections = extract_sections_from_body(body)
        
        # Create file contents with clear headings
        parts = []
        eb = sections.get('Educational Background', '').strip()
        car = sections.get('Career', '').strip()
        pi = sections.get('Personal information', '').strip()

        if eb:
            parts.append('Educational Background\n' + eb)
        if car:
            parts.append('Career\n' + car)
        if pi:
            parts.append('Personal Information\n' + pi)
        if not parts:
            # fallback to full body
            parts = [body.strip()]

        out_text = '\n\n'.join(parts).strip()
        out_path = os.path.join(BIO_DIR, f"{candidate}.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(out_text)
        saved += 1
        print(f"Saved bio for {candidate} -> {out_path}")

    print(f"\nSaved {saved} bios. {len(unmatched)} unmatched candidates.")
    if unmatched:
        print("Unmatched candidates (no entry found in docx):")
        for u in unmatched[:50]:
            print(" - ", u)
        if len(unmatched) > 50:
            print(f"... and {len(unmatched) - 50} more")

if __name__ == '__main__':
    main()
