import glob
import os
import re
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import logging

logging.getLogger('modelscope').setLevel(logging.WARNING)

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch')


# 标注+标点恢复，组合使用，需要更高显存，而且同样是根据文本来加标点
# inference_pipeline = pipeline(
#     task=Tasks.auto_speech_recognition,
#     model='damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
#     vad_model='damo/speech_fsmn_vad_zh-cn-16k-common-pytorch',
#     punc_model='damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch',
# )


def process_audio(audio_file, speaker_name):
    rec_result = inference_pipeline(audio_in=audio_file)
    # print(rec_result)
    result = rec_result.get("text")
    text_format = f"{audio_file}|{speaker_name}|ZH|{result}\n"  # 保存文本格式
    return text_format


def funasr_audio_files(input_path, max_processes=2):
    # 查找二级目录
    subdirs = [d for d in glob.glob(os.path.join(input_path, '*')) if os.path.isdir(d)]

    all_audio_files = []
    subdir_map = {}
    for subdir in subdirs:
        subdir_name = os.path.basename(subdir)
        # 在子目录中搜索所有WAV音频文件
        audio_files = glob.glob(os.path.join(subdir, "*.wav"), recursive=False)
        audio_files = sorted(audio_files, key=lambda s: int(re.findall(r'(\d+)\.wav$', s)[0]))
        all_audio_files.extend(audio_files)
        for audio_file in audio_files:
            subdir_map[audio_file] = subdir_name
    
    # 多进程
    with ProcessPoolExecutor(max_processes) as executor:
        speaker_names = [subdir_map[audio] for audio in all_audio_files]
        results = list(tqdm(executor.map(process_audio, all_audio_files, speaker_names), total=len(all_audio_files)))

    for text, audio_file in zip(results, all_audio_files):
        subdir_name = subdir_map[audio_file]
        saved_filename = os.path.join(input_path, f"{subdir_name}.txt")
        with open(saved_filename, 'a', encoding='utf8') as f:
            f.write(text)


if __name__ == '__main__':
    input_base_path = r"datasets_processed"
    funasr_audio_files(input_base_path)
    print(f"处理完成")
