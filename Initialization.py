import os
import json
import platform
import subprocess
import google.generativeai as genai
from pathlib import Path

def check_api_validity(api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Test connection")
        return response.text is not None
    except Exception as e:
        return False

def main():
    data_dir = Path("FilefoldAI_data")
    data_dir.mkdir(exist_ok=True)
    api_file = data_dir / "api.json"

    # API存在性检测
    if api_file.exists() and api_file.stat().st_size > 0:
        with open(api_file, 'r') as f:
            existing_api = json.load(f).get('api_key', '')
        choice = input(f"检测到已存在API密钥({existing_api[:4]}...)，是否重新输入？(y/n): ")
        if choice.lower() != 'y':
            print("跳过API输入步骤...")
            return install_dependencies()

    # API输入与验证循环
    while True:
        api_key = input("请输入Gemini API密钥(获取地址：https://aistudio.google.com/apikey)：")
        if check_api_validity(api_key):
            with open(api_file, 'w') as f:
                json.dump({"api_key": api_key}, f)
            break
        else:
            print("\033[91mAPI验证失败！\033[0m")
            retry = input("是否重新输入？(y/n): ")
            if retry.lower() != 'y':
                print("继续使用无效API可能导致后续功能异常！")
                break

    # 依赖安装逻辑
    install_dependencies()

def install_dependencies():
    required_packages = ['google-generativeai', 'pyqt6', 'python-dotenv']
    system = platform.system()
    
    # 系统特定依赖
    if system == "Linux":
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"], check=True)
    elif system == "Windows":
        pass  # 无额外系统依赖

    # 通用Python包安装
    for pkg in required_packages:
        try:
            __import__(pkg.split('-')[0].replace('_', '-'))
        except ImportError:
            subprocess.run(["pip", "install", pkg], check=True)

    print(f"初始化完成！请运行 {'linux_Run.py' if system == 'Linux' else 'Windows_Run.py'}")

if __name__ == "__main__":
    main()
