; Установщик ИТП в духе Windows 98 — как окно соглашения в самом ИТП: классические серые кнопки и рамки
; (без оформления Windows 10/11), фон окна #C0C0C0, синяя полоса с мордочкой слева на первой и последней страницах.
XPStyle off
!define MUI_BGCOLOR C0C0C0
!define MUI_TEXTCOLOR 000000
!define MUI_INSTFILESPAGE_COLORS "000000 FFFFFF"
; низ окна (под страницей, где кнопки) — тоже серый 98-го, а не светлый Windows 11
!define MUI_CUSTOMFUNCTION_GUIINIT itpGuiInit
Function itpGuiInit
  SetCtlColors $HWNDPARENT 000000 C0C0C0
FunctionEnd
!define MUI_WELCOMEPAGE_TITLE "Установка ИТП"
!define MUI_WELCOMEPAGE_TEXT "Сейчас на компьютер будет установлен ИТП.$\r$\n$\r$\n«И так, программирование» — курс Python с нуля.$\r$\nИнтернет не нужен: Python уже внутри.$\r$\n$\r$\nНажмите «Далее», чтобы продолжить."
!define MUI_FINISHPAGE_TITLE "ИТП установлен"
!define MUI_FINISHPAGE_TEXT "Ярлык ИТП — на рабочем столе и в меню «Пуск».$\r$\n$\r$\nКролик уже ждёт!"

; классические кнопки и рамки: атрибут ставится ещё раз здесь — customHeader идёт после шаблона, последний побеждает
!macro customHeader
  XPStyle off
!macroend

!macro customWelcomePage
  !insertmacro MUI_PAGE_WELCOME
!macroend
