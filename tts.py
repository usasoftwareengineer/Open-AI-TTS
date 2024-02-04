import os
from pathlib import Path
from openai import OpenAI
import datetime

# 환경 변수에서 OpenAI API 키 가져오기
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("환경 변수에서 OPENAI_API_KEY를 찾을 수 없습니다.")

client = OpenAI(api_key=api_key)

try:
    # 입력 파일 경로 설정
    input_file_path = Path(__file__).parent / "input.txt"
    
    # 입력 파일 존재 확인
    if not input_file_path.exists():
        raise FileNotFoundError(f"{input_file_path} 파일을 찾을 수 없습니다.")

    # 입력 파일에서 텍스트 읽기, UTF-8 인코딩 사용
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # OpenAI의 음성 생성 API 호출
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=input_text
    )

    # 현재 시간을 기반으로 고유한 파일 이름 생성
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file_name = f"output_{timestamp}.mp3"
    output_file_path = Path(__file__).parent / output_file_name

    # 생성된 음성 데이터를 파일로 저장
    response.stream_to_file(output_file_path)

    print(f"음성 파일이 {output_file_path}에 저장되었습니다.")

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"에러가 발생했습니다: {e}")