const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getNavegadores: () => ipcRenderer.invoke('get-navegadores'),
  getSites: () => ipcRenderer.invoke('get-sites'),
  openBrowser: (browser, url) => ipcRenderer.invoke('open-browser', browser, url),
  closeBrowser: (browser) => ipcRenderer.invoke('close-browser', browser),
  takeScreenshot: () => ipcRenderer.invoke('take-screenshot'),
  scrollDown: () => ipcRenderer.invoke('scroll-down'),
  scrollUp: () => ipcRenderer.invoke('scroll-up'),
  typeText: (text) => ipcRenderer.invoke('type-text', text),
  openUrl: (browser, url) => ipcRenderer.invoke('open-url', browser, url),
  openScreenshotFolder: () => ipcRenderer.invoke('open-screenshot-folder'),
});
