"""
Perplexity Sonar AI 챗봇 애플리케이션
Perplexity API를 활용한 스트리밍 방식의 AI 챗봇 애플리케이션입니다.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# 모듈 임포트
from modules.api_client import PerplexityClient, process_stream_response, display_metadata
from modules.file_processor import create_file_attachment_message
from modules.ui_components import (
    setup_page, initialize_session_state, render_sidebar,
    render_file_upload_section, render_chat_history, render_cancel_button
)

# 환경 변수 로드
load_dotenv()

# Perplexity API 키 가져오기
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    st.error("API 키가 설정되지 않았습니다. .env 파일에 PERPLEXITY_API_KEY를 설정해주세요.")
    st.stop()

# Perplexity API 클라이언트 초기화
perplexity_client = PerplexityClient(api_key)

# 페이지 설정
setup_page()

# 세션 상태 초기화
initialize_session_state()

# 사이드바 렌더링
settings = render_sidebar()
model = settings["model"]
temperature = settings["temperature"]
max_tokens = settings["max_tokens"]
system_message = settings["system_message"]

# 메인 화면 제목
st.title("Perplexity AI 챗봇 🤖")

# 파일 업로드 섹션 렌더링
render_file_upload_section()

# 채팅 기록 렌더링
render_chat_history()

# 응답 생성 취소 버튼 렌더링
render_cancel_button()

# 사용자 입력
prompt = st.chat_input("메시지를 입력하세요...", disabled=st.session_state.generating)

# 사용자가 메시지를 입력했을 때
if prompt:
    content = prompt

    # 파일 첨부 메시지 생성
    file_message = create_file_attachment_message(st.session_state.uploaded_files)
    if file_message:
        #file_prompt = {"type": "image_url", "image_url": file_message}
        content = [{"type": "text", "text": prompt}] + file_message

    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": content})
    with st.chat_message("user"):
        st.write(prompt)

    # 생성 상태 설정
    st.session_state.generating = True
    st.session_state.cancel_generation = False

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # 메시지 준비
        messages = [{"role": "system", "content": system_message}]
        messages.extend([
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ])

        # MCP 서버 설정
        mcp_servers = []
        for server in st.session_state.mcp_servers:
            mcp_servers.append({"url": server})

        # 스트리밍 응답 처리
        try:
            # print(f"{messages}\n\n")
            # 응답 생성
            stream = perplexity_client.generate_stream_response(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                use_mcp=st.session_state.enable_mcp,
                mcp_servers=mcp_servers if mcp_servers else None
            )

            # 응답 처리 및 표시
            full_response, metadata = process_stream_response(
                stream,
                message_placeholder,
                lambda: st.session_state.cancel_generation
            )

            # 메타데이터 표시
            display_metadata(metadata)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
            raise e

    # 생성 상태 해제
    st.session_state.generating = False
    st.session_state.cancel_generation = False

    # AI 응답을 세션 상태에 저장
    if full_response:  # 취소된 경우 빈 응답이 될 수 있음
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 페이지 새로고침
    # st.rerun()

# 푸터
st.markdown("---")
st.markdown("Powered by Perplexity Sonar API")
