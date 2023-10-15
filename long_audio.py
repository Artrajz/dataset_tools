import glob
import os

from pydub import AudioSegment
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    vad_model='damo/speech_fsmn_vad_zh-cn-16k-common-pytorch',
    punc_model='damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch',
)


def recog(audio_path):
    rec_result = inference_pipeline(audio_in=audio_path)
    return rec_result


def clip(audio_path, rec_result, input_base_path, output_dir="datasets", min_time=3000, max_time=15000):
    rel_path = os.path.relpath(audio_path, start=input_base_path)
    output_path = os.path.join(output_dir, rel_path)
    output_dir, file_name_with_extension = os.path.split(output_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    os.makedirs(output_dir, exist_ok=True)
    speaker_name = os.path.basename(os.path.dirname(audio_path))

    audio = AudioSegment.from_file(audio_path)

    sentences = rec_result['sentences']
    start_time = 0
    text = ""
    continue_clip = False
    i = 0
    sentences_num = len(sentences)
    lines = []

    if len(audio) <= max_time:
        output_file = os.path.join(output_dir, f"{file_name}{file_extension}")
        audio.export(output_file, format="wav")
        for sentence in sentences:
            text += sentence['text']
        lines.append(f"{output_file}|{speaker_name}|ZH|{text}\n")
        return lines

    for num, sentence in enumerate(sentences):
        if not continue_clip:
            start_time = sentence['ts_list'][0][0]

        end_time = sentence['ts_list'][-1][1]
        text += sentence['text']
        segment_time = end_time - start_time

        if segment_time > min_time or num == sentences_num - 1:
            if num == sentences_num - 1:
                end_time = -1
            sliced_audio = audio[start_time:end_time]
            output_file = os.path.join(output_dir, f"{file_name}_{i}{file_extension}")
            sliced_audio.export(output_file, format="wav")
            lines.append(f"{output_file}|{speaker_name}|ZH|{text}\n")
            text = ""
            continue_clip = False
            i += 1
        else:
            continue_clip = True

    return lines


def clip_all(input_path, output_dir="datasets", min_time=3000, max_time=15000):
    audio_files = glob.glob(os.path.join(input_path, "**", "*.*"), recursive=True)
    lines = []
    for audio_path in audio_files:
        rec_result = recog(audio_path)

        lines.extend(clip(audio_path, rec_result, input_base_path=input_path, output_dir=output_dir, min_time=min_time,
                          max_time=max_time))

    save_path = "all.txt"
    with open(save_path, "w", encoding='utf8') as f:
        f.writelines(lines)
    return save_path


if __name__ == '__main__':
    clip_all('cache', output_dir="datasets")
