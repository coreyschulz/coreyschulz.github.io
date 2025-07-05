# Blog Generation Guide

## Overview
This system converts markdown files to HTML blog posts using a template system.

## Usage

1. Create a markdown file with frontmatter:
```markdown
---
title: Your Blog Post Title
date: 2025-07-05
---

Your content here...
```

2. Run the generator:
```bash
python3 generate_blog.py your-post.md
```

3. The HTML file will be created in the `/blog` directory

## Features

- Automatic reading time calculation
- Responsive design for desktop and mobile
- Social sharing buttons
- Syntax highlighting for code blocks
- Clean, modern typography
- Navigation between posts (placeholder for future enhancement)

## Markdown Support

- Headers (h1-h6)
- Bold and italic text
- Links
- Code blocks and inline code
- Blockquotes
- Ordered and unordered lists
- Horizontal rules
- Tables (basic support)

## Customization

- Template: `/blog/template.html`
- Styles: `/css/blog.css`
- Theme: Inherits from site theme (default: indigo-white)