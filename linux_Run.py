import os
import json
import time
from pathlib import Path
import google.generativeai as genai

def load_api():
    with open("FilefoldAI_data/api.json") as f:
        return json.load(f)['api_key']

def get_ai_mapping(filenames, lang):
    genai.configure(api_key=load_api())
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # 优化后的提示词模板
    prompt = f"""根据以下文件名生成分类映射，且严格使用{lang}创建文件夹名称：
    分类规则：
 
    文档类（.pdf/.docx/.xlsx）→ "文档"
    图片类（.jpg/.png/.gif）→ "图片"
    视频类（.mp4/.avi）→ "视频"
    压缩文件（.zip/.rar）→ "压缩包"
    你可以自定义名称
    还有，如果是其他语言，请不要随便分类，比如一些文件随便分类到other文件夹是不允许的，要思考后分类

    格式要求：严格使用 {{"filename":"category"}} 的JSON格式
    
    示例输入：["game.exe", "photo.jpg", "unknown_file"]
    示例输出：{{"game.exe": "游戏", "photo.jpg": "图片", "unknown_file": "其他"}}


    实际文件列表：
    {filenames}
    """
    
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text.replace('```json', '').replace('```', ''))
    except json.JSONDecodeError:
        raise ValueError("AI返回格式异常")

def main():
    target_dir = input("请输入要整理的目录路径：")
    lang_choice = input("选择文件夹语言 (1)中文 (2)英文 (3)自定义：")
    
    # 修复语言选择逻辑
    if lang_choice == '3':
        lang = input("请输入自定义语言：")
    else:
        lang = '中文' if lang_choice == '1' else '英文'

    filenames = [f.name for f in Path(target_dir).iterdir() if f.is_file()]
    print("AI正在分析文件...")
    try:
        mapping = get_ai_mapping(filenames, lang)
    except Exception as e:
        print(f"错误：{str(e)}")
        return
    
    log = []
    for filename, category in mapping.items():
        src = Path(target_dir) / filename
        if not src.exists():
            continue
            
        dest_dir = Path(target_dir) / category
        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / filename
        
        try:
            src.rename(dest)
            log.append(f"文件 '{filename}' 移动到 '{category}'")
        except Exception as e:
            log.append(f"移动失败：{filename} → {str(e)}")
    
    print("\n移动记录：")
    print('\n'.join(log))
    
    if input("是否保存日志？(y/n): ").lower() == 'y':
        log_dir = Path("FilefoldAI_log")
        log_dir.mkdir(exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        with open(log_dir / f"log_{timestamp}.txt", 'w') as f:
            f.write('\n'.join(log))

if __name__ == "__main__":
    main()