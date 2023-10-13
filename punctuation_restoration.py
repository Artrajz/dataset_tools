import os.path

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

import logging

"""
恢复标点符号，由于是根据文本来恢复的，所以可能与音频的实际停顿有所差异。
"""

logging.getLogger('modelscope').setLevel(logging.WARNING)

inference_pipeline = pipeline(
    task=Tasks.punctuation,
    model='damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch',
    model_revision="v1.1.7")


def punctuation_restoration(input_path):
    all_lines = []

    with open(input_path, "r", encoding='utf8') as f:
        all_lines.extend(f.readlines())

    updated_lines = []

    for line in all_lines:
        parts = line.split("|")
        text = parts[-1].strip()

        rec_result = inference_pipeline(text_in=text)
        result = rec_result.get("text")

        parts[-1] = result  # 替换最后一个部分，即text
        new_line = "|".join(parts) + "\n"
        updated_lines.append(new_line)

    directory, filename = os.path.split(input_path)
    filename = filename.split('.')[0] + ".list"
    save_path = os.path.join(directory, filename)
    with open(save_path, 'w', encoding='utf8') as out_file:
        out_file.writelines(updated_lines)
    return save_path


if __name__ == '__main__':
    inpute_path = r"datasets/all.txt"
    save_path = punctuation_restoration(inpute_path)
    print(save_path)
