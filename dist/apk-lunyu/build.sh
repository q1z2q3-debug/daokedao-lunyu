#!/usr/bin/env bash
# 本地构建《道可道之论语》APK（不依赖 gradle，手工走 aapt2 → javac → d8 → zipalign → apksigner）
# 依赖：JDK 11+、Android build-tools 35.0.0、platforms/android-35。
#   SDK_ROOT=/path/to/sdk ./build.sh
set -euo pipefail
cd "$(dirname "$0")"

SDK_ROOT=${SDK_ROOT:-/home/user/apkbuild/sdk}
BT="$SDK_ROOT/build-tools/35.0.0"
JAR="$SDK_ROOT/platforms/android-35/android.jar"
CODE=16042
NAME=0.16.42
OUT="../../dist/道可道之论语-v$NAME.apk"

rm -rf build && mkdir -p build/res build/gen build/classes build/dex

# 源 Manifest 不带 package（供 gradle 用 namespace）；aapt2 手工链需要，故生成一份临时件
sed 's|<manifest xmlns:android="http://schemas.android.com/apk/res/android">|<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.runze.daokedaolunyu">|' \
  app/src/main/AndroidManifest.xml > build/AndroidManifest.xml

"$BT/aapt2" compile --dir app/src/main/res -o build/res/resources.zip
"$BT/aapt2" link -o build/unsigned.apk \
  -I "$JAR" \
  --manifest build/AndroidManifest.xml \
  -A app/src/main/assets \
  --java build/gen \
  --min-sdk-version 21 --target-sdk-version 35 \
  --version-code "$CODE" --version-name "$NAME" \
  build/res/resources.zip

javac -source 11 -target 11 -encoding UTF-8 \
  -classpath "$JAR" \
  -d build/classes $(find app/src/main/java -name '*.java')

"$BT/d8" --lib "$JAR" --min-api 21 --release \
  --output build/dex $(find build/classes -name '*.class')

python3 - <<'PY'
import zipfile, os
# d8 输出 build/dex/classes.dex；需以 classes.dex 置于包根
src = 'build/dex/classes.dex'
if os.path.exists(src):
    with zipfile.ZipFile('build/unsigned.apk', 'a', zipfile.ZIP_DEFLATED) as z:
        z.write(src, 'classes.dex')
PY

"$BT/zipalign" -p -f 4 build/unsigned.apk build/aligned.apk

KS=.debug.keystore
if [ ! -f "$KS" ]; then
  keytool -genkeypair -keystore "$KS" -alias androiddebugkey -storepass android -keypass android \
    -dname "CN=Runze, O=Daokedao, C=CN" -keyalg RSA -keysize 2048 -validity 10000 >/dev/null 2>&1
fi

"$BT/apksigner" sign --ks "$KS" --ks-pass pass:android --key-pass pass:android \
  --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
  --out "$OUT" build/aligned.apk

"$BT/apksigner" verify --print-certs "$OUT" | head -6
ls -l "$OUT"
sha256sum "$OUT"
