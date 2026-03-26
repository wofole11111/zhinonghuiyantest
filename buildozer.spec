[app]

# 应用基本信息
title = 智农慧眼
package.name = zhihui_nongyan
package.domain = org.agri
version = 1.0.0

# 应用图标（需要准备icon.png）
# icon.filename = icon.png

# 源代码文件
source.include_exts = py,png,jpg,kv,atlas

# 主要启动文件
source.dir = .
source.main = main.py

# 支持的架构
android.arch = arm64-v8a, armeabi-v7a

# 权限
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# 应用需求
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30

# 所需模块
requirements = python3,kivy==2.3.0,Pillow==10.3.0

# 应用图标
android.icon = icon.png
# 应用名称（中文）
android.app_name = 智农慧眼

# 存储权限
android.gradle_dependencies = 'androidx.appcompat:appcompat:1.4.1'
android.add_src =

# 相机权限
android.whitelist = CAMERA

# 日志级别
log_level = 2

# 警告忽略
warn_on_root = 0

# 打包为APK
android.release = True
android.keystore = my-release-key.keystore
android.keystore_alias = my-key-alias

[buildozer]

# 构建工具路径
buildozer_dir = ~/.buildozer

# 二进制文件目录
bin_dir = ./bin