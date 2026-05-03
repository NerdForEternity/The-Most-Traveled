#!/usr/bin/env python3

import os
import re
from pathlib import Path

def fix_replacement_chars(text):
    """
    Replace Unicode replacement character (�) with appropriate punctuation.
    """
    result = []
    quote_stack = []  # Track open quotes
    
    for i, char in enumerate(text):
        if char == '�':
            # Look at surrounding context
            prev_char = text[i-1] if i > 0 else ' '
            next_char = text[i+1] if i < len(text) - 1 else ' '
            
            # Check if it's likely an apostrophe/single quote
            if prev_char.isalnum() and next_char.isalnum():
                # Middle of word: apostrophe (e.g., "don't", "it's")
                result.append("'")
            elif prev_char.isalnum() and not next_char.isalnum():
                # End of word: could be closing quote or apostrophe
                if quote_stack and quote_stack[-1] == 'single':
                    result.append("'")
                    quote_stack.pop()
                else:
                    result.append("'")
            elif not prev_char.isalnum() and next_char.isalnum():
                # Start of word: opening quote
                quote_stack.append('single')
                result.append("'")
            else:
                # Default to apostrophe
                result.append("'")
        else:
            result.append(char)
    
    text = ''.join(result)
    
    # Replace opening quotes (after spaces, newlines, or punctuation like :, (, [, etc.)
    text = re.sub(r'([\s:\(\[\{])[\']([\w])', r'\1"\2', text)
    
    # Replace closing quotes before punctuation or spaces
    text = re.sub(r'([\w])[\']([\s\.\,\!\?\)\]\}])', r'\1"\2', text)
    
    # Replace remaining single quotes with curly apostrophes in contractions
    text = re.sub(r"(\w)'(\w)", r"\1'\2", text)
    
    return text

def process_html_files(directory):
    """
    Process all HTML files in the directory and subdirectories.
    """
    html_dir = Path(directory)
    html_files = list(html_dir.glob('**/*.html'))
    
    if not html_files:
        print("No HTML files found.")
        return
    
    print(f"Found {len(html_files)} HTML file(s)")
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '�' in content:
                fixed_content = fix_replacement_chars(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                # Count replacements
                count = content.count('�')
                print(f"✓ Fixed {file_path.name} ({count} replacements)")
            else:
                print(f"  No replacements needed in {file_path.name}")
        
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")

if __name__ == '__main__':
    repo_dir = '/media/nerdforeternity/SSD/GithubRepos/The-Most-Traveled'
    process_html_files(repo_dir)
    print("\nDone!")
