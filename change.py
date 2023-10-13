import os.path
from random import shuffle

with open(r'all.list.cleaned', 'r', encoding='utf8') as f:
    all_lines = f.readlines()

updated_lines = []

speakers = set()

# 修改音频的路径，比如说原本标注出来的路径是绝对路径，如果要将数据集转移到别的机器上训练最好转成相对路径
# 修改后的路径为"datasets/speaker_name/audio_name"
for line in all_lines:
    parts = line.split("|")
    new_path = "datasets"
    speaker_name = os.path.basename(os.path.dirname(parts[0]))
    speakers.add(speaker_name)
    audio_name = os.path.basename(parts[0])
    parts[0] = f"{new_path}/{speaker_name}/{audio_name}"
    parts[1] = speaker_name
    new_line = "|".join(parts)
    updated_lines.append(new_line)

# print(updated_lines)
# print(speakers)
print(len(speakers))
size = 0.2

with open(r'all.list.cleaned', 'w', encoding='utf8') as f:
    f.writelines(updated_lines)

# 将speakers集合转换为列表并排序
speakers_list = sorted(list(speakers))
print(speakers_list)

# 对updated_lines重新排序，使前len(speakers)行按照speakers的顺序排列
sorted_head_lines = []

for speaker in speakers_list:
    # 为每个speaker找到第一行并将其添加到sorted_head_lines
    for line in updated_lines:
        line_speaker = line.split("|")[1]
        if speaker == line_speaker:
            sorted_head_lines.append(line)
            updated_lines.remove(line)  # 从updated_lines中删除已被选择的行
            break

# 随机打乱
shuffle(updated_lines)

# 合并两部分
updated_lines = sorted_head_lines + updated_lines

# 分割训练集和验证集
with open(r'train.list', 'w', encoding='utf8') as f:
    f.writelines(updated_lines[:int(len(updated_lines) * (1 - size))])

with open(r'val.list', 'w', encoding='utf8') as f:
    f.writelines(updated_lines[int(len(updated_lines) * (1 - size)):])
