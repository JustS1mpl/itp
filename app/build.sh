#!/usr/bin/env bash
# Сборка приложений ИТП из готового out5.html (сначала: python build5.py в корне репозитория).
#   APK (раздавать файлом, RuStore) и AAB (Google Play) — app/dist/android/
#   EXE: установщик и переносная версия — app/dist/
# Окружение (JDK 21, Android SDK, кэши npm/Gradle/Electron) — в itp-tools/env.sh, всё на диске E.
set -e
cd "$(dirname "$0")"
. "../../itp-tools/env.sh"
cp ../out5.html www/index.html
npx cap sync android
(cd android && ./gradlew.bat --no-daemon assembleRelease bundleRelease)
mkdir -p dist/android
cp android/app/build/outputs/apk/release/app-release.apk dist/android/ITP.apk
cp android/app/build/outputs/bundle/release/app-release.aab dist/android/ITP.aab
npx electron-builder --win nsis portable
ls -la dist dist/android
