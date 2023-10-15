import glob
import os
import shutil

import ffmpeg
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg', '.mp4']
TARGET_FORMAT = '.wav'


def is_audio_file(filepath):
    # 检查文件是否为音频文件
    return os.path.splitext(filepath)[1].lower() in AUDIO_EXTENSIONS


def get_audio_sample_rate(file_path):
    probe = ffmpeg.probe(file_path)
    audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
    if audio_stream:
        sample_rate = int(audio_stream['sample_rate'])
        return sample_rate
    else:
        return None


def process_audio(input_path, output_dir, input_base_path, target_sample_rate=44100):
    # 保留目录结构
    rel_path = os.path.relpath(input_path, start=input_base_path)
    output_path = os.path.join(output_dir, rel_path)
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    current_format = os.path.splitext(input_path)[1].lower()
    output_file_path = os.path.splitext(output_path)[0] + TARGET_FORMAT

    # 检查新文件夹中是否已经存在相同文件名的音频文件
    if os.path.exists(output_file_path):
        output_file_sample_rate = get_audio_sample_rate(output_file_path)
        # 如果新文件夹中采样率与采样率相同，则跳过该音频
        if output_file_sample_rate == target_sample_rate:
            return

    current_sample_rate = get_audio_sample_rate(input_path)
    if current_format != TARGET_FORMAT or current_sample_rate != target_sample_rate:

        ffmpeg.input(input_path).output(output_file_path, ar=target_sample_rate).global_args('-loglevel',
                                                                                             'error').global_args(
            '-y').run()
    else:
        # 直接复制文件到新文件夹
        shutil.copy2(input_path, output_file_path)


def convert(input_path, output_path=None, target_sample_rate=44100, max_processes=os.cpu_count()):
    # 如果没有指定输出路径，则使用默认名称
    if output_path is None:
        output_path = f"{input_path}_processed"

    os.makedirs(output_path, exist_ok=True)

    # 在子目录中搜索所有音频文件
    audio_files = glob.glob(os.path.join(input_path, "**", "*.*"), recursive=True)
    audio_files = [f for f in audio_files if is_audio_file(f)]

    # 多进程
    with ProcessPoolExecutor(max_processes) as executor:
        list(tqdm(
            executor.map(process_audio, audio_files, [output_path] * len(audio_files), [input_path] * len(audio_files),
                         [target_sample_rate] * len(audio_files)), total=len(audio_files)))

    return output_path


if __name__ == '__main__':
    output_path = convert(r"raw", output_path=r"datasets")
    print(output_path)
