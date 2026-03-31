import os
import subprocess
from bs4 import BeautifulSoup
import re

html_file = 'Namma_Cloud_Book.html'

with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

main_content = soup.find('main', id='main')
sections = main_content.find_all('section')

def convert_html_to_qmd(html_content, output_filename):
    tmp_html = f"tmp_{output_filename}.html"
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Run quarto pandoc to convert html to markdown
    cmd = ["quarto", "pandoc", tmp_html, "-o", output_filename, "--wrap=none", "--from=html", "--to=markdown"]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Converted {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {output_filename}: {e.stderr}")
    finally:
        if os.path.exists(tmp_html):
            os.remove(tmp_html)

chapters = []

for section in sections:
    sec_id = section.get('id', '')
    
    # Identify heading for chapter metadata
    if sec_id == 'cover':
        filename = 'index.qmd'
        title = "Foreword"
    else:
        filename = f"{sec_id}.qmd"
        heading = section.find('h1', class_='chapter-title')
        title = heading.text.strip() if heading else sec_id
        
    # Optional: we can pre-process callouts in the HTML to Quarto native callouts,
    # or just let Pandoc handle divs and fix them later.
    for callout in section.find_all('div', class_=re.compile(r'callout callout-.*')):
        # Quarto syntax: 
        # ::: {.callout-note}
        # ## Title
        # Content
        # :::
        classes = callout.get('class', [])
        c_type = 'note'
        for c in classes:
            if c.startswith('callout-') and c != 'callout-title':
                c_type = c.replace('callout-', '')
        
        # Replace div with specifically formatted text that pandoc converts to plain text, 
        # or we can rewrite the HTML to standard simple structure.
        # It's easier to just let pandoc do its thing with divs, and we just fix it after.
        pass

    # Convert the section to string
    html_str = str(section)
    convert_html_to_qmd(html_str, filename)
    chapters.append((filename, title))

print(f"Extracted {len(chapters)} chapters.")
