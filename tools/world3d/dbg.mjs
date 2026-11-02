import fs from "fs";
const ep = process.argv[2], t = +process.argv[3];
const html = fs.readFileSync(ep + "/index.html", "utf8");
const T = JSON.parse(html.match(/window.__T = (.*?);\n/)[1]);
const { path } = await import(ep + "/assets/world/engine.js");
const plot = (await import(ep + "/assets/world/director.js")).default(T);
for (const [n, a] of Object.entries(plot.actors)) { const p = path(a.path)(t); console.log(n, p.x.toFixed(1), p.z.toFixed(1)); }
