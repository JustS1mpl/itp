// ИТП узнаёт, что запущен как программа для Windows (a_notify.js: NATIVE === 'win')
const { contextBridge } = require('electron')
contextBridge.exposeInMainWorld('itpDesk', { platform: process.platform })
