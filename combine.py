import os
from pydub import AudioSegment

def combine_audio_files(input_dir, phonemes, output_file):
    """
    合并给定目录中的音频文件，并保存为新的OGG文件。
    
    参数:
    input_dir (str): 输入音频文件所在的目录。
    phonemes (list): 音素列表。
    output_file (str): 输出音频文件的路径。
    """
    
    # 确保输出文件夹存在
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    # 创建一个空的AudioSegment对象来存储合并后的音频
    combined_audio = None

    for phoneme in phonemes:
        # 构建完整的文件路径
        file_path = os.path.join(input_dir, f"{phoneme}.ogg")

        # 加载音频文件
        audio = AudioSegment.from_file(file_path, format="ogg")

        if combined_audio is None:
            # fade_duration = len(audio)//6
            combined_audio = audio
        else:
            # 计算交叉淡入淡出的时长（取两个音频长度的四分之一作为交叉淡入淡出的时长）
            crossfade_duration = min(len(combined_audio), len(audio)) // 6

            # 添加交叉淡入淡出
            combined_audio = combined_audio.append(audio, crossfade=crossfade_duration)
            # combined_audio = combined_audio.append(audio.fade_in(crossfade_duration), crossfade=crossfade_duration)
           

    # 保存合并后的音频到新文件
    combined_audio.export(output_file, format="ogg")

# 示例调用
if __name__ == "__main__":
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 定义输入目录、音素列表和输出文件路径
    # input_dir = os.path.join(script_dir, 'output_modulate')
    phonemes = ['f', 'a', 't', 'ei']
    file_name_prefix = ''.join(phonemes)
    input_dir = os.path.join(script_dir, 'output_modulate',file_name_prefix)

    output_file = os.path.join(script_dir, 'output_combined',f"{file_name_prefix}.ogg")

    # 调用函数进行合并
    combine_audio_files(input_dir, phonemes, output_file)
