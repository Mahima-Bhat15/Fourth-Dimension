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
ORANGE = '#ED9C16'
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
    for key in ('source', 'checked_at', 'time_zone'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'{key} is required.')
    zone = ZoneInfo(data['time_zone'])
    date_label(data['checked_at'], zone)
    rows = data.get('assignments')
    if not isinstance(rows, list) or len(rows) > 30:
        raise ValueError('assignments must be a list of up to 30 items; split larger reports.')
    for row in rows:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), str) and row[k].strip() for k in ('course', 'name')):
            raise ValueError('Each assignment needs course and name strings.')
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


def render(data, output):
    zone = validate(data)
    rows = data['assignments']
    pages = [[row] for row in rows] or [[]]
    paths = []
    for page_index, page in enumerate(pages):
        height = 320 + max(1, len(page)) * 400 + 170
        image = Image.new('RGB', (960, height), BG)
        draw = ImageDraw.Draw(image)

        def text(x, y, value, size=26, color=NAVY, bold=False, width=800):
            face = font(size, bold)
            draw.text((x, y), short(draw, value, width, face), font=face, fill=color)

        text(56, 40, 'CANVAS / GRADER BRIEF', 22, MUTED, True)
        text(56, 90, 'Your grading,', 64, NAVY, True)
        text(56, 160, 'at a glance.', 64, NAVY, True)
        text(56, 248, data.get('range_label') or 'Selected assignments', 26, MUTED, width=680)
        if len(pages) > 1:
            text(790, 250, f'{page_index + 1} / {len(pages)}', 24, MUTED, width=130)
        if not page:
            text(60, 360, 'No assignments in the supplied result.', 32, bold=True)
            text(60, 420, 'Check the source and coverage before assuming nothing is due.', 24, MUTED)
        for index, row in enumerate(page):
            y = 310 + index * 400
            draw.rounded_rectangle((48, y + 5, 912, y + 383), radius=30, fill='#EAE4D9')
            draw.rounded_rectangle((48, y, 912, y + 378), radius=30, fill='white')
            text(78, y + 25, row['course'].upper(), 23, MUTED, True, width=530)
            draw.rounded_rectangle((718, y + 22, 878, y + 63), radius=20, fill='#FFF0D3')
            text(738, y + 29, 'ASSIGNMENT', 17, '#926012', True, width=125)
            text(78, y + 69, row['name'], 41, bold=True, width=790)
            if row.get('due_status') == 'multiple':
                due = 'Multiple deadlines - see assignment link'
            elif row.get('due_at'):
                due = date_label(row['due_at'], zone)
            elif row.get('due_status') == 'no_due_date':
                due = 'No due date'
            else:
                due = 'Unavailable'
            text(78, y + 128, 'STUDENT DEADLINE', 17, MUTED, True, width=250)
            text(78, y + 154, due, 28, bold=True)
            points = row.get('points_possible')
            points_text = f'{points:g} points possible' if points is not None else 'Points unavailable'
            weight = row.get('assignment_group_weight_pct')
            if weight is not None:
                points_text += f'  ·  Assignment-group weight {weight:g}%'
            text(78, y + 197, points_text, 23, MUTED)
            submitted, total = row.get('students_submitted'), row.get('eligible_students')
            if submitted is not None and total is not None and total > 0:
                text(78, y + 242, f'Students submitted   {submitted:g} / {total:g}', 24, bold=True)
                text(784, y + 242, f'{submitted / total:.0%}', 24, GREEN, True, width=90)
                draw.rounded_rectangle((78, y + 280, 878, y + 294), radius=7, fill=TRACK)
                if submitted > 0:
                    draw.rounded_rectangle((78, y + 280, 78 + max(14, 800 * submitted / total), y + 294), radius=7, fill=GREEN)
            else:
                label = f'Students submitted: {submitted:g}' if submitted is not None else 'Submission count unavailable'
                text(78, y + 251, label, 25, MUTED)
            pending = row.get('needs_grading')
            text(78, y + 321, f'Needs grading: {pending:g}' if pending is not None else 'Needs grading: unavailable', 24, '#A56908', True, width=390)
            grading_due = 'Not specified'
            if row.get('grading_due_at'):
                grading_due = date_label(row['grading_due_at'], zone)
            text(480, y + 324, 'Grading due: ' + grading_due, 19, MUTED, width=395)
        footer = height - 148
        draw.line((56, footer - 10, 904, footer - 10), fill='#E0D9CF', width=2)
        text(56, footer + 6, 'Source: ' + data['source'], 21, MUTED)
        text(56, footer + 39, 'Checked: ' + date_label(data['checked_at'], zone), 21, MUTED)
        text(56, footer + 75, data.get('coverage_note') or 'Only verified fields shown; unavailable is not zero.', 20, MUTED)
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
    group.add_argument('--demo', action='store_true', help='Render exactly two fictional demo assignments.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    fictional = args.sample or args.demo
    asset = 'demo-card.json' if args.demo else 'sample-card.json'
    source = Path(__file__).resolve().parents[1] / 'assets' / asset if fictional else args.input
    target = args.output or Path.home() / '.config/canvas-grader-brief/cards' / ('demo.png' if args.demo else 'sample.png' if args.sample else 'brief.png')
    if target.suffix.lower() != '.png':
        parser.error('--output must end in .png')
    try:
        data = json.loads(source.read_text())
        if fictional:
            data['source'] = 'FICTIONAL DEMO - not live Canvas'
        print(json.dumps({'images': render(data, target), 'sample': fictional}))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'Could not render card: {exc}\n')


if __name__ == '__main__':
    main()
