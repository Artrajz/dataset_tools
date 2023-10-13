import glob
import os
import shutil

import ffmpeg
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg']
TARGET_FORMAT = '.wav'


def is_audio_file(filepath):
    # 检查文件是否为音频文件
    return os.path.splitext(filepath)[1].lower() in AUDIO_EXTENSIONS


def process_audio(audio_file, output_dir, input_base_path, target_sample_rate=44100):
    # 保留目录结构
    rel_path = os.path.relpath(audio_file, start=input_base_path)
    output_file_path = os.path.join(output_dir, rel_path)
    output_file_dir = os.path.dirname(output_file_path)
    os.makedirs(output_file_dir, exist_ok=True)

    # 检查新文件夹中是否已经存在相同文件名的音频文件
    if os.path.exists(output_file_path):
        probe = ffmpeg.probe(output_file_path)
        current_sample_rate = int(probe['streams'][0]['sample_rate'])
        current_format = os.path.splitext(output_file_path)[1].lower()

        # 如果新文件夹中的音频格式和采样率与目标格式和采样率相同，则跳过该音频
        if current_format == TARGET_FORMAT and current_sample_rate == target_sample_rate:
            # print(f"Skipping {audio_file} (already exists in the output folder)")
            return

    # 如果当前格式不是目标格式或采样率与目标采样率不同，则进行转换
    probe = ffmpeg.probe(audio_file)
    current_sample_rate = int(probe['streams'][0]['sample_rate'])
    current_format = os.path.splitext(audio_file)[1].lower()
    if current_format != TARGET_FORMAT or current_sample_rate != target_sample_rate:
        output_file_path = os.path.splitext(output_file_path)[0] + TARGET_FORMAT
        ffmpeg.input(audio_file).output(output_file_path, ar=target_sample_rate).global_args('-loglevel', 'error').global_args('-y').run()
    else:
        # 直接复制文件到新文件夹
        shutil.copy2(audio_file, output_file_path)



def resample_and_reformat(input_path, output_path=None, target_sample_rate=44100, max_processes=os.cpu_count()):
    # 如果没有指定输出路径，则使用默认名称
    if output_path is None:
        output_path = f"{input_path}_processed"

    os.makedirs(output_path, exist_ok=True)

    # 在子目录中搜索所有音频文件
    audio_files = glob.glob(os.path.join(input_path, "**", "*.*"), recursive=True)
    audio_files = [f for f in audio_files if is_audio_file(f)]

    # 多进程
    with ProcessPoolExecutor(max_processes) as executor:
        list(tqdm(executor.map(process_audio, audio_files, [output_path] * len(audio_files), [input_path] * len(audio_files), [target_sample_rate] * len(audio_files)), total=len(audio_files)))

    return output_path


if __name__ == '__main__':
    input_base_path = r"raw"
    output_path = resample_and_reformat(input_base_path,output_path=r"datasets")
    print(output_path)
