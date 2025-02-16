# FilefoldAI - 你的智能文件整理助手 📂✨

欢迎来到 **FilefoldAI**，一个用 AI 帮你自动整理文件的工具！如果你是一个文件混乱到连自己都找不到的人，那么这个项目就是为你量身打造的。我们利用 Gemini 2.0 Flash 模型，让你的文件自动归类

(虽然之前有大佬做了这个相似的项目，功能比我多，但是需要ollama本地ai部署，对于配置差的人不友好，所以我做了个这个)

---

## 项目介绍 🚀

FilefoldAI 是一个基于 Python 的文件整理工具，它通过 Gemini 2.0 Flash 模型自动分析文件名，并根据文件内容智能创建文件夹，将文件移动到对应的文件夹中。无论是游戏、文档、图片还是其他文件，FilefoldAI 都能帮你整理得井井有条。

### 主要功能：
- **自动分类**：根据文件名智能分类，支持中英文文件夹命名，还可以自定义语言。
- **跨平台支持**：支持 Linux 和 Windows 系统。
- **日志记录**：每次整理都会生成日志文件，方便追踪文件移动记录。
- **自定义语言**：如果你不喜欢默认的中英文分类名，还可以自定义文件夹语言！

---

## 如何使用？ 🤔
### 下载文件
首先点击大绿色按钮，点击"Download zip"然后解压到一个地方就可以了，或者前往[Release](https://github.com/Eatgrapes/FilefoldAI/releases)下载
### 1. 安装依赖
实际上，你可以直接运行Initialization.py输入完apikey之后会自动安装依赖，但是如果失败的话请手动安装:

```bash
pip install google-generativeai python-dotenv
```

如果你在 Windows 上使用 GUI 版本，还需要安装 PyQt6：

```bash
pip install pyqt6
```

### 2. 初始化配置
运行 `Initialization.py` 来设置你的 Gemini API 密钥。如果没有密钥，可以去 [Google AI Studio](https://aistudio.google.com/apikey) 获取（中国内地用户可能需要 VPN）。

```bash
python Initialization.py
```

按照提示输入 API 密钥，程序会自动检测密钥是否有效，并安装所需的依赖。

### 3. 运行整理工具

#### Linux 用户 🐧
运行 `linux_Run.py`，选择要整理的目录和文件夹语言，剩下的交给 AI 吧！

```bash
python linux_Run.py
```

#### Windows 用户 🪟
直接双击 `Windows_Run.py`，或者通过命令行运行：

```bash
python Windows_Run.py
```

你会看到一个简洁的 GUI 界面，选择目录和语言后，点击“开始整理”即可。

---

## 声明 📜

这个项目的大部分代码是由 AI 生成的（感谢 Deepseek 的辛勤工作！），小部分是由开发者修改和优化的。如果你发现任何问题或有改进建议，欢迎提出来！我们会在未来的版本中不断完善。

### 关于 API 和模型
- **API**：目前只支持 Gemini API，未来可能会增加对其他模型的支持。
- **模型**：默认使用 Gemini 2.0 Flash 模型，暂时不支持切换模型。如果你有特殊需求，可以手动修改代码（但我们不保证效果）。

---

## 遇到问题？ 🐛

如果你在使用过程中遇到任何问题，比如：
- AI 分类不准确
- 文件移动失败
- 其他奇奇怪怪的 bug

欢迎在项目的 [Issues](https://github.com/Eatgrapes/FilefoldAI/issues) 页面提出来！我们会尽快修复，也可以提意见

(此外，如果你是手机版termux的linux，如果出错，你可以试试用虚拟化环境运行)
