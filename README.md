# Desktop Pet

一个基于 Python `tkinter` 的桌面宠物示例项目。

## 当前已实现

- 首次启动时弹出宠物选择界面
- 可选择 `小兔`、`小猫`、`小狗`
- 选择结果会保存到 `data/settings.json`
- 鼠标在窗口外时，宠物会朝鼠标方向移动
- 鼠标进入窗口后，宠物眼神会跟随鼠标

## 运行方式

确保本机已安装 Python 3，然后在项目根目录执行：

```bash
python main.py
```

## 目录结构

```text
.
├── main.py
├── desktop_pet
│   ├── app.py
│   ├── pets.py
│   ├── scene.py
│   ├── selection.py
│   └── settings.py
└── data
```
