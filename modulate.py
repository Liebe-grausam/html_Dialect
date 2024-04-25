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
            path = os.path.join(script_dir, "./output_consonant", f"{phoneme}.ogg")
        else:
            path = os.path.join(script_dir, "./output_vowel", f"{phoneme}.ogg")
        
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

# 示例调用
if __name__ == "__main__":
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 定义音素和对应的升降半音数
    phoneme_with_pitch = [("f", 0), ("a", -2), ("t", 0), ("ei", 0)]
    file_name_prefix = "".join([item[0] for item in phoneme_with_pitch])
    # 设置输出目录
    output_dir = os.path.join(script_dir, 'output_modulate',file_name_prefix)

    # 调用函数进行变调
    pitch_shift_audio(phoneme_with_pitch, output_dir)
