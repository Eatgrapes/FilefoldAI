import os
import json
import time
import sys
import platform
from pathlib import Path

# ======================== 初始化检查 ========================

def check_environment():
    """检查运行环境并导入必要的模块"""
    # 尝试导入GUI相关模块
    gui_available = False
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QLabel, QLineEdit, QPushButton,
            QFileDialog, QMessageBox, QComboBox, QInputDialog
        )
        from PyQt6.QtCore import Qt
        gui_available = True
    except ImportError:
        print("⚠️ PyQt6未安装，GUI功能不可用")
        gui_available = False
    
    # 尝试导入AI相关模块
    try:
        import google.generativeai as genai
        from openai import OpenAI
        ai_available = True
    except ImportError as e:
        print(f"❌ AI模块导入失败: {str(e)}")
        ai_available = False
    
    return gui_available, ai_available

GUI_AVAILABLE, AI_AVAILABLE = check_environment()

# ======================== 核心功能 ========================

def load_config():
    """加载配置文件"""
    config_path = Path("FilefoldAI_data/api.json")
    if not config_path.exists():
        print("❌ 错误：未找到配置文件，请先运行Initialization.py")
        sys.exit(1)
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            if not all(key in config for key in ['api_key', 'model_type']):
                raise ValueError("配置文件缺少必要字段")
            return config
    except Exception as e:
        print(f"❌ 配置文件错误: {str(e)}")
        sys.exit(1)

def get_ai_mapping(filenames, lang):
    """获取AI分类结果"""
    config = load_config()
    
    prompt = f"""根据文件名生成分类映射，使用{lang}创建文件夹名称。要求：
    - 文档类（.pdf/.docx/.xlsx）→ "文档"
    - 图片类（.jpg/.png/.gif）→ "图片"
    - 视频类（.mp4/.avi）→ "视频"
    - 压缩文件（.zip/.rar）→ "压缩包"
    - 其他文件根据内容智能分类
    
    返回格式必须为严格的JSON，如：
    {{"file1.txt": "文档", "image.jpg": "图片"}}
    在过程中你可以运用搜索，比如遇到pcl2不知道这是什么就可以搜索，就可以知道这是个游戏启动器
    待分类文件：
    {filenames}
    """
    
    try:
        if config["model_type"] == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=config['api_key'])
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            result = response.text
        else:
            from openai import OpenAI
            client = OpenAI(
                api_key=config['api_key'],
                base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1024
            )
            result = response.choices[0].message.content
        
        # 清理AI返回结果
        cleaned = result.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned)
    except Exception as e:
        raise RuntimeError(f"AI处理失败: {str(e)}")

# ======================== 命令行界面 ========================

def run_cli():
    """命令行模式主逻辑"""
    print("\n📁 文件整理工具 (命令行模式)")
    
    # 获取目标目录
    while True:
        target_dir = input("请输入要整理的目录路径: ").strip()
        if Path(target_dir).exists():
            break
        print("❌ 目录不存在，请重新输入")
    
    # 选择语言
    lang_options = {'1': '中文', '2': '英文', '3': '自定义'}
    lang_choice = input("选择分类语言:\n1. 中文\n2. 英文\n3. 自定义\n请选择: ").strip()
    lang = lang_options.get(lang_choice, '中文')
    if lang == '自定义':
        lang = input("请输入自定义语言: ").strip()
    
    # 获取文件列表
    files = [f.name for f in Path(target_dir).iterdir() if f.is_file()]
    if not files:
        print("ℹ️ 目录中没有可处理的文件")
        return
    
    # AI处理
    print("🧠 AI正在分析文件...")
    try:
        mapping = get_ai_mapping(files, lang)
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        return
    
    # 执行文件移动
    success = 0
    log = []
    for filename, category in mapping.items():
        src = Path(target_dir) / filename
        if not src.exists():
            continue
            
        dest_dir = Path(target_dir) / category
        try:
            dest_dir.mkdir(exist_ok=True)
            src.rename(dest_dir / filename)
            log.append(f"成功: {filename} → {category}")
            success += 1
        except Exception as e:
            log.append(f"失败: {filename} → {str(e)}")
    
    # 显示结果
    print("\n".join(log))
    print(f"\n✅ 完成: 成功移动 {success}/{len(mapping)} 个文件")
    
    # 保存日志
    if input("是否保存日志？(y/n): ").lower() == 'y':
        log_dir = Path("FilefoldAI_log")
        log_dir.mkdir(exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        with open(log_dir / f"log_{timestamp}.txt", 'w', encoding='utf-8') as f:
            f.write("\n".join(log))
        print(f"📝 日志已保存到 {log_dir}")

# ======================== 图形界面 ========================

if GUI_AVAILABLE:
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QLabel, QLineEdit, QPushButton,
        QFileDialog, QMessageBox, QComboBox, QInputDialog
    )
    from PyQt6.QtCore import Qt

    class FileOrganizerApp(QWidget):
        """文件整理GUI应用"""
        def __init__(self):
            super().__init__()
            self.setWindowTitle("FilefoldAI")
            self.setFixedSize(500, 200)
            self.setup_ui()
            self.mapping = {}
        
        def setup_ui(self):
            """初始化界面组件"""
            # 目录选择
            self.dir_label = QLabel("目标目录:", self)
            self.dir_label.move(20, 20)
            
            self.dir_input = QLineEdit(self)
            self.dir_input.setGeometry(100, 20, 300, 25)
            
            self.browse_btn = QPushButton("浏览...", self)
            self.browse_btn.setGeometry(410, 20, 70, 25)
            self.browse_btn.clicked.connect(self.browse_directory)
            
            # 语言选择
            self.lang_label = QLabel("分类语言:", self)
            self.lang_label.move(20, 60)
            
            self.lang_combo = QComboBox(self)
            self.lang_combo.addItems(["中文", "英文", "自定义"])
            self.lang_combo.setGeometry(100, 60, 150, 25)
            
            # 执行按钮
            self.run_btn = QPushButton("开始整理", self)
            self.run_btn.setGeometry(200, 120, 100, 40)
            self.run_btn.clicked.connect(self.start_organizing)
        
        def browse_directory(self):
            """打开目录选择对话框"""
            dir_path = QFileDialog.getExistingDirectory(self, "选择目录")
            if dir_path:
                self.dir_input.setText(dir_path)
        
        def start_organizing(self):
            """开始整理流程"""
            target_dir = self.dir_input.text().strip()
            if not target_dir:
                QMessageBox.warning(self, "错误", "请先选择目录")
                return
            
            # 获取语言设置
            lang = self.lang_combo.currentText()
            if lang == "自定义":
                lang, ok = QInputDialog.getText(self, "自定义语言", "请输入分类语言:")
                if not ok or not lang.strip():
                    return
                lang = lang.strip()
            
            # 验证目录
            if not Path(target_dir).exists():
                QMessageBox.critical(self, "错误", "目录不存在")
                return
            
            # 获取文件列表
            files = [f.name for f in Path(target_dir).iterdir() if f.is_file()]
            if not files:
                QMessageBox.information(self, "提示", "目录中没有可处理的文件")
                return
            
            # 使用AI分类
            try:
                QMessageBox.information(self, "提示", "AI正在分析文件，请稍候...")
                self.mapping = get_ai_mapping(files, lang)
                self.process_files()
            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))
        
        def process_files(self):
            """执行文件移动操作"""
            log = []
            success = 0
            target_dir = self.dir_input.text()
            
            for filename, category in self.mapping.items():
                src = Path(target_dir) / filename
                if not src.exists():
                    continue
                
                dest_dir = Path(target_dir) / category
                try:
                    dest_dir.mkdir(exist_ok=True)
                    src.rename(dest_dir / filename)
                    log.append(f"{filename} → {category}")
                    success += 1
                except Exception as e:
                    log.append(f"{filename} 失败: {str(e)}")
            
            # 显示结果
            msg = QMessageBox()
            msg.setText(f"完成整理 {success} 个文件\n是否保存日志？")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if msg.exec() == QMessageBox.StandardButton.Yes:
                self.save_log(log)
        
        def save_log(self, log_entries):
            """保存日志文件"""
            log_dir = Path("FilefoldAI_log")
            log_dir.mkdir(exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            log_file = log_dir / f"gui_log_{timestamp}.txt"
            
            try:
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write("\n".join(log_entries))
                QMessageBox.information(self, "成功", f"日志已保存到:\n{log_file}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"日志保存失败:\n{str(e)}")

# ======================== 主程序入口 ========================

if __name__ == "__main__":
    # 选择运行模式
    if GUI_AVAILABLE and AI_AVAILABLE:
        print("检测到完整功能支持")
        use_gui = input("是否使用图形界面？(y/n): ").strip().lower() == 'y'
    else:
        use_gui = False
    
    # 启动对应模式
    if use_gui:
        app = QApplication(sys.argv)
        window = FileOrganizerApp()
        window.show()
        sys.exit(app.exec_())
    else:
        if not AI_AVAILABLE:
            print("❌ 错误：缺少必要的AI模块支持")
            sys.exit(1)
        run_cli()
