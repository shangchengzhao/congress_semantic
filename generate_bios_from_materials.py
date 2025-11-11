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


def parse_docx_into_numbered_entries(docx_path=DOCX):
    doc = Document(docx_path)
    entries = []  # list of (name_text, body_text)

    number_pattern = re.compile(r"^\s*(\d+)\.\s*(.+)$")

    current_name = None
    current_body_lines = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            # keep blank lines as paragraph separators in body
            if current_name and current_body_lines:
                current_body_lines.append("")
            continue

        m = number_pattern.match(text)
        if m:
            # New entry
            # Save previous
            if current_name is not None:
                body = "\n".join(current_body_lines).strip()
                entries.append((current_name, body))
            # set new
            name_text = m.group(2).strip()
            current_name = name_text
            current_body_lines = []
        else:
            # append to current body
            if current_name is not None:
                current_body_lines.append(text)
            else:
                # If doc doesn't start with number, ignore leading text
                continue

    # save last
    if current_name is not None:
        body = "\n".join(current_body_lines).strip()
        entries.append((current_name, body))

    # build mapping from normalized name to (orig_name, body)
    mapping = {}
    for orig_name, body in entries:
        key = normalize_name(orig_name)
        mapping[key] = (orig_name, body)
    return mapping


def extract_sections_from_body(body_text: str) -> dict:
    # Try to find the three sections by headings. Return dict with keys Educational Background, Career, Personal information
    result = {"Educational Background":"", "Career":"", "Personal information":"", "full":""}
    result['full'] = body_text.strip()
    if not body_text:
        return result

    # Build a case-insensitive pattern for known headings
    headings_regex = re.compile(r"(^|\\n)(?P<h>\\s*(?:Educational Background|Education|Career|Professional Experience|Personal information|Personal Information|Personal Info)\\s*:\??)\\s*\\n", flags=re.I)

    # If headings exist, split by lines and locate indices
    # We'll also try a fallback by searching for heading tokens
    lines = body_text.splitlines()
    # flatten lines to single string for regex search
    text = "\n".join(lines)

    # find possible heading locations with their normalized heading label
    headings_positions = []  # list of (pos_index, label)

    for idx, line in enumerate(lines):
        l = line.strip()
        if not l:
            continue
        for canonical in ["Educational Background", "Career", "Personal information"]:
            # match ignoring case and optional trailing ':'
            if re.match(rf"^{canonical}\\s*:??$", l, flags=re.I):
                headings_positions.append((idx, canonical))

    if headings_positions:
        # sort by position
        headings_positions.sort()
        for i, (pos, label) in enumerate(headings_positions):
            start = pos+1
            end = headings_positions[i+1][0] if i+1 < len(headings_positions) else len(lines)
            section_text = "\n".join(lines[start:end]).strip()
            result[label] = section_text
        return result

    # Fallback: try to split by heading tokens inside the text
    # We'll search for tokens and split (Education, Career, Personal)
    token_pattern = re.compile(r"(Educational Background|Education|Career|Professional Experience|Personal information|Personal Information|Personal Info)\\s*[:\n]", flags=re.I)
    tokens = [(m.start(), m.group(1)) for m in token_pattern.finditer(text)]
    if tokens:
        tokens.sort()
        for i, (pos, token) in enumerate(tokens):
            start = pos + len(token)
            end = tokens[i+1][0] if i+1 < len(tokens) else len(text)
            chunk = text[start:end].strip("\n ")
            # map token to canonical
            if re.search(r"education", token, flags=re.I):
                result['Educational Background'] += ("\n" + chunk).strip()
            elif re.search(r"career|professional", token, flags=re.I):
                result['Career'] += ("\n" + chunk).strip()
            else:
                result['Personal information'] += ("\n" + chunk).strip()
        return result

    # Final fallback: try to heuristically split into three approx equal parts
    all_lines = [ln for ln in lines if ln.strip()]
    if not all_lines:
        return result
    n = len(all_lines)
    # split into up to three parts
    a = int(n/3)
    b = int(2*n/3)
    part1 = "\n".join(all_lines[:a]).strip()
    part2 = "\n".join(all_lines[a:b]).strip()
    part3 = "\n".join(all_lines[b:]).strip()
    result['Educational Background'] = part1
    result['Career'] = part2
    result['Personal information'] = part3
    return result


def main():
    os.makedirs(BIO_DIR, exist_ok=True)

    headers, rows = read_materials()

    # 1) Update materials.csv bio_name values
    updated_rows = []
    candidate_names = []
    for r in rows:
        bio_name = r.get('bio_name', '') or ''
        # If bio_name already is like bio/*.txt, keep
        if bio_name.startswith('bio/') and bio_name.lower().endswith('.txt'):
            # also extract candidate name
            name = os.path.splitext(os.path.basename(bio_name))[0]
            candidate_names.append(name)
            updated_rows.append(r)
            continue
        # If it looks like an image path, extract candidate
        candidate = extract_candidate_name_from_path(bio_name)
        if candidate:
            new_bio = f"{BIO_DIR}/{candidate}.txt"
            r['bio_name'] = new_bio
            candidate_names.append(candidate)
        else:
            # keep as is
            r['bio_name'] = bio_name
        updated_rows.append(r)

    # write back updated CSV
    write_materials(headers, updated_rows)
    print(f"Updated {len(updated_rows)} rows in {MATERIALS}")

    # 2) Parse docx into numbered entries mapping
    mapping = parse_docx_into_numbered_entries()
    print(f"Parsed {len(mapping)} numbered entries from {DOCX}")

    # 3) For each candidate, find match and extract sections
    saved = 0
    unmatched = []
    for candidate in sorted(set(candidate_names)):
        norm_candidate = normalize_name(candidate)
        match = None
        # Direct match
        if norm_candidate in mapping:
            match = mapping[norm_candidate]
        else:
            # try fuzzy matches: iterate mapping keys and compare simplified tokens
            for key, (orig_name, body) in mapping.items():
                if norm_candidate == key:
                    match = (orig_name, body)
                    break
            if not match:
                # try contains: candidate name tokens in orig_name
                for key, (orig_name, body) in mapping.items():
                    if normalize_name(orig_name).find(norm_candidate) != -1 or norm_candidate.find(normalize_name(orig_name)) != -1:
                        match = (orig_name, body)
                        break
        if not match:
            unmatched.append(candidate)
            continue

        orig_name, body = match
        sections = extract_sections_from_body(body)
        # Create file contents with clear headings
        parts = []
        eb = sections.get('Educational Background') or sections.get('Education') or ''
        car = sections.get('Career') or sections.get('Professional Experience') or ''
        pi = sections.get('Personal information') or sections.get('Personal Information') or ''

        if eb:
            parts.append('Educational Background:\n' + eb.strip())
        if car:
            parts.append('Career:\n' + car.strip())
        if pi:
            parts.append('Personal information:\n' + pi.strip())
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
        for u in unmatched[:200]:
            print(" - ", u)

if __name__ == '__main__':
    main()
