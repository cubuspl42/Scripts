#!/usr/bin/env python3
import pyperclip
import re

def to_technical_string(text):
    # Convert the text to lower case
    text = text.lower()

    # Replace all non-safe characters with '-'
    text = re.sub(r'[^a-z0-9]', '-', text)

    # Replace multiple consecutive '-' with a single '-'
    text = re.sub(r'-+', '-', text)

    # Remove leading and trailing '-'
    text = text.strip('-')

    return text
    

print(to_technical_string(pyperclip.paste()), end='')
