# Portfolio redesign (mockup)

A mockup of Sidanta Parajuli's personal website, restructured after
[terryli710.github.io](https://terryli710.github.io/): a full-screen hero, then calm hairline
lists; a Projects index with search and tags; a page per project with a sticky Contents list;
a Design gallery; and a Profile page that is the whole résumé.

- **Home:** the sunrise photograph as the hero, then links, projects, experience and design. The site's colors are sampled from that photo. The particle-lily version is kept at `/lily/`.
- **Projects:** `src/pages/projects/*.md`, one Markdown file per project. Add a file to add a project.
- **Figures:** `python3 scripts/figures.py` and `python3 scripts/figures_vidvo.py` redraw every figure into `public/fig/`. Each project has its own kind of figure. Real data: `scripts/nightly-snapshot.json` (the pipeline's published data) and `scripts/bts-air-cargo.json` (BTS Monthly Transportation Statistics); the world outline is Natural Earth via world-atlas.
- **Design:** placeholders in `src/data/site.js` until the real pieces arrive.
- **Profile:** experience, selected work, education and skills, all from `src/data/site.js`.

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static site in dist/
```

Every push to `main` builds the site and publishes it to GitHub Pages
(Settings → Pages → Source: GitHub Actions).
