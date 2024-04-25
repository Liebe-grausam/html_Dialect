import os
import librosa
import soundfile as sf

def pitch_shift_audio(phoneme_with_pitch, output_dir,consonant_list = ["'m","#","b","f","m","p","ph","t","v","'l","'n","h","j","k","kh","ng","ny","s","sh","th","ts","tsh","w","y","z","zh"]):
    """
    对音频文件进行变调并保存结果。
    
    参数:
    phoneme_with_pitch (list): 包含音频文件名和升降半音数的元组列表。
    output_dir (str): 输出音频文件的目录。
    """
    
    # 确保输出文件夹存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    files_with_pitch = []
    for phoneme, pitch in phoneme_with_pitch:
        if phoneme in consonant_list:            
            path = os.path.join(script_dir, "./consonant", f"{phoneme}.ogg")
        else:
            path = os.path.join(script_dir, "./vowel", f"{phoneme}.ogg")
        
        files_with_pitch.append((path, pitch))


    for input_file, pitch in files_with_pitch:
        # 构建输入和输出文件路径
        # input_file = os.path.join(script_dir, 'output_vowel', f"{phoneme}.ogg")
        file_name = os.path.basename(input_file)
        output_file = os.path.join(output_dir, file_name)

        # 加载音频文件并使用soundfile作为加载器
        y, sr = librosa.load(input_file, sr=None, res_type='kaiser_fast')

        # 如果pitch不为0，则进行变调
        if pitch != 0:
            y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch)

            # 保存变调后的音频文件
            sf.write(output_file, y_shifted, sr)
        else:
            # 如果pitch为0，则直接复制音频文件
            sf.write(output_file, y, sr)

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

    # 定义音素和对应的升降半音数
    # 获取用户输入的字符串
    input_str = input("please input the value of phoneme_with_pitch, for example, [('f', 0), ('a', -2), ('t', 0), ('ei', 0)]): ")

    # 使用 eval 函数将输入的字符串转换为列表
    phoneme_with_pitch = eval(input_str)


    # phoneme_with_pitch = [("f", 0), ("a", -2), ("t", 0), ("ei", 0)]
    file_name_prefix = "".join([item[0] for item in phoneme_with_pitch])
    # 设置输出目录
    output_dir = os.path.join(script_dir, 'modulate',file_name_prefix)

    # 调用函数进行变调
    pitch_shift_audio(phoneme_with_pitch, output_dir)



    # 获取脚本所在目录
    # script_dir = os.path.dirname(os.path.abspath(__file__))

    # 定义输入目录、音素列表和输出文件路径
    # input_dir = os.path.join(script_dir, 'output_modulate')
    phonemes = [item[0] for item in phoneme_with_pitch]
    # phonemes = ['f', 'a', 't', 'ei']
    # file_name_prefix = ''.join(phonemes)
    input_dir = os.path.join(script_dir, 'modulate',file_name_prefix)

    output_file = os.path.join(script_dir, 'combined',f"{file_name_prefix}.ogg")

    # 调用函数进行合并
    combine_audio_files(input_dir, phonemes, output_file)
