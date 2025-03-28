# FilefoldAI - 你的智能文件整理助手 📂✨

欢迎来到 **FilefoldAI**，一个用 AI 帮你自动整理文件的工具！如果你是一个文件混乱到连自己都找不到的人，那么这个项目就是为你量身打造的。我们支持 Gemini 和 DeepSeek-R1 模型，让你的文件自动归类

(虽然之前有大佬做了这个相似的项目，功能比我多，但是需要ollama本地ai部署，对于配置差的人不友好，所以我做了个这个)

---

## 项目介绍 🚀

FilefoldAI 是一个基于 Python 的文件整理工具，它通过 AI 模型自动分析文件名，并根据文件内容智能创建文件夹，将文件移动到对应的文件夹中。无论是游戏、文档、图片还是其他文件，FilefoldAI 都能帮你整理得井井有条。

### 主要功能：
- **双模型支持**：自由选择 Gemini 2.0 Flash 或 DeepSeek-R1 模型
- **自动分类**：根据文件名智能分类，支持中英文文件夹命名，还可以自定义语言
- **跨平台支持**：支持 Linux 和 Windows 系统
- **日志记录**：每次整理都会生成日志文件，方便追踪文件移动记录
- **自定义语言**：如果你不喜欢默认的中英文分类名，还可以自定义文件夹语言！

---

## 如何使用？ 🤔
### 下载文件
首先点击大绿色按钮，点击"Download zip"然后解压到一个地方就可以了，或者前往[Release](https://github.com/Eatgrapes/FilefoldAI/releases)下载

### 1. 安装依赖
建议先手动安装核心依赖：

```bash
# 基础依赖
pip install google-generativeai openai python-dotenv

# Windows GUI 额外依赖
pip install pyqt6

# Linux 系统依赖
sudo apt-get install python3-tk
```

### 2. 初始化配置
运行 `Initialization.py` 来设置：

```bash
python Initialization.py
```

按照提示：
1. 选择要使用的AI模型（Gemini 或 DeepSeek-R1）
2. 输入对应模型的API密钥：
   - Gemini 密钥获取：[Google AI Studio](https://aistudio.google.com/apikey)
   - DeepSeek 密钥获取：[DeepSeek Console](https://api.deepseek.com)
3. 程序会自动验证密钥并安装缺少的依赖

### 3. 运行整理工具

#### Linux 用户 🐧
```bash
python linux_Run.py
```

#### Windows 用户 🪟
直接双击 `Windows_Run.py`，或通过命令行运行：
```bash
python Windows_Run.py
```

---

## 声明 📜

这个项目的大部分代码是由 AI 生成的（感谢 Deepseek 的辛勤工作！），小部分是由开发者修改和优化的。如果你发现任何问题或有改进建议，欢迎提出来！我们会在未来的版本中不断完善。

### 关于 API 和模型
- **支持模型**：目前支持 Gemini 2.0 Flash 和 DeepSeek-R1
- **API 要求**：需要对应平台的API密钥
- **模型切换**：重新运行 Initialization.py 即可切换模型

---

## 遇到问题？ 🐛

常见问题解决：
1. **依赖安装失败**：尝试手动安装（见上方安装步骤）
2. **API验证失败**：检查密钥是否正确，或尝试重新输入
3. **分类不准确**：尝试更换模型或调整提示词

欢迎在项目的 [Issues](https://github.com/Eatgrapes/FilefoldAI/issues) 页面提出来！我们会尽快修复，也可以提意见

(手机版Termux用户建议使用虚拟化环境运行)
