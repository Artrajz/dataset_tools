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


def filter_and_merge_txt(txt_files):
    all_lines = []

    for txt_file in txt_files:
        with open(txt_file, "r", encoding='utf8') as f:
            all_lines.extend(f.readlines())

    filtered_lines = [line for line in all_lines if filter_line(line)]

    return filtered_lines


def clean_and_merge(input_path):
    txt_files = glob.glob(os.path.join(input_path, "*.txt"), recursive=False)
    filtered_lines = filter_and_merge_txt(txt_files)
    directory = input_path
    filename = "all.txt"
    save_path = os.path.join(directory, filename)
    with open(save_path, 'w', encoding='utf8') as out_file:
        out_file.writelines(filtered_lines)
    return save_path


if __name__ == '__main__':
    # 输入路径是datasets目录，目录下可能会有多个txt标注文件（当然只有一个也是可以的），该脚本是将它们做简单的清洗并合并为一个txt文件
    # 保存到cleaned.list文件中
    input_base_path = r"H:\datasets"
    save_path = clean_and_merge(input_base_path)
    print(save_path)
