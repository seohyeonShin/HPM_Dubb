import re,os

def convert_vtt_to_srt(vtt_path, txt_path):
    # VTT 파일 열기
    with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
        lines = vtt_file.readlines()

    # 결과를 저장할 변수 초기화
    txt_content = ""
    index = 1  # SRT에서 각 자막의 인덱스는 1부터 시작합니다.

    # 한 번에 4줄씩 처리하기 위해 range를 설정합니다.
    for i in range(4, len(lines), 4):
        # 타임스탬프 줄 처리 (첫 번째 행)
        try:
            time_line = lines[i].strip().split(' ')[0] + ' --> ' + lines[i].strip().split(' ')[2]
            # 실제 대화 내용 (두 번째 행)
            dialogue_line = lines[i+2].strip()
            # 정규표현식으로 시간태그와 <c> 등을 제거 
            cleaned_text =re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', dialogue_line)
            cleaned_text =re.sub(r'<\/?c>', '', cleaned_text) 
            # SRT 형식에 맞게 내용 추가
            # srt_content += f"{index}\n{time_line}\n{cleaned_text}\n\n"
            txt_content += f"{cleaned_text}"" "
            index += 1
        except:
            print(f"Error format for {vtt_path}")

    # SRT 파일 쓰기
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(txt_content)
def vtt_to_txt(vtt_path, txt_path):
    with open(vtt_path, 'r') as vtt_file:
        lines = vtt_file.readlines()

    text_content = []
    for line in lines:
        # Skip VTT metadata or timestamp lines
        if not (line.startswith('NOTE') or line.startswith('WEBVTT') or '-->' in line):
            cleaned_line = line.strip()
            if cleaned_line:  # Add non-empty lines
                text_content.append(cleaned_line)

    # Combine lines into a single text block
    full_text = ' '.join(text_content)

    # Save to a txt file
    with open(txt_path, 'w') as txt_file:
        txt_file.write(full_text)

def convert_all_vtt_to_txt(wavs_dir, vtt_dir, output_dir):
    # List all WAV files in the specified directory
    # wav_files = [f for f in os.listdir(wavs_dir) if f.endswith('.wav')]
    vtt_files = [f for f in os.listdir(vtt_dir) if f.endswith('.vtt')]
    
    # Iterate over each WAV file to find its corresponding VTT file
    for vtt_file in vtt_files:
        base_name = os.path.splitext(vtt_file)[0].split('.')[0]
        vtt_path = os.path.join(vtt_dir, base_name + '.en.vtt')
        txt_path = os.path.join(output_dir, base_name + '.txt')
        wav_file = base_name + '.wav'
        # Check if the VTT file exists
        if os.path.exists(vtt_path):
            if base_name == '1yoOSIcsCyI':
                vtt_to_txt(vtt_path,txt_path)
            else:
                # Convert the VTT to SRT (assuming your function actually produces TXT, despite the name)
                convert_vtt_to_srt(vtt_path, txt_path)
        else:
            print(f"No VTT file found for {wav_file}")


def check_missing_pairs(directory):
    wav_files = {file[:-4] for file in os.listdir(directory) if file.endswith('.wav')}
    txt_files = {file[:-4] for file in os.listdir(directory) if file.endswith('.txt')}

    only_wav = wav_files - txt_files
    only_txt = txt_files - wav_files

    if only_wav:
        print("Files with only WAV:", ", ".join(only_wav))
    if only_txt:
        print("Files with only TXT:", ", ".join(only_txt))




corpus_dir = '/workspace/CODE/Lip2Wav/Dataset/chem/wavs_origin'
vtt_dir = '/workspace/CODE/Lip2Wav/Dataset/chem/vtt1'
output_dir = '/workspace/CODE/DATABASE/HPM/text' #'/workspace/CODE/Lip2Wav/Dataset/chem/corpus_1'
convert_all_vtt_to_txt(corpus_dir, vtt_dir, output_dir)
        
#         # Example usage
# directory = '/workspace/CODE/Lip2Wav/Dataset/chem/corpus_1'
# check_missing_pairs(directory)


