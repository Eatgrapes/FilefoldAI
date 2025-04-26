# FilefoldAI/Initialization.py
import os
import json
import platform
import subprocess
import google.generativeai as genai
from pathlib import Path
from openai import OpenAI

def check_api_validity(api_key, model_type):
    """验证API密钥有效性"""
    try:
        if model_type == "gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content("Test connection")
            return response.text is not None
        elif model_type == "deepseek":
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "user", "content": "Test connection"}],
                max_tokens=10,
                temperature=0
            )
            return bool(response.choices[0].message.content)
    except Exception as e:
        print(f"验证错误: {str(e)}")
        return False

def main():
    """主初始化函数"""
    data_dir = Path("FilefoldAI_data")
    data_dir.mkdir(exist_ok=True)
    api_file = data_dir / "api.json"

    # 模型选择
    while True:
        model_choice = input("请选择AI模型 (1)Gemini (2)DeepSeek-R1: ").strip()
        if model_choice in ["1", "2"]:
            model_type = "gemini" if model_choice == "1" else "deepseek"
            break
        print("无效选择，请输入1或2")

    # 加载现有配置
    config = {"api_key": "", "model_type": model_type}
    if api_file.exists() and api_file.stat().st_size > 0:
        with open(api_file, 'r') as f:
            existing_config = json.load(f)
            config.update(existing_config)

    # 密钥验证逻辑
    if config["model_type"] == model_type and config["api_key"]:
        choice = input(f"检测到已存在{model_type.upper()} API密钥({config['api_key'][:4]}...)，是否重新输入？(y/n): ")
        if choice.lower() != 'y':
            print("跳过API输入步骤...")
            return install_dependencies()

    # API输入验证循环
    while True:
        api_key = input(f"请输入{model_type.upper()} API密钥：").strip()
        if check_api_validity(api_key, model_type):
            config.update({"api_key": api_key, "model_type": model_type})
            with open(api_file, 'w') as f:
                json.dump(config, f, indent=2)
            break
        else:
            print("\033[91mAPI验证失败！\033[0m")
            retry = input("是否重新输入？(y/n): ").strip().lower()
            if retry != 'y':
                print("继续使用无效API可能导致后续功能异常！")
                break

    install_dependencies()

def install_dependencies():
    """安装所需依赖"""
    required_packages = ['google-generativeai', 'pyqt6', 'python-dotenv', 'openai']
    system = platform.system()
    
    # 系统特定依赖
    if system == "Linux":
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"], check=True)
    elif system == "Windows":
        pass

    # 通用Python包安装
    for pkg in required_packages:
        try:
            __import__(pkg.split('-')[0].replace('_', '-'))
        except ImportError:
            subprocess.run(["pip", "install", pkg], check=True)

    print("初始化完成！请运行 Run.py")  # 统一提示信息

if __name__ == "__main__":
    main()
