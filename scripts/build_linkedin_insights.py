#!/usr/bin/env python3
"""Rebuild Visualriot insights from the Dropbox LinkedIn package folder."""
from pathlib import Path
import html
import re

SOURCE_DIR = Path('/Users/visualriot/Dropbox/hermes/from Onquest/content/linkedin')
OUTPUT_FILE = Path(__file__).resolve().parents[1] / 'insights.html'

STRONG_RE = re.compile(r'\*\*(.+?)\*\*')


def md_inline(text: str) -> str:
    return STRONG_RE.sub(r'<strong>\1</strong>', html.escape(text))


def md_to_html(md: str) -> str:
    out = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith('**') and line.endswith('**') and line.count('**') == 2:
            out.append(f'<p class="article-kicker">{md_inline(line[2:-2])}</p>')
            i += 1
            continue
        if line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append(md_inline(lines[i][2:].strip()))
                i += 1
            out.append('<ul class="clean article-list">' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>')
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('- '):
            if lines[i].startswith('**') and lines[i].endswith('**') and lines[i].count('**') == 2:
                break
            para.append(lines[i].rstrip())
            i += 1
        out.append(f'<p>{md_inline(" ".join(x.strip() for x in para).strip())}</p>')
    return '\n'.join(out)


def parse_packages():
    articles = []
    for fp in sorted(SOURCE_DIR.glob('*/*-complete.md')):
        text = fp.read_text(encoding='utf-8')
        lines = text.splitlines()
        if not lines:
            continue
        title = lines[0].lstrip('# ').replace('LinkedIn Package: ', '').strip()
        date = ''
        voice = ''
        for line in lines[:10]:
            if line.startswith('**Date:**'):
                date = line.split('**Date:**', 1)[1].strip()
            elif line.startswith('**Voice:**'):
                voice = line.split('**Voice:**', 1)[1].strip()
        start = end = None
        for idx, line in enumerate(lines):
            if line.strip() == '## 1) Long-form article':
                start = idx + 1
            elif start is not None and line.startswith('## 2)'):
                end = idx
                break
        if start is None:
            continue
        body = '\n'.join(lines[start:end]).strip('\n')
        body_lines = body.splitlines()
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        articles.append({
            'title': title,
            'date': date,
            'voice': voice,
            'source': fp.name,
            'body': '\n'.join(body_lines),
        })
    articles.sort(key=lambda a: a['date'], reverse=True)
    return articles


def build_page(articles):
    latest = articles[:6]
    article_sections = []
    for a in latest:
        article_sections.append(
            '<article class="card article">'
            '<div class="article-meta">'
            '<div><div class="eyebrow">LinkedIn mirror</div>'
            f'<h2>{html.escape(a["title"])}</h2></div>'
            '<div class="article-meta-right">'
            f'<div class="muted">Date: {html.escape(a["date"])} </div>'
            f'<div class="muted">Voice: {html.escape(a["voice"])} </div>'
            '</div></div>'
            f'<div class="article-body">{md_to_html(a["body"])}</div>'
            f'<div class="article-source muted">Source package: {html.escape(a["source"])}</div>'
            '</article>'
        )
    archive_items = ''.join(
        f'<li><strong>{html.escape(a["title"])}</strong> <span class="muted">({html.escape(a["date"])}{", " + html.escape(a["voice"]) if a["voice"] else ""})</span></li>'
        for a in articles
    )
    page = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '  <title>LinkedIn Articles | Visualriot®</title>\n'
        '  <meta name="description" content="Full Visualriot articles mirrored from public LinkedIn posts and kept current on the website.">\n'
        '  <link rel="stylesheet" href="styles.css">\n'
        '</head>\n<body>\n'
        '  <a class="skip" href="#content">Skip to content</a>\n'
        '  <header>\n    <div class="wrap topbar">\n'
        '      <a class="brand" href="index.html" aria-label="Visualriot home">\n        <span class="brand-lockup" aria-hidden="true">VR</span>\n        <span class="brand-copy"><strong>Visualriot®</strong><span>Modern communication, kept sharp</span></span>\n      </a>\n'
        '      <nav aria-label="Main navigation">\n        <ul>\n'
        '          <li><a href="index.html">Home</a></li>\n'
        '          <li><a href="about.html">About</a></li>\n'
        '          <li><a href="how-we-help.html">How We Help</a></li>\n'
        '          <li><a href="selected-experience.html">Experience</a></li>\n'
        '          <li><a aria-current="page" href="insights.html">LinkedIn Articles</a></li>\n'
        '          <li><a class="cta primary" href="book-a-call.html">Book a Call</a></li>\n'
        '        </ul>\n      </nav>\n    </div>\n  </header>\n'
        '  <main id="content">\n'
        '    <section class="hero">\n'
        '      <div class="wrap hero-grid insights-hero">\n'
        '        <div>\n'
        '          <div class="eyebrow">Insights</div>\n'
        '          <h1>Full articles mirrored from LinkedIn and kept current on the site.</h1>\n'
        '          <p class="lede">The site now publishes the full long-form articles here so the website stays aligned with the public LinkedIn profile.</p>\n'
        '          <p class="muted">Source profile: <a href="https://www.linkedin.com/in/inmanc" target="_blank" rel="noreferrer">linkedin.com/in/inmanc</a>. The build script reads the current article packages from Dropbox and regenerates this page.</p>\n'
        '        </div>\n'
        '        <aside class="hero-card">\n'
        '          <span class="pill">Latest mirror status</span>\n'
        '          <div class="stats single">\n'
        f'            <div class="stat"><strong>{len(latest)}</strong><span>full articles rendered here</span></div>\n'
        f'            <div class="stat"><strong>{len(articles)}</strong><span>article packages available</span></div>\n'
        '            <div class="stat"><strong>Dropbox</strong><span>source package folder</span></div>\n'
        '            <div class="stat"><strong>Auto-ready</strong><span>rerun the build script when a new package lands</span></div>\n'
        '          </div>\n'
        '        </aside>\n'
        '      </div>\n'
        '    </section>\n'
        '    <section class="section">\n'
        '      <div class="wrap card callout">\n'
        '        <h2>How this stays up to date</h2>\n'
        '        <p>The generator scans <code>Dropbox/hermes/from Onquest/content/linkedin</code>, sorts the article packages by date, and rebuilds this page from the latest content.</p>\n'
        '        <p class="muted">That keeps the website in sync with the public LinkedIn article workflow without hand-editing the page every time.</p>\n'
        '      </div>\n'
        '    </section>\n'
        '    <section class="section">\n'
        '      <div class="wrap stack">\n'
        + ''.join(article_sections) +
        '\n      </div>\n'
        '    </section>\n'
        '    <section class="section">\n'
        '      <div class="wrap card">\n'
        '        <div class="head"><div><div class="eyebrow">Archive</div><h2>All mirrored article packages</h2></div></div>\n'
        '        <ul class="clean archive-list">\n'
        f'          {archive_items}\n'
        '        </ul>\n'
        '      </div>\n'
        '    </section>\n'
        '  </main>\n'
        '  <footer class="footer">\n'
        '    <div class="wrap footgrid">\n'
        '      <div><strong>Visualriot</strong><div class="muted">Human-led communication strategy with practical AI support.</div></div>\n'
        '      <div><div><a href="https://www.linkedin.com/in/inmanc" target="_blank" rel="noreferrer">LinkedIn profile</a></div><div class="muted">No email links on the site.</div></div>\n'
        '    </div>\n'
        '  </footer>\n'
        '</body>\n</html>\n'
    )
    OUTPUT_FILE.write_text(page, encoding='utf-8')
    print(f'Wrote {OUTPUT_FILE}')


if __name__ == '__main__':
    build_page(parse_packages())
