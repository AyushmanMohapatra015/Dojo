// Local-only Chromium driver using Node's built-in WebSocket; no packages needed.
import { spawn } from 'node:child_process';
import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const [browser, folder, url] = process.argv.slice(2);
if (!url?.startsWith('http://127.0.0.1:')) throw new Error('local_url_required');
const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const child = spawn(browser, ['--headless', '--disable-gpu', '--no-first-run',
  '--no-default-browser-check', '--disable-background-networking', '--disable-sync',
  '--disable-extensions', '--remote-debugging-port=0', '--user-data-dir=' + join(folder, 'profile'),
  'about:blank'], { stdio: 'ignore', windowsHide: true });
let socket;
let id = 0;
const pending = new Map();
const send = (method, params = {}) => new Promise((resolve, reject) => {
  const key = ++id;
  const timer = setTimeout(() => { pending.delete(key); reject(new Error('debugger_timeout')); }, 10000);
  pending.set(key, { resolve, reject, timer });
  socket.send(JSON.stringify({ id: key, method, params }));
});
const evaluate = async (expression) => (await send('Runtime.evaluate', { expression, returnByValue: true })).result.value;
const press = async (key, code, virtualKey, modifiers = 0) => {
  for (const type of ['keyDown', 'keyUp']) {
    await send('Input.dispatchKeyEvent', { type, key, code, windowsVirtualKeyCode: virtualKey,
      nativeVirtualKeyCode: virtualKey, modifiers,
      ...(type === 'keyDown' && key === 'Enter' ? { text: '\r', unmodifiedText: '\r' } : {}) });
  }
  await pause(100);
};

try {
  let port;
  for (let attempt = 0; attempt < 80; attempt++) {
    try { port = Number((await readFile(join(folder, 'profile/DevToolsActivePort'), 'utf8')).split('\n')[0]); break; }
    catch { await pause(100); }
  }
  if (!port) throw new Error('debugger_unavailable');
  const pages = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  socket = new WebSocket(pages.find((page) => page.type === 'page').webSocketDebuggerUrl);
  await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
  socket.onmessage = (message) => {
    const value = JSON.parse(message.data);
    const task = pending.get(value.id);
    if (!task) return;
    clearTimeout(task.timer); pending.delete(value.id);
    if (value.error) task.reject(new Error('debugger_command_failed'));
    else task.resolve(value.result);
  };
  await send('Page.enable');
  const reports = [];
  for (const width of [320, 375, 768, 1440]) {
    await send('Emulation.setDeviceMetricsOverride', { width, height: 1000, deviceScaleFactor: 1, mobile: false });
    await send('Page.navigate', { url });
    let text;
    for (let attempt = 0; attempt < 100; attempt++) {
      await pause(100);
      const evaluated = await send('Runtime.evaluate', {
        expression: "document.getElementById('browser-check-result')?.textContent", returnByValue: true });
      text = evaluated.result?.value;
      if (text) break;
    }
    if (!text) throw new Error('probe_incomplete');
    const result = JSON.parse(text);
    result.requested_width = width;
    const table = await send('Runtime.evaluate', { expression: `(() => {
      const region=document.querySelector('[aria-label="Seed-level runs table"]');
      region.scrollLeft=0; region.focus();
      return {needed: region.scrollWidth > region.clientWidth};
    })()`, returnByValue: true });
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39 });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39 });
    await pause(250);
    const keyboard = await send('Runtime.evaluate', { expression: `(() => {
      const region=document.querySelector('[aria-label="Seed-level runs table"]');
      return {scrolled: region.scrollLeft > 0, focused: document.activeElement===region,
        focusVisible: region.matches(':focus-visible'), outlineWidth: parseFloat(getComputedStyle(region).outlineWidth)};
    })()`, returnByValue: true });
    result.tableKeyboardScroll = { ...table.result.value, ...keyboard.result.value };
    await evaluate("document.querySelector('.dataset-details__summary').focus()");
    await press(' ', 'Space', 32);
    const disclosureOpened = await evaluate("document.querySelector('.dataset-details').open");
    await press('Tab', 'Tab', 9);
    const datasetControlReached = await evaluate("document.activeElement.textContent.trim().startsWith('Load complete sample dataset')");
    await evaluate("document.querySelector('.dataset-details__summary').focus()");
    await press(' ', 'Space', 32);
    const disclosureClosed = await evaluate("!document.querySelector('.dataset-details').open");
    await evaluate("document.querySelector('.dojo-explorer-nav button').focus()");
    await press('Tab', 'Tab', 9);
    const compareReached = await evaluate("document.activeElement.textContent.trim()==='Compare'");
    await press('Enter', 'Enter', 13);
    const compareActivated = await evaluate("document.querySelector('.dojo-explorer-nav [aria-current=page]').textContent.trim()==='Compare'");
    await press('Tab', 'Tab', 9);
    const runsReached = await evaluate("document.activeElement.textContent.trim()==='Runs'");
    await press('Tab', 'Tab', 9, 8);
    const reverseTabWorks = await evaluate("document.activeElement.textContent.trim()==='Compare' && document.activeElement.matches(':focus-visible')");
    result.keyboardNavigation = { disclosureOpened, datasetControlReached, disclosureClosed,
      compareReached, compareActivated, runsReached, reverseTabWorks };
    await evaluate(`(() => {const button=document.createElement('button'); button.id='native-key-control';
      button.onclick=()=>button.dataset.activated='true'; document.body.append(button); button.focus();})()`);
    await press('Enter', 'Enter', 13);
    result.keyboardNavigation.nativeEnterControl = await evaluate("document.getElementById('native-key-control').dataset.activated==='true'");
    await evaluate("document.getElementById('native-key-control').remove()");
    if (width === 375 || width === 1440) {
      const base = await evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)");
      await evaluate("document.documentElement.style.fontSize='200%'");
      const scale = await evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)");
      const views = [];
      for (const name of ['Overview', 'Compare', 'Runs', 'Method']) {
        await evaluate(`[...document.querySelectorAll('.dojo-explorer-nav button')].find(b=>b.textContent.trim()==='${name}').click()`);
        await pause(250);
        views.push({ name, overflow: await evaluate('document.documentElement.scrollWidth>document.documentElement.clientWidth+1') });
      }
      result.largeText = { rootScale: scale/base, views };
      await evaluate('window.scrollTo(0,0)');
      const large = await send('Page.captureScreenshot', { format: 'png' });
      await writeFile(join(folder, `width-${width}-large-text.png`), Buffer.from(large.data, 'base64'), { flag: 'wx' });
      await evaluate("document.documentElement.style.fontSize=''");
    }
    await evaluate("[...document.querySelectorAll('.dojo-explorer-nav button')].find(b=>b.textContent.trim()==='Runs').click(); window.scrollTo(0,0)");
    await pause(200);
    reports.push(result);
    const screenshot = await send('Page.captureScreenshot', { format: 'png' });
    await writeFile(join(folder, `width-${width}.png`), Buffer.from(screenshot.data, 'base64'), { flag: 'wx' });
    if (width === 320) {
      await send('Runtime.evaluate', { expression: "[...document.querySelectorAll('.dojo-explorer-nav button')].find(b=>b.textContent.trim()==='Method').click(); window.scrollTo(0,0)" });
      await pause(300);
      const method = await send('Page.captureScreenshot', { format: 'png' });
      await writeFile(join(folder, 'width-320-method.png'), Buffer.from(method.data, 'base64'), { flag: 'wx' });
    }
    if (width === 375 || width === 1440) {
      await send('Runtime.evaluate', { expression: "[...document.querySelectorAll('.dojo-explorer-nav button')].find(b=>b.textContent.trim()==='Compare').click(); window.scrollTo(0,0)" });
      await pause(300);
      const compare = await send('Page.captureScreenshot', { format: 'png' });
      await writeFile(join(folder, `width-${width}-compare.png`), Buffer.from(compare.data, 'base64'), { flag: 'wx' });
    }
  }
  console.log(JSON.stringify(reports));
} finally {
  if (socket?.readyState === WebSocket.OPEN) {
    await send('Browser.close').catch(() => {});
    socket.close();
  }
  for (const task of pending.values()) clearTimeout(task.timer);
  if (child.exitCode === null) {
    await Promise.race([new Promise((resolve) => child.once('exit', resolve)), pause(2000)]);
    if (child.exitCode === null) child.kill();
  }
}
