# Reverse Engineering Checklist (REA-First)

## 0. APK Login & Anti-Tamper Bypass (Priorité Absolue)
1. **REA Analysis** : Utilise `rea_call` avec `inspect-android-jni-bindings` pour voir si le login est en Java ou en natif.
2. **Anti-Tamper Detection** : Si l'APK contient des libs comme `librenderbase.so`, `libjiagu.so`, ou `libshella.so`, l'anti-tamper est **natif**.
3. **Login Java (Façade)** : Si le login est en Java, patch les méthodes `onCreate`, `m1211`, `Login` (Smali) pour forcer le succès.
4. **Anti-Tamper Natif (Le Vrai Boss)** : Si le login est en natif ou si l'APK crash après le patch Java :
   - Utilise `rea_call` avec `execute-rizin-command` sur le fichier `.so`.
   - Cherche les instructions `CMP` et `B.NE` (branches conditionnelles) qui vérifient la signature.
   - Patche l'instruction (`MOV` ou `NOP`) pour forcer le retour à `true`.
5. **Global Kill Neutralization** : Cherche toutes les occurrences de `Process.killProcess()` dans le Smali et remplace-les par `nop`.

## 1. APK Inventory
1. List entries with sizes and timestamps (`unzip -l`).
2. Read AndroidManifest.xml (`rea_call` avec `inspect-android-package`).
3. Detect protectors **before** unpacking (`apk-unpack-detect` ou `rea_call`).
4. Extract DEX and native libs to a private working directory.
5. Record architecture (arm64-v8a, armeabi-v7a) et ABI filters.

## 2. IL2CPP (Pour les jeux Unity)
1. Locate `libil2cpp.so` et `dump.cs`.
2. Confirm image/assembly and target version (`Il2CppDumper`).
3. Index dump.cs **before** searching (`dump_index.py`).
4. Search exact class/method/field names.
5. Resolve overloads by argument count (ne pas confondre `Camera.WorldToScreenPoint(Vector3)` et `(Vector3, Camera)`).
6. Record RVA and evidence line (toujours en hex).
7. Convert RVA to file offset (`rva_to_offset.py`) seulement si tu dois patcher le binaire.

## 3. Native (.so)
1. Parse ELF program headers for PT_LOAD mapping (`readelf -l`).
2. Determine base/RVA/file-offset convention (RVA = base + offset).
3. Use disassembly (`rizin` ou `Ghidra`) **seulement après** avoir trouvé le symbole.
4. Record architecture (ARM64) et calling convention (AAPCS64).

## 4. Runtime
1. Verify target process exists (`ps -A` ou `rea_call` avec `list-adb-processes`).
2. Verify privilege and ptrace capability (si pas de root, reporte "EACCES: ptrace not allowed").
3. If blocked, report the exact reason (pas de "je ne peux pas").
4. Do not claim runtime evidence from static data (ne dis pas "j'ai hooké" si tu n'as pas exécuté Frida).