import glob
import os
import re


"""
进行简单的数据清洗，过于简单以至于仍需要手动清洗()
有能力的可以改一改，训练如果报错可能就是存在有背景音乐的音频
""" 

def filter_line(line):
    text = line.split("|")[-1].strip()
    # 去除文本识别为None的
    if text == 'None':
        return False
    # 去除文本识别出英文的
    if re.search("[a-zA-z]", text):
        return False

    return True


def filter_text(input_path):
    all_lines = []
    
    with open(input_path, "r", encoding='utf8') as f:
        all_lines.extend(f.readlines())

    filtered_lines = [line for line in all_lines if filter_line(line)]
    save_path = input_path
    with open(save_path, 'w', encoding='utf8') as out_file:
        out_file.writelines(filtered_lines)
    return save_path


if __name__ == '__main__':
    # 该脚本是将它们做简单的清洗
    # 保存到all.txt文件中
    input_base_path = r"all.txt"
    save_path = filter_text(input_base_path)
    print(save_path)
