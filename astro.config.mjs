import { defineConfig } from 'astro/config';

// BASE is set by the GitHub Pages workflow to "/<repo>/"; locally the site lives at "/".
export default defineConfig({
  site: process.env.SITE || 'https://sidantap.github.io',
  base: process.env.BASE || '/',
  trailingSlash: 'always',
});
