import re
import os
import docx 
import json

file_path = os.path.join(os.getcwd(), "app", "data", "lichTuan", "lichTuan.docx")
extract_events_from_doc(file_path)