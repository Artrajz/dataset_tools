import importlib
import sys

if __name__ == '__main__':
    # 填写相同路径就是用处理过后的音频覆盖原来的音频
    input_base_path = r"J:\datasets\raw"
    output_path = r"J:\datasets\datasets"

    # 重采样+格式化为wav
    print("重采样+格式化为wav")
    resample_and_reformat_module = importlib.import_module('resample_and_reformat')
    processed_path = resample_and_reformat_module.resample_and_reformat(input_base_path,output_path)
    print(processed_path)
    del sys.modules['resample_and_reformat']

    # 标注
    print("开始标注")
    funasr_audio_files_module = importlib.import_module('asr_script')
    funasr_audio_files_module.funasr_audio_files(processed_path)
    del sys.modules['asr_script']

    # 去除英文文本并合并成一个txt文件
    print("去除英文文本并合并成一个txt文件")
    clean_and_merge_module = importlib.import_module('clean_and_merge')
    all_txt = clean_and_merge_module.clean_and_merge(processed_path)
    print(all_txt)
    del sys.modules['clean_and_merge']

    # 标点恢复
    print("标点恢复")
    punctuation_restoration_module = importlib.import_module('punctuation_restoration')
    finished_txt = punctuation_restoration_module.punctuation_restoration(all_txt)
    print(finished_txt)
    del sys.modules['punctuation_restoration']

