# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a static personal website hosted on GitHub Pages at coreyschulz.com. It's a lightweight site built with pure HTML and CSS - no JavaScript frameworks, build tools, or server-side processing required.

## Development Commands

Since this is a static site with no build process:
- **Run locally**: Use any static file server (e.g., `python -m http.server 8000` or `npx serve`)
- **Deploy**: Push to GitHub and changes automatically deploy via GitHub Pages
- **Test**: Open HTML files directly in a browser or use a local server

## Architecture

### Key Structure
- Pure static HTML/CSS website
- No JavaScript dependencies or frameworks
- Modular CSS organization with reset styles, main styles, and theme system
- Responsive design with mobile-first approach

### CSS Architecture
```
css/
├── reset.css          # Browser normalization
├── styles.css         # Core styles and layout
└── themes/            # Color theme overrides
    ├── indigo-white.css
    └── red-white.css
```

### Theme System
The site uses a theme-based approach where:
1. `styles.css` defines all layout and structure
2. Theme files override CSS color variables
3. Pages link to both styles.css and a theme file

### Content Organization
- Root level: Main pages (index.html, consulting.html, privacy policies)
- `/blog/`: Blog posts
- `/best/`: Annual media recommendation lists
- `/images/`: Organized by year/purpose

## Important Patterns

### Adding New Pages
1. Create HTML file at appropriate location
2. Include reset.css, styles.css, and a theme file
3. Use existing pages as templates for consistent structure

### CSS Modifications
- Responsive breakpoints: 576px, 768px, 992px, 1200px
- Font sizes scale from 14px (mobile) to 20px (desktop)
- Use flexbox for centering, grid for card layouts

### Deployment
The site auto-deploys on push to master branch. The CNAME file configures the custom domain (coreyschulz.com).

## Current State
The site is in transition with several "Under Construction" pages. Recent commits show removal of a Jeopardy game application that was moved to a separate domain.