import docx
import os
import base64 
import re
import json

def b64_to_docx(text):
    save_path = os.path.join(os.getcwd(), "app", "data", "lichTuan", "lichTuan.doc")
    docx_data = base64.b64decode(text)
    with open(save_path, "wb") as file:
        file.write(docx_data)


def read_docx():
    file_path = os.path.join(os.getcwd(), "app", "data", "lichTuan", "lichTuan.doc")
    print(file_path)
    doc = docx.Document(file_path)
    full_text = []

    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell_text = cell.text.strip()
                if cell_text:
                    full_text.append(cell_text)

    return '\n'.join(full_text)

def parse_schedule(text):
    date_pattern = r'(Thứ\s+\w+,?\s*ngày\s+\d{1,2}/\d{1,2})'
    time_event_pattern = r'(\d{2}[:.]\d{2}): (.+)'
    location_pattern = r'DD: (.+)'
    attendees_pattern = r'TP: (.+)'
    preparation_pattern = r'C/b: (.+)'

    schedule = []
    current_date = ""
    current_event = None
    unique_events = set()

    lines = text.split("\n")

    for line in lines:
        date_match = re.search(date_pattern, line)
        if date_match:
            current_date = date_match.group(1).replace("  ", " ")  
            continue

        time_event_match = re.search(time_event_pattern, line)
        if time_event_match:
            if current_event:
                event_tuple = tuple(sorted(current_event.items()))
                if event_tuple not in unique_events:
                    schedule.append(current_event)
                    unique_events.add(event_tuple)
            
            current_event = {
                'date': current_date,
                'time': time_event_match.group(1),
                'event': time_event_match.group(2).strip(),
                'location': '',
                'attendees': '',
                'preparation': ''
            }
        elif current_event:
            location_match = re.search(location_pattern, line)
            if location_match:
                current_event['location'] = location_match.group(1).strip()
            
            attendees_match = re.search(attendees_pattern, line)
            if attendees_match:
                current_event['attendees'] = attendees_match.group(1).strip()
            
            preparation_match = re.search(preparation_pattern, line)
            if preparation_match:
                current_event['preparation'] = preparation_match.group(1).strip()

    if current_event:
        event_tuple = tuple(sorted(current_event.items()))
        if event_tuple not in unique_events:
            schedule.append(current_event)

    return schedule

def save_to_json(schedule):
    output_file = os.path.join(os.getcwd(), "app", "data", "lichTuan", "lichTuan.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=4)

print(read_docx())