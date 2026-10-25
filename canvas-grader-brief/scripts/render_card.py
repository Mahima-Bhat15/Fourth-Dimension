#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow==12.0.0"]
# ///
"""Render verified aggregate assignment data as PNG cards. No network or credentials."""
import argparse
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

NAVY = '#18344D'
MUTED = '#68747F'
BG = '#F8F4EC'
TRACK = '#EAEFF2'
GREEN = '#167368'


def number(value, label, integer=False):
    if value is None:
        return
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value < 0 or (integer and not float(value).is_integer())):
        raise ValueError(f'{label} must be a nonnegative number' + (' of whole items.' if integer else '.'))


def date_label(value, zone):
    date = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if date.tzinfo is None:
        raise ValueError('Dates must include a UTC offset or Z.')
    local = date.astimezone(zone)
    return local.strftime('%b %d, %Y · %I:%M %p %Z').replace(' 0', ' ')


def validate(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be an object.')
    for key in ('time_zone',):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'{key} is required.')
    zone = ZoneInfo(data['time_zone'])
    if data.get('checked_at'):
        date_label(data['checked_at'], zone)
    rows = data.get('assignments')
    if not isinstance(rows, list) or len(rows) > 30:
        raise ValueError('assignments must be a list of up to 30 items; split larger reports.')
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('name'), str) or not row['name'].strip():
            raise ValueError('Each assignment needs a name string.')
        if row.get('course') is not None and not isinstance(row['course'], str):
            raise ValueError('course must be a string when supplied.')
        for key in ('points_possible', 'assignment_group_weight_pct'):
            number(row.get(key), key)
        for key in ('students_submitted', 'eligible_students', 'needs_grading'):
            number(row.get(key), key, integer=True)
        submitted, total = row.get('students_submitted'), row.get('eligible_students')
        if submitted is not None and total is not None and submitted > total:
            raise ValueError('Students submitted cannot exceed the matching eligible total.')
        if row.get('assignment_group_weight_pct') is not None and row['assignment_group_weight_pct'] > 100:
            raise ValueError('Assignment-group weight cannot exceed 100%.')
        for key in ('due_at', 'grading_due_at'):
            if row.get(key):
                date_label(row[key], zone)
        if row.get('due_status', 'unavailable') not in ('unavailable', 'no_due_date', 'multiple'):
            raise ValueError('due_status must be unavailable, no_due_date, or multiple.')
    return zone


def font(size, bold=False):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans' + ('-Bold' if bold else '') + '.ttf',
        '/System/Library/Fonts/Supplemental/Arial' + (' Bold' if bold else '') + '.ttf',
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def short(draw, value, width, face):
    value = ' '.join(str(value).split())
    if draw.textlength(value, font=face) <= width:
        return value
    while value and draw.textlength(value + '...', font=face) > width:
        value = value[:-1]
    return value + '...'


def assignment_fields(row, zone):
    """Only display actual values; missing fields do not reserve space."""
    fields = []
    if row.get('course'):
        fields.append(('text', row['course'].upper(), 23, MUTED, True))
    fields.append(('text', row['name'], 41, NAVY, True))
    if row.get('due_status') == 'multiple':
        fields.append(('text', 'Student deadlines: Multiple dates', 27, NAVY, True))
    elif row.get('due_at'):
        fields.append(('text', 'Due: ' + date_label(row['due_at'], zone), 27, NAVY, True))
    marks = []
    if row.get('points_possible') is not None:
        marks.append(f"{row['points_possible']:g} points possible")
    if row.get('assignment_group_weight_pct') is not None:
        marks.append(f"Assignment-group weight {row['assignment_group_weight_pct']:g}%")
    if marks:
        fields.append(('text', ' · '.join(marks), 23, MUTED, False))
    submitted, total = row.get('students_submitted'), row.get('eligible_students')
    if submitted is not None:
        label = f'Students submitted: {submitted:g}'
        if total is not None and total > 0:
            label += f' / {total:g}'
        fields.append(('text', label, 25, NAVY, True))
        if total is not None and total > 0:
            fields.append(('bar', submitted / total))
    elif total is not None:
        fields.append(('text', f'Eligible students: {total:g}', 25, NAVY, False))
    if row.get('needs_grading') is not None:
        fields.append(('text', f"Needs grading: {row['needs_grading']:g}", 25, '#A56908', True))
    if row.get('grading_due_at'):
        fields.append(('text', 'Grading due: ' + date_label(row['grading_due_at'], zone), 24, MUTED, False))
    return fields


def render(data, output):
    zone = validate(data)
    rows = data['assignments']
    pages = [rows[i:i + 3] for i in range(0, len(rows), 3)]
    paths = []
    for page_index, page in enumerate(pages):
        cards = [assignment_fields(row, zone) for row in page]
        heights = [64 + sum(38 if f[0] == 'bar' else f[2] + 18 for f in fields) for fields in cards]
        image = Image.new('RGB', (960, 64 + sum(heights) + 24 * (len(page) - 1)), BG)
        draw = ImageDraw.Draw(image)
        y = 32
        for fields, height in zip(cards, heights):
            draw.rounded_rectangle((32, y + 4, 928, y + height + 4), radius=28, fill='#EAE4D9')
            draw.rounded_rectangle((32, y, 928, y + height), radius=28, fill='white')
            cursor = y + 28
            for field in fields:
                if field[0] == 'bar':
                    ratio = field[1]
                    draw.rounded_rectangle((64, cursor + 4, 896, cursor + 18), radius=7, fill=TRACK)
                    if ratio > 0:
                        draw.rounded_rectangle((64, cursor + 4, 64 + max(14, 832 * ratio), cursor + 18), radius=7, fill=GREEN)
                    cursor += 38
                else:
                    _, value, size, color, bold = field
                    face = font(size, bold)
                    draw.text((64, cursor), short(draw, value, 832, face), font=face, fill=color)
                    cursor += size + 18
            y += height + 24
        destination = output if page_index == 0 else output.with_name(output.stem + f'-{page_index + 1}' + output.suffix)
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, 'PNG', optimize=True)
        paths.append(str(destination.resolve()))
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--input', type=Path)
    group.add_argument('--sample', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'assets/sample-card.json' if args.sample else args.input
    target = args.output or Path.home() / '.config/canvas-grader-brief/cards' / ('sample.png' if args.sample else 'brief.png')
    if target.suffix.lower() != '.png':
        parser.error('--output must end in .png')
    try:
        data = json.loads(source.read_text())
        if args.sample:
            for row in data.get('assignments', []):
                if 'demo' not in row.get('course', '').lower():
                    row['course'] = (row.get('course', '') + ' · DEMO').strip()
        print(json.dumps({'images': render(data, target), 'sample': args.sample}))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'Could not render card: {exc}\n')


if __name__ == '__main__':
    main()
