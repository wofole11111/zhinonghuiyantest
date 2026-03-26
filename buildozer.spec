[app]

title = 智农慧眼
package.name = zhinonghuiyan
package.domain = org.agri
version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,kv
source.main = main.py

requirements = python3,kivy==2.3.0,Pillow==10.3.0

# 修改这里：android.arch 改成 android.archs（加s）
android.archs = arm64-v8a

# 删除这一行（如果存在）
# android.sdk = 30

# 保留这些
android.api = 30
android.minapi = 21
android.ndk = 23b

android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.app_name = 智农慧眼

log_level = 2

[buildozer]

bin_dir = ./bin
buildozer_dir = ~/.buildozer