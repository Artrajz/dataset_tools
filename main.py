import importlib
import sys

if __name__ == '__main__':
    # 填写相同路径就是用处理过后的音频覆盖原来的音频
    input_path = r"raw"
    output_path = r"datasets"
    cache_path = r"cache"

    print("1：输入全为短音频\n"
          "2：输入为长音视频（短音频也可以，但处理会比任务1慢）\n"
          "请选择任务：", end="")
    task_type = int(input())

    if task_type == 1:
        # 重采样+格式化为wav
        print("重采样+格式化为wav")
        convert_module = importlib.import_module('convert')
        processed_path = convert_module.convert(input_path, output_path)
        print(processed_path)
        del sys.modules['convert']

        # 标注
        print("开始标注")
        funasr_audio_files_module = importlib.import_module('asr_script')
        processed_path = funasr_audio_files_module.funasr_audio_files(processed_path)
        print(processed_path)
        del sys.modules['asr_script']

        # 简单清洗，去除英文文本文件
        print("简单清洗")
        filter_module = importlib.import_module('filter_text')
        processed_path = filter_module.filter_text(processed_path)
        print(processed_path)
        del sys.modules['filter_text']

        # 标点恢复
        print("标点恢复")
        punctuation_restoration_module = importlib.import_module('punctuation_restoration')
        processed_path = punctuation_restoration_module.punctuation_restoration(processed_path)
        print(processed_path)
        del sys.modules['punctuation_restoration']
    elif task_type == 2:
        # 重采样+格式化为wav
        print("重采样+格式化为wav")
        convert_module = importlib.import_module('convert')
        processed_path = convert_module.convert(input_path, cache_path)
        print(processed_path)
        del sys.modules['convert']

        # 切片和标注
        print("切片和标注")
        funasr_audio_files_module = importlib.import_module('long_audio')
        processed_path = funasr_audio_files_module.clip_all(processed_path, output_path, min_time=3000, max_time=15000)
        print(processed_path)
        del sys.modules['long_audio']

        # 简单清洗，去除英文文本文件
        print("简单清洗")
        filter_module = importlib.import_module('filter_text')
        processed_path = filter_module.filter_text(processed_path)
        print(processed_path)
        del sys.modules['filter_text']
