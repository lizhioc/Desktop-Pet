# Desktop Pet

一个基于 Python `tkinter` 开发的无边框桌面宠物项目。当前版本使用本地图片资源驱动 Q 版人物形象，支持男女角色选择、拖动、互动动作和移动模式切换。

## 已有功能

- 首次启动时弹出角色选择界面，可选择 `男生` 或 `女生`。
- 后续启动会记住上一次选择的角色和窗口位置。
- 程序图标使用羽毛图标，运行窗口和打包后的 exe 保持一致。
- 运行时生成的 `data` 文件夹会在 Windows 上自动设置为隐藏。
- 主窗口为无边框透明窗口，只显示桌宠人物本体。
- 站立状态会从当前角色的站立素材中随机切换，切换间隔为 `3-10` 秒随机。
- 按住桌宠可拖动位置，拖动时会显示当前角色的抓取姿态。
- 右键点击桌宠可打开退出菜单。
- 连续点击桌宠 `3` 次可重新打开角色选择界面。
- 左键点击桌宠可打开侧边互动菜单。
- 一级菜单包含 `互动` 和 `模式` 两个入口。
- `互动` 二级菜单包含 `摸头`、`揪耳朵`、`拍PP`、`喂蛋糕`、`喝饮料` 和 `返回`。
- 点击互动动作后会显示对应互动图片，`3` 秒后自动恢复站立姿态。
- `模式` 二级菜单包含 `自由`、`跟随` 和 `返回`。
- 跟随模式下，桌宠会根据鼠标相对方向切换左右移动素材，并缓慢跟随鼠标。
- 互动菜单默认显示在人物右侧，靠近屏幕边缘时会自动切换到另一侧。
- 互动菜单 `3` 秒无操作后会自动关闭。

## 运行方式

确保本机已安装 Python 3，然后在项目根目录执行：

```bash
python main.py
```

## 打包 exe

项目使用 PyInstaller 打包为 Windows 可执行文件。首次打包前先安装构建依赖：

```bash
python -m pip install -r requirements-build.txt
```

然后执行：

```powershell
.\build_exe.ps1
```

打包完成后，可执行文件会生成在：

```text
dist\DesktopPet.exe
```

`DesktopPet.exe` 会内置 Python 运行环境和项目素材，复制到其他 Windows 电脑后可以直接运行。运行时产生的角色选择和窗口位置记录会保存在 exe 同目录的 `data` 文件夹中。

如果重新打包后资源管理器里仍显示旧图标，可以先关闭资源管理器预览、删除旧的 `dist` 目录后重新打包，或把 exe 改个文件名再查看，这是 Windows 图标缓存导致的显示延迟。

## 素材目录

项目会从 `assets/pet` 下读取角色素材：

- `boy`：男生站立姿态。
- `girl`：女生站立姿态。
- `left`：向左移动动作。
- `right`：向右移动动作。
- `catch`：拖动抓取姿态。
- `interact`：互动动作姿态。

程序图标位于 `assets/icons`。

## 项目结构

```text
.
├── assets
│   ├── icons
│   └── pet
│       ├── boy
│       ├── girl
│       ├── left
│       ├── right
│       ├── catch
│       └── interact
├── data
├── desktop_pet
│   ├── app.py
│   ├── pets.py
│   ├── paths.py
│   ├── scene.py
│   ├── selection.py
│   └── settings.py
├── build_exe.ps1
├── DesktopPet.spec
├── main.py
├── requirements-build.txt
└── README.md
```
