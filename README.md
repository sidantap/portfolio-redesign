# Portfolio redesign (mockup)

A mockup of Sidanta Parajuli's personal website, restructured after
[terryli710.github.io](https://terryli710.github.io/): a full-screen hero, then calm hairline
lists; a Projects index with search and tags; a page per project with a sticky Contents list;
a Design gallery; and a Profile page that is the whole résumé.

- **Home:** the red spider lily in particles, then links, projects, experience and design.
- **Projects:** `src/pages/projects/*.md`, one Markdown file per project. Add a file to add a project.
- **Design:** placeholders in `src/data/site.js` until the real pieces arrive.
- **Profile:** experience, selected work, education and skills, all from `src/data/site.js`.

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static site in dist/
```

Every push to `main` builds the site and publishes it to GitHub Pages
(Settings → Pages → Source: GitHub Actions).
