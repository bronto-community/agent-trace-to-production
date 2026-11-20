// shoot.mjs URL OUT [--click "text"]... [--w 1600] [--h 900] [--wait 1500] [--clip x,y,w,h]
// Real screenshots for the deck, taken from the running lab (Jaeger). Not part of the talk.
import { chromium } from 'playwright-chromium'
import { homedir } from 'node:os'
const args = process.argv.slice(2)
const [url, out] = args
const opt = (k, d) => { const i = args.indexOf('--' + k); return i > 0 ? args[i + 1] : d }
const clicks = args.flatMap((a, i) => (a === '--click' ? [args[i + 1]] : []))
const exe = `${homedir()}/Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell`
const browser = await chromium.launch({ executablePath: exe })
const page = await browser.newPage({ viewport: { width: +opt('w', 1600), height: +opt('h', 900) }, deviceScaleFactor: 2 })
await page.goto(url, { waitUntil: 'networkidle' })
await page.waitForTimeout(+opt('wait', 1500))
const widen = +opt('widen', 0) // widen Jaeger's span-name column by this many px
if (widen) {
  const h = page.locator('.VerticalResizer--dragger').first()
  const bb = await h.boundingBox().catch(() => null)
  if (bb) { const x = bb.x + bb.width / 2, y = bb.y + 60; await page.mouse.move(x, y); await page.mouse.down(); await page.mouse.move(x + widen, y, { steps: 10 }); await page.mouse.up(); await page.waitForTimeout(500) }
  else console.error('resizer not found:', await page.evaluate(() => [...document.querySelectorAll('[class*="Resizer"]')].map(e => e.className).slice(0, 5)))
}
for (const c of clicks) {
  const loc = c.startsWith('css=') ? page.locator(c.slice(4)).first() : page.getByText(c, { exact: false }).first()
  await loc.click({ timeout: 8000 }).catch(e => console.error('click failed:', c, e.message.split('\n')[0]))
  await page.waitForTimeout(600)
}
const sel = opt('sel') // clip to this element's box
if (sel) { const bb = await page.locator(sel).first().boundingBox(); await page.screenshot({ path: out, clip: { x: bb.x, y: bb.y, width: bb.width, height: Math.min(bb.height, +opt('maxh', 5000)) } }); await browser.close(); console.log('wrote', out, Math.round(bb.width) + 'x' + Math.round(bb.height)); process.exit(0) }
const clip = opt('clip')
if (clip) { const [x, y, width, height] = clip.split(',').map(Number); await page.screenshot({ path: out, clip: { x, y, width, height } }) }
else await page.screenshot({ path: out })
await browser.close()
console.log('wrote', out)
