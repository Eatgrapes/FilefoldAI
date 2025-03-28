import sys
import json
import time
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QComboBox, QInputDialog
)
from PyQt6.QtCore import Qt
import google.generativeai as genai
from openai import OpenAI  # 新增导入

class FileOrganizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mapping = {}
        self.target_dir = ""

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('FilefoldAI - Windows版')
        
        # 目录选择组件
        self.dir_label = QLabel('目标目录:', self)
        self.dir_label.move(20, 20)
        
        self.dir_input = QLineEdit(self)
        self.dir_input.setGeometry(100, 20, 300, 25)
        
        self.browse_btn = QPushButton('浏览...', self)
        self.browse_btn.setGeometry(420, 20, 80, 25)
        self.browse_btn.clicked.connect(self.select_directory)
        
        # 语言选择组件
        self.lang_label = QLabel('分类语言:', self)
        self.lang_label.move(20, 60)
        
        self.lang_combo = QComboBox(self)
        self.lang_combo.addItems(['中文', '英文', '自定义'])
        self.lang_combo.setGeometry(100, 60, 150, 25)
        
        # 执行按钮
        self.run_btn = QPushButton('开始整理', self)
        self.run_btn.setGeometry(250, 100, 100, 30)
        self.run_btn.clicked.connect(self.start_organize)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择目录")
        if dir_path:
            self.dir_input.setText(dir_path)
            self.target_dir = dir_path
            
    def load_config(self):
        api_file = Path("FilefoldAI_data/api.json")
        if not api_file.exists():
            QMessageBox.critical(self, "错误", "未找到API配置文件！")
            return None
        with open(api_file, 'r') as f:
            return json.load(f)
    
    def get_ai_mapping(self, filenames, lang):
        config = self.load_config()
        if not config:
            return {}

        prompt = f"""根据以下文件名生成分类映射，严格使用{lang}创建文件夹名称：
    分类规则：
 
    文档类（.pdf/.docx/.xlsx）→ "文档"
    图片类（.jpg/.png/.gif）→ "图片"
    视频类（.mp4/.avi）→ "视频"
    压缩文件（.zip/.rar）→ "压缩包"
    你可以自定义名称
    如果是其他语言，请不要随便分类，比如一些文件随便分类到other文件夹是不允许的，要思考后分类

    格式要求：严格使用 {{"filename":"category"}} 的JSON格式
    
    示例输入：["game.exe", "photo.jpg", "unknown_file"]
    示例输出：{{"game.exe": "游戏", "photo.jpg": "图片", "unknown_file": "其他"}}

    实际文件列表：
    {filenames}
    """
        
        if config["model_type"] == "gemini":
            genai.configure(api_key=config['api_key'])
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            result = response.text
        else:
            try:
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
            except Exception as e:
                QMessageBox.critical(self, "API错误", f"DeepSeek调用失败: {str(e)}")
                return {}

        try:
            cleaned = result.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "格式错误", f"解析失败: {str(e)}\n原始响应: {result[:200]}...")
            return {}

    def process_files(self):
        log = []
        moved_files = 0
        for filename, category in self.mapping.items():
            src = Path(self.target_dir) / filename
            if not src.exists():
                continue
                
            dest_dir = Path(self.target_dir) / category
            dest_dir.mkdir(exist_ok=True)
            dest = dest_dir / filename
            
            try:
                src.rename(dest)
                log.append(f"文件 '{filename}' 移动到 '{category}'")
                moved_files += 1
            except Exception as e:
                log.append(f"移动失败：{filename} → {str(e)}")
        
        # 保存日志
        msg = QMessageBox()
        msg.setText(f"成功移动 {moved_files}/{len(self.mapping)} 个文件\n是否保存日志？")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            log_dir = Path("FilefoldAI_log")
            log_dir.mkdir(exist_ok=True)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            with open(log_dir / f"log_{timestamp}.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(log))

    def start_organize(self):
        self.target_dir = self.dir_input.text().strip()
        if not self.target_dir:
            QMessageBox.warning(self, "错误", "请先选择目录！")
            return

        # 语言选择逻辑
        lang_choice = self.lang_combo.currentText()
        if lang_choice == "自定义":
            lang, ok = QInputDialog.getText(self, "输入语言", "请输入分类语言:")
            if not ok or not lang.strip():
                QMessageBox.warning(self, "错误", "请输入有效的分类语言！")
                return
            lang = lang.strip()
        else:
            lang = lang_choice

        # 文件检查
        target_path = Path(self.target_dir)
        if not target_path.exists():
            QMessageBox.warning(self, "错误", "目录不存在！")
            return
            
        filenames = [f.name for f in target_path.iterdir() if f.is_file()]
        if not filenames:
            QMessageBox.warning(self, "错误", "目标目录中没有文件！")
            return

        # 处理过程
        QMessageBox.information(self, "提示", "AI正在分析文件，请稍候...")
        self.mapping = self.get_ai_mapping(filenames, lang)
        if self.mapping:
            self.process_files()
            QMessageBox.information(self, "完成", f"成功整理 {len(self.mapping)} 个文件！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerGUI()
    window.show()
    sys.exit(app.exec_())
