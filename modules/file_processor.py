"""
파일 처리 모듈
다양한 유형의 파일을 처리하고 관리하는 기능을 제공합니다.
"""

import io
import json
import base64
import datetime
import pandas as pd
import streamlit as st

def process_file(file):
    """
    업로드된 파일을 처리합니다.

    Args:
        file: 업로드된 파일 객체

    Returns:
        dict: 처리된 파일 정보
    """
    file_type = file.type
    file_content = file.read()

    # 파일 유형에 따른 처리
    if file_type.startswith('text/'):
        # 텍스트 파일
        try:
            text_content = file_content.decode('utf-8')
            return True, {
                "type": "text",
                "content": text_content,
                "summary": f"텍스트 파일 ({len(text_content)} 자)"
            }
        except UnicodeDecodeError as e:
            return False, f"텍스트 파일 처리 오류: ({str(e)})"

    elif file_type.startswith('image/'):
        # 이미지 파일
        if file_type.endswith('png') or file_type.endswith('jpeg') or file_type.endswith('gif') or file_type.endswith('webp'):
            return True, {
                "type": "image",
                "content": base64.b64encode(file_content).decode('utf-8'),
                "summary": f"이미지 파일 ({file_type}, {len(file_content)} 바이트)"
            }
        return False, "지원되지 않는 이미지 파일 형식입니다."

    # elif file_type == 'application/pdf':
    #     # PDF 파일
    #     return {
    #         "type": "pdf",
    #         "content": base64.b64encode(file_content).decode('utf-8'),
    #         "summary": f"PDF 파일 ({len(file_content)} 바이트)"
    #     }

    # elif file_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
    #     # Excel 파일
    #     try:
    #         df = pd.read_excel(io.BytesIO(file_content))
    #         return {
    #             "type": "excel",
    #             "content": df.to_json(orient='records'),
    #             "summary": f"Excel 파일 ({df.shape[0]} 행, {df.shape[1]} 열)"
    #         }
    #     except Exception as e:
    #         return {
    #             "type": "binary",
    #             "content": base64.b64encode(file_content).decode('utf-8'),
    #             "summary": f"Excel 파일 처리 오류: {str(e)}"
    #         }

    elif file_type in ['application/json']:
        # JSON 파일
        try:
            json_data = json.loads(file_content)
            return True, {
                "type": "json",
                "content": json.dumps(json_data, ensure_ascii=False),
                "summary": "JSON 파일"
            }
        except Exception as e:
            return False, f"JSON 파일 처리 오류: ({str(e)})"
            # return {
            #     "type": "binary",
            #     "content": base64.b64encode(file_content).decode('utf-8'),
            #     "summary": f"JSON 파일 처리 오류: {str(e)}"
            # }

    return False, "지원되지 않는 파일 형식입니다."
    # 기타 파일
    # return {
    #     "type": "binary",
    #     "content": base64.b64encode(file_content).decode('utf-8'),
    #     "summary": f"파일 ({file_type}, {len(file_content)} 바이트)"
    # }


def create_file_attachment_message(files):
    """
    파일 첨부 메시지를 생성합니다.

    Args:
        files (dict): 파일 정보 딕셔너리

    Returns:
        str: 생성된 메시지
    """
    if not files:
        return ""

    # message = "다음 파일을 분석해주세요:\n\n"
    message = []
    for filename, file_info in files.items():
        content = f"- {filename}: {file_info['summary']}\n"

        # 텍스트 파일인 경우 내용 추가
        if file_info['type'] in ['text', 'json']:
            message.append({"type": "text", "content": f"{content}\n```{file_info['type']}\n{file_info['content'][:10000]}\n```"})
            # message += f"\n```\n{file_info['content'][:10000]}\n```\n\n"

        elif file_info['type'] == 'image':
            message.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{file_info['content']}"}})
            # message += f"\n```\n{file_info['content']}\n```\n\n"

    return message


def save_conversation(filename, messages, model, system_message):
    """
    대화 내용을 파일로 저장합니다.

    Args:
        filename (str): 저장할 파일명
        messages (list): 대화 메시지 목록
        model (str): 사용한 모델 이름
        system_message (str): 시스템 메시지

    Returns:
        str: 저장된 파일명
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not filename:
        filename = f"conversation_{timestamp}.json"
    elif not filename.endswith('.json'):
        filename = f"{filename}.json"

    conversation_data = {
        "timestamp": timestamp,
        "model": model,
        "system_message": system_message,
        "messages": messages
    }

    # JSON 파일로 저장
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(conversation_data, f, ensure_ascii=False, indent=2)

    return filename


def load_conversation(uploaded_file):
    """
    업로드된 파일에서 대화 내용을 불러옵니다.

    Args:
        uploaded_file: 업로드된 파일 객체

    Returns:
        tuple: (성공 여부, 메시지)
    """
    try:
        content = uploaded_file.read()
        data = json.loads(content)

        # 필수 키 확인
        if "messages" not in data:
            return False, "유효하지 않은 대화 파일입니다."

        # 메시지 형식 확인
        for msg in data["messages"]:
            if "role" not in msg or "content" not in msg:
                return False, "메시지 형식이 올바르지 않습니다."

        return True, data
    except Exception as e:
        return False, f"파일을 불러오는 중 오류가 발생했습니다: {str(e)}"
