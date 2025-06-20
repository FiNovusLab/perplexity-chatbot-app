"""
UI 컴포넌트 모듈
Streamlit UI 컴포넌트 및 레이아웃 관련 기능을 제공합니다.
"""

import streamlit as st
from modules.file_processor import process_file, save_conversation, load_conversation

def setup_page():
    """
    페이지 기본 설정을 수행합니다.
    """
    st.set_page_config(
        page_title="Perplexity AI 챗봇",
        page_icon="🤖",
        layout="wide",
    )


def initialize_session_state():
    """
    세션 상태를 초기화합니다.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "metadata_history" not in st.session_state:
        st.session_state.metadata_history = []

    # if "enable_mcp" not in st.session_state:
    #     st.session_state.enable_mcp = False

    # if "mcp_servers" not in st.session_state:
    #     st.session_state.mcp_servers = []

    if "generating" not in st.session_state:
        st.session_state.generating = False

    if "cancel_generation" not in st.session_state:
        st.session_state.cancel_generation = False

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}


def render_sidebar():
    """
    사이드바 UI를 렌더링합니다.

    Returns:
        dict: 사이드바에서 설정된 값들
    """
    with st.sidebar:
        st.title("설정")

        # 모델 선택
        models = [
            "sonar-deep-research",
            "sonar-reasoning-pro",
            "sonar-reasoning",
            "sonar-pro",
            "sonar"
        ]

        model = st.selectbox(
            "모델 선택",
            options=models,
            index=4,  # sonar를 기본값으로 설정
        )
        st.session_state.model = model

        # 온도 설정
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="값이 높을수록 더 창의적인 응답을 생성합니다."
        )

        # 최대 토큰 설정
        max_tokens = st.slider(
            "최대 토큰 수",
            min_value=100,
            max_value=4000,
            value=1000,
            step=100,
            help="응답의 최대 길이를 설정합니다."
        )

        # 시스템 메시지 설정
        system_message = st.text_area(
            "시스템 메시지",
            value=st.session_state.get("system_message", "You are a helpful AI assistant."),
            help="AI의 역할과 행동을 정의합니다."
        )
        st.session_state.system_message = system_message

        # MCP 서버 설정
        # render_mcp_settings()

        # 대화 관리
        render_conversation_management()

        # 대화 초기화 버튼
        if st.button("대화 초기화"):
            st.session_state.messages = []
            st.session_state.uploaded_files = {}
            st.session_state.metadata_history = []
            st.rerun()

    return {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "system_message": system_message
    }


def render_mcp_settings():
    """MCP 서버 설정 UI를 렌더링합니다."""
    st.subheader("MCP 서버 설정")

    # MCP 기능 활성화 여부 선택
    enable_mcp = st.checkbox(
        "MCP 기능 활성화",
        value=st.session_state.get("enable_mcp", False),
        help="MCP(Model Context Protocol) 기능을 활성화합니다. 현재 OpenAI 라이브러리 버전과 호환성 문제가 있을 수 있습니다."
    )
    st.session_state.enable_mcp = enable_mcp

    if enable_mcp:
        mcp_server_url = st.text_input("MCP 서버 URL")

        if st.button("MCP 서버 추가"):
            if mcp_server_url and mcp_server_url not in st.session_state.mcp_servers:
                st.session_state.mcp_servers.append(mcp_server_url)

        # 등록된 MCP 서버 목록
        if st.session_state.mcp_servers:
            st.write("등록된 MCP 서버:")
            for i, server in enumerate(st.session_state.mcp_servers):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text(server)
                with col2:
                    if st.button("삭제", key=f"delete_{i}"):
                        st.session_state.mcp_servers.pop(i)
                        st.rerun()
    else:
        # MCP 기능이 비활성화되면 서버 목록 초기화
        if st.session_state.mcp_servers:
            st.session_state.mcp_servers = []


def render_conversation_management():
    """대화 저장 및 불러오기 UI를 렌더링합니다."""
    st.subheader("대화 관리")

    # 대화 저장
    save_filename = st.text_input("저장할 파일명 (선택사항)", key="save_filename")
    if st.button("대화 저장"):
        if st.session_state.messages:
            filename = save_conversation(
                save_filename,
                st.session_state.messages,
                st.session_state.get("model", "sonar"),
                st.session_state.get("system_message", "You are a helpful AI assistant.")
            )
            st.success(f"대화가 {filename} 파일로 저장되었습니다.")
        else:
            st.warning("저장할 대화 내용이 없습니다.")

    # 대화 불러오기
    uploaded_file = st.file_uploader("대화 파일 불러오기", type=["json"], key="conversation_file")
    if uploaded_file is not None:
        if st.button("불러오기"):
            success, result = load_conversation(uploaded_file)
            if success:
                st.session_state.messages = result["messages"]

                # 시스템 메시지가 있으면 업데이트
                if "system_message" in result:
                    st.session_state.system_message = result["system_message"]

                st.success("대화 내용을 성공적으로 불러왔습니다.")
                st.rerun()
            else:
                st.error(result)


def render_file_upload_section():
    """파일 업로드 섹션을 렌더링합니다."""
    uploaded_files = st.file_uploader("이미지 파일 업로드 (선택사항, < 5MB)", type=["png", "jpg", "jpeg", "webp", "gif"], accept_multiple_files=True, key="file_upload")
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.uploaded_files:
                # 파일 처리 및 저장
                result, file_info = process_file(uploaded_file)
                if result:
                    st.session_state.uploaded_files[uploaded_file.name] = file_info
                    st.info(f"파일이 업로드되었습니다: {uploaded_file.name} ({file_info['summary']})")
                else:
                    st.error(f"파일 업로드 실패: {uploaded_file.name}, {file_info}")

    # 업로드된 파일 목록 표시
    if st.session_state.uploaded_files:
        st.subheader("업로드된 파일")
        cols = st.columns(3)
        for i, (filename, file_info) in enumerate(st.session_state.uploaded_files.items()):
            col_idx = i % 3
            with cols[col_idx]:
                st.text(f"{filename}: {file_info['summary']}")
                if st.button("삭제", key=f"delete_file_{i}"):
                    del st.session_state.uploaded_files[filename]
                    st.rerun()


def render_chat_history():
    """채팅 기록을 렌더링합니다."""
    from modules.api_client import display_metadata
    metadata_history = st.session_state.get("metadata_history", [])
    assistant_idx = 0
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], str):
                st.write(message["content"])
            elif isinstance(message["content"], list):
                st.write(message["content"][0]["text"])
            # assistant 메시지일 때 metadata 표시
            if message["role"] == "assistant" and assistant_idx < len(metadata_history):
                display_metadata(metadata_history[assistant_idx])
                assistant_idx += 1


def render_cancel_button():
    """응답 생성 취소 버튼을 렌더링합니다."""
    if st.session_state.generating:
        if st.button("응답 생성 취소", key="cancel_button"):
            st.session_state.cancel_generation = True
            st.info("응답 생성을 취소하는 중...")
