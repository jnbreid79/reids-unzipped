# Reid's Unzipped — Jekyll / GitHub Pages

## Quick setup

1. **Create a GitHub repo** called `reids-unzipped` (or whatever you prefer).

2. **Drop these files** into the repo root.

3. **Enable GitHub Pages** in repo Settings → Pages → Source: `main` branch, `/ (root)`.

4. **Update `_config.yml`** — change `url` and `repository` to match your GitHub username and repo name.

5. **Add your images** to `assets/images/`:
   - `hero-banner.jpg` — wide landscape sailing shot for the homepage hero (ideally 1800px+ wide)
   - `zipper-logo-light.png` — the light (white/ice blue) version of the logo
   - `crew/angus.jpg`, `crew/sophie.jpg`, `crew/isla.jpg`, `crew/jamie.jpg` — portrait crops work best
   - `crew-photo.jpg` — group shot for the sidebar bio

6. Your site will be live at `https://yourusername.github.io/reids-unzipped` within a few minutes of pushing.

## Colour palette reference

| Name | Hex | Used for |
|------|-----|----------|
| Navy | `#1a3a5c` | Masthead, footer, headings |
| Mid blue | `#2d6a9f` | Links, buttons |
| Ice blue | `#b8d4e8` | Logo accent, highlights, borders |
| Off-white | `#f8fbfd` | Page background |
| Muted | `#5a7a96` | Meta text, captions |

## Adding a new blog post

Create a file in `_posts/` named `YYYY-MM-DD-post-title.md`:

```markdown
---
title: "Your Post Title"
date: 2025-11-28
categories: [Pacific, New Zealand]
tags: [whangarei, passage, wildlife]
header:
  image: /assets/images/posts/your-hero-image.jpg
  teaser: /assets/images/posts/your-hero-image.jpg
excerpt: "A one or two sentence summary shown on the homepage."
---

Your post content here in Markdown...
```

Images for posts go in `assets/images/posts/`.

## Custom skin

The colour theme lives in `_sass/minimal-mistakes/skins/_zipper.scss` and additional
layout/component styles are in `assets/css/main.scss`. Everything is commented.
