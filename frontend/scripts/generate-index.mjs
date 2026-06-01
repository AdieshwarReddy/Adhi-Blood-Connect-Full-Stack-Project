/**
 * Post-build script for Netlify/static deployment.
 * Generates an index.html in dist/client that bootstraps the SPA
 * by loading the main JS bundle and CSS stylesheet.
 */
import { readdirSync, writeFileSync } from "fs";
import { join } from "path";

const clientDir = join(process.cwd(), "dist", "client");
const assetsDir = join(clientDir, "assets");

const files = readdirSync(assetsDir);
const mainJs = files.find((f) => f.startsWith("index-") && f.endsWith(".js") && !f.includes("kwb3") && !f.includes("Dc15"));
const mainCss = files.find((f) => f.startsWith("styles-") && f.endsWith(".css"));
const routerJs = files.find((f) => f.startsWith("index-kwb") && f.endsWith(".js"));

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Adhi Bloodconnect — Intelligent Blood Donation</title>
    <meta name="description" content="AI-powered blood donation platform connecting donors, patients, and hospitals." />
    <link rel="stylesheet" href="/assets/${mainCss}" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/assets/${routerJs || mainJs}"></script>
    <script type="module" src="/assets/${mainJs}"></script>
  </body>
</html>
`;

writeFileSync(join(clientDir, "index.html"), html);
console.log("✅ Generated index.html for static deployment");
