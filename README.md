# Portfolio redesign (mockup)

A mockup of Sidanta Parajuli's personal website, restructured after
[terryli710.github.io](https://terryli710.github.io/): a full-screen hero, then calm hairline
lists; a Writing index with search and tags; long-form case studies with a sticky Contents list;
a Design gallery; and a Profile page that is the whole résumé.

- **Home:** the red spider lily in particles, then links, work, notes and design.
- **Writing:** `src/pages/writing/*.md`. Add a Markdown file to add a post.
- **Design:** placeholders in `src/data/site.js` until the real pieces arrive.
- **Profile:** experience, selected work, education and skills, all from `src/data/site.js`.

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static site in dist/
```

Every push to `main` builds the site and publishes it to GitHub Pages
(Settings → Pages → Source: GitHub Actions).
