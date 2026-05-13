# Visualriot static site starter

This folder contains the plain HTML/CSS starter for the Visualriot site.

## Pages
- index.html
- about.html
- how-we-help.html
- selected-experience.html
- testimonials.html
- insights.html  (LinkedIn Articles)
- white-papers.html  (Coming Soon)
- book-a-call.html  (parked for later)
- styles.css

## Deployment idea
This is ready for Cloudflare Pages as a static site.

### Typical steps
1. Put this folder in a Git repo.
2. Push to GitHub.
3. Connect the repo to Cloudflare Pages.
4. Use the root folder as the publish directory.
5. Attach the Cloudflare-managed domain.

## Replace these placeholders
- `https://www.linkedin.com/in/inmanc`
- `https://cal.com/your-handle`

## Notes
- Use `scripts/build_linkedin_insights.py` to regenerate `insights.html` from the Dropbox article packages.
- No email links on the site.
- Insights mirrors the public LinkedIn article library on the website.
- Book a Call is parked for later.
- Visual style uses the orange and blue palette from the draft direction.
