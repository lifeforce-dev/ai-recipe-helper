# GitHub Pages deployment

This app auto-deploys the `web` folder to GitHub Pages on every push to the `release` branch.

Steps (one-time):
- In your repo settings → Pages, set Source to `GitHub Actions`.
- Create a `release` branch and push.

Usage:
- Merge to `release`. The workflow builds Vite with `VITE_BASE=/ai-recipe-helper/` and deploys `web/dist`.
- App will be available at `https://<your-username>.github.io/ai-recipe-helper/`.

Dev:
- `npm ci` then `npm run dev` in `web/`.
