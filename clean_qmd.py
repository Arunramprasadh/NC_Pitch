import os
import re
import glob

# Find all .qmd files in the current directory
qmd_files = glob.glob("*.qmd")

def clean_markdown(content):
    # 1. Remove Pandoc div lines (e.g., ::: {#id .class} or :::)
    # Matches lines starting with 3 or more colons, optional spaces and attributes, till end of line
    content = re.sub(r'^:{3,}.*$\n?', '', content, flags=re.MULTILINE)
    
    # 2. Remove Pandoc span attributes but keep text: [Text]{.class} -> Text
    # We loop to handle nested cases if any, but a simple sub usually suffices.
    content = re.sub(r'\[([^\]]+)\]\{[^}]+\}', r'\1', content)
    
    # 3. Remove Pandoc heading attributes: # Heading {#id .class} -> # Heading
    content = re.sub(r'^(#+.*?)\s+\{[^}]+\}$', r'\1', content, flags=re.MULTILINE)
    
    return content

for file_path in qmd_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned_content = clean_markdown(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"Cleaned {file_path}")
