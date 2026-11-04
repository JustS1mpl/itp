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
; обновление (владелец, 7.1.0): если ИТП уже установлен, установщик это видит (версия из записи об установке в реестре)
; и пишет «обновление с X до Y». Ставит в ту же папку поверх, старую версию убирает сам; прогресс лежит отдельно
; (%APPDATA%\ИТП) и не трогается. Тексты страниц — переменные, их заполняет customInit.
; Строки разбиты вручную: сама Windows переносила русский текст этой страницы посреди слова
!ifndef BUILD_UNINSTALLER
Var itpOld
Var itpWT
Var itpWX
Var itpFT
Var itpFX
!endif
!macro customInit
  ReadRegStr $itpOld HKCU "${UNINSTALL_REGISTRY_KEY}" DisplayVersion
  ${If} $itpOld == ""
    ReadRegStr $itpOld HKLM "${UNINSTALL_REGISTRY_KEY}" DisplayVersion
  ${EndIf}
  ${If} $itpOld == ""
    StrCpy $itpWT "Установка ИТП"
    StrCpy $itpWX "Сейчас на компьютер будет установлен$\r$\nИТП ${VERSION}.$\r$\n$\r$\n«И так, программирование» —$\r$\nкурс Python с нуля.$\r$\nИнтернет не нужен: Python уже внутри.$\r$\n$\r$\nНажмите «Далее», чтобы продолжить."
    StrCpy $itpFT "ИТП установлен"
    StrCpy $itpFX "Ярлык ИТП — на рабочем столе$\r$\nи в меню «Пуск».$\r$\n$\r$\nКролик уже ждёт!"
  ${ElseIf} $itpOld == "${VERSION}"
    StrCpy $itpWT "ИТП уже установлен"
    StrCpy $itpWX "На компьютере уже стоит ИТП ${VERSION} —$\r$\nэто последняя версия.$\r$\n$\r$\nЕго можно переустановить поверх, если$\r$\nчто-то сломалось. Прогресс, настройки$\r$\nи серия сохранятся.$\r$\n$\r$\nНажмите «Далее», чтобы переустановить,$\r$\nили «Отмена»."
    StrCpy $itpFT "ИТП переустановлен"
    StrCpy $itpFX "Весь прогресс на месте.$\r$\n$\r$\nКролик уже ждёт!"
  ${Else}
    StrCpy $itpWT "Обновление ИТП"
    StrCpy $itpWX "На компьютере стоит ИТП $itpOld.$\r$\nУстановщик обновит его до версии ${VERSION}$\r$\nв той же папке, поверх старой.$\r$\n$\r$\nЗаново ничего проходить не нужно:$\r$\nпрогресс, настройки и серия сохранятся.$\r$\n$\r$\nНажмите «Далее», чтобы обновить."
    StrCpy $itpFT "ИТП обновлён до ${VERSION}"
    StrCpy $itpFX "Было: $itpOld. Стало: ${VERSION}.$\r$\nВесь прогресс на месте.$\r$\n$\r$\nКролик уже ждёт!"
  ${EndIf}
!macroend
; только у установщика: у удаляльщика своих переменных нет
!ifndef BUILD_UNINSTALLER
!define MUI_WELCOMEPAGE_TITLE "$itpWT"
!define MUI_WELCOMEPAGE_TEXT "$itpWX"
!define MUI_FINISHPAGE_TITLE "$itpFT"
!define MUI_FINISHPAGE_TEXT "$itpFX"
!endif

; классические кнопки и рамки: атрибут ставится ещё раз здесь — customHeader идёт после шаблона, последний побеждает
!macro customHeader
  XPStyle off
!macroend

!macro customWelcomePage
  !insertmacro MUI_PAGE_WELCOME
!macroend
