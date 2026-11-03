// ИТП для Windows: окно с тем же ИТП.html, что и в браузере. Всё работает без интернета.
// Файлы (резервная копия, картинки, код .py) — окно «Сохранить как»; ссылки и почта — в системном браузере/почте.
const { app, BrowserWindow, shell, Menu, session } = require('electron')
const path = require('path')

// один экземпляр: второй запуск просто показывает уже открытое окно
if (!app.requestSingleInstanceLock()) app.quit()

let win
function create () {
  win = new BrowserWindow({
    width: 1200, height: 820, minWidth: 380, minHeight: 600,
    title: 'ИТП', backgroundColor: '#FBF7F5', show: false, autoHideMenuBar: true,
    icon: path.join(__dirname, '..', 'icons', 'icon.png'),
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, sandbox: true, spellcheck: false }
  })
  Menu.setApplicationMenu(null)
  win.loadFile(path.join(__dirname, '..', 'www', 'index.html'))
  win.once('ready-to-show', () => win.show())

  const outside = (u) => !u.startsWith('file:') && !u.startsWith('blob:') && !u.startsWith('data:') && !u.startsWith('about:')
  // новые окна и переходы наружу — в системе, а не внутри ИТП
  win.webContents.setWindowOpenHandler(({ url }) => { if (outside(url)) shell.openExternal(url); return { action: 'deny' } })
  win.webContents.on('will-navigate', (e, url) => { if (outside(url)) { e.preventDefault(); shell.openExternal(url) } })
  // F12 — инструменты разработчика, Ctrl+R — перезагрузка (меню скрыто)
  win.webContents.on('before-input-event', (e, i) => {
    if (i.type !== 'keyDown') return
    if (i.key === 'F12') win.webContents.toggleDevTools()
    else if (i.control && i.key.toLowerCase() === 'r') win.webContents.reload()
  })
}

app.on('second-instance', () => { if (win) { if (win.isMinimized()) win.restore(); win.focus() } })
app.whenReady().then(() => {
  // скачивание (blob-ссылки из ИТП) — всегда с окном «Сохранить как», в папку «Загрузки» по умолчанию
  session.defaultSession.on('will-download', (e, item) => {
    item.setSaveDialogOptions({ defaultPath: path.join(app.getPath('downloads'), item.getFilename()) })
  })
  create()
})
app.on('window-all-closed', () => app.quit())
