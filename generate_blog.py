#!/usr/bin/env python3
"""
Blog post generator for static site
Converts markdown files to HTML using a template
"""

import os
import re
import sys
from datetime import datetime
from urllib.parse import quote
import argparse

def parse_frontmatter(content):
    """Parse YAML-style frontmatter from markdown content"""
    frontmatter = {}
    body = content
    
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            body = parts[2]
            
            for line in frontmatter_text.strip().split('\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
    
    return frontmatter, body

def markdown_to_html(markdown_text):
    """Convert markdown to HTML - basic implementation"""
    html = markdown_text
    
    # Convert headers
    for i in range(6, 0, -1):
        pattern = r'^' + '#' * i + r' (.+)$'
        html = re.sub(pattern, rf'<h{i}>\1</h{i}>', html, flags=re.MULTILINE)
    
    # Convert bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
    
    # Convert italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
    
    # Convert links
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Convert inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Convert code blocks
    def convert_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2)
        return f'<pre><code class="language-{lang}">{code}</code></pre>'
    
    html = re.sub(r'```(\w*)\n(.*?)```', convert_code_block, html, flags=re.DOTALL)
    
    # Convert blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Convert unordered lists
    def convert_ul(text):
        lines = text.split('\n')
        result = []
        in_list = False
        
        for line in lines:
            if re.match(r'^[-*+] ', line):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                result.append(f'<li>{line[2:]}</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('</ul>')
        
        return '\n'.join(result)
    
    html = convert_ul(html)
    
    # Convert ordered lists
    def convert_ol(text):
        lines = text.split('\n')
        result = []
        in_list = False
        
        for line in lines:
            if re.match(r'^\d+\. ', line):
                if not in_list:
                    result.append('<ol>')
                    in_list = True
                content = re.sub(r'^\d+\. ', '', line)
                result.append(f'<li>{content}</li>')
            else:
                if in_list:
                    result.append('</ol>')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('</ol>')
        
        return '\n'.join(result)
    
    html = convert_ol(html)
    
    # Convert horizontal rules
    html = re.sub(r'^---+$', '<hr>', html, flags=re.MULTILINE)
    
    # Convert paragraphs
    paragraphs = []
    current_para = []
    
    for line in html.split('\n'):
        line = line.strip()
        if line:
            if line.startswith('<'):
                if current_para:
                    paragraphs.append('<p>' + ' '.join(current_para) + '</p>')
                    current_para = []
                paragraphs.append(line)
            else:
                current_para.append(line)
        elif current_para:
            paragraphs.append('<p>' + ' '.join(current_para) + '</p>')
            current_para = []
    
    if current_para:
        paragraphs.append('<p>' + ' '.join(current_para) + '</p>')
    
    return '\n'.join(paragraphs)

def calculate_reading_time(text):
    """Calculate estimated reading time in minutes"""
    words = len(re.findall(r'\w+', text))
    return max(1, round(words / 200))

def generate_blog_post(markdown_file, output_dir='blog'):
    """Generate HTML blog post from markdown file"""
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)
    
    # Get metadata
    title = frontmatter.get('title', 'Untitled')
    date_str = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Parse date
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        date_iso = date.isoformat()
        date_formatted = date.strftime('%B %d, %Y')
    except:
        date_iso = datetime.now().isoformat()
        date_formatted = datetime.now().strftime('%B %d, %Y')
    
    # Convert markdown to HTML
    html_content = markdown_to_html(body.strip())
    
    # Calculate reading time
    reading_time = calculate_reading_time(body)
    
    # Generate filename
    filename = os.path.basename(markdown_file).replace('.md', '.html')
    output_path = os.path.join(output_dir, filename)
    
    # Prepare template variables
    url = f"https://coreyschulz.com/blog/{filename}"
    replacements = {
        '{{title}}': title,
        '{{date_iso}}': date_iso,
        '{{date_formatted}}': date_formatted,
        '{{reading_time}}': str(reading_time),
        '{{content}}': html_content,
        '{{title_encoded}}': quote(title),
        '{{url_encoded}}': quote(url),
        '{{#if prev_post}}': '<!--',
        '{{/if}}': '-->',
        '{{#if next_post}}': '<!--',
        '{{prev_post.filename}}': '',
        '{{prev_post.title}}': '',
        '{{next_post.filename}}': '',
        '{{next_post.title}}': ''
    }
    
    # Read template
    with open('blog/template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace template variables
    for key, value in replacements.items():
        template = template.replace(key, value)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"Generated: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Generate blog posts from markdown files')
    parser.add_argument('markdown_file', help='Path to the markdown file')
    parser.add_argument('-o', '--output-dir', default='blog', help='Output directory (default: blog)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.markdown_file):
        print(f"Error: File not found: {args.markdown_file}")
        sys.exit(1)
    
    generate_blog_post(args.markdown_file, args.output_dir)

if __name__ == '__main__':
    main()