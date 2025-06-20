"""
Perplexity API 클라이언트 모듈
API 호출 및 응답 처리 관련 기능을 제공합니다.
"""

import json
import httpx
from openai import OpenAI
import streamlit as st


class PerplexityClient:
    """Perplexity API 클라이언트 클래스"""

    def __init__(self, api_key):
        """
        Perplexity API 클라이언트 초기화

        Args:
            api_key (str): Perplexity API 키
        """
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.openai_client = OpenAI(
            api_key=api_key, base_url=self.base_url, http_client=httpx.Client()
        )

    def generate_stream_response(
        self, model, messages, temperature, max_tokens, use_mcp=False, mcp_servers=None
    ):
        """
        스트리밍 방식으로 응답을 생성합니다.

        Args:
            model (str): 사용할 모델 이름
            messages (list): 메시지 목록
            temperature (float): 온도 값
            max_tokens (int): 최대 토큰 수
            use_mcp (bool): MCP 사용 여부
            mcp_servers (list): MCP 서버 목록

        Returns:
            generator: 응답 스트림 제너레이터
        """
        if use_mcp and mcp_servers:
            return self._generate_with_mcp(
                model, messages, temperature, max_tokens, mcp_servers
            )
        else:
            return self._generate_with_openai(model, messages, temperature, max_tokens)

    def _generate_with_openai(self, model, messages, temperature, max_tokens):
        """OpenAI 라이브러리를 사용하여 응답 생성"""
        stream = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        return stream

    def _generate_with_mcp(self, model, messages, temperature, max_tokens, mcp_servers):
        """MCP를 사용하여 직접 API 호출로 응답 생성"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client() as client:
            with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                    "mcp_servers": mcp_servers,
                },
            ) as response:
                # Ensure the response is successful
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        # line is already a string from response.iter_lines()
                        if line.startswith("data: "):
                            line = line[6:]  # 'data: ' 접두사 제거
                            if line != "[DONE]":
                                try:
                                    chunk_data = json.loads(line)
                                    # citations 정보가 있으면 함께 전달
                                    yield chunk_data
                                except json.JSONDecodeError:
                                    # Handle cases where a line might not be valid JSON
                                    # or is an empty data field
                                    pass

    def use_async_api(self, messages, model, temperature, max_tokens):
        """
        비동기 API를 사용하여 응답을 생성하는 함수

        Args:
            messages (list): 메시지 목록
            model (str): 사용할 모델 이름
            temperature (float): 온도 값
            max_tokens (int): 최대 토큰 수

        Returns:
            dict: API 응답
        """
        import time

        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False,
                },
            )

            if response.status_code == 202:
                request_id = response.json().get("id")

                # 요청 상태 확인
                while True:
                    status_response = client.get(
                        f"{self.base_url}/chat/completions/{request_id}",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                    )

                    if status_response.status_code == 200:
                        return status_response.json()

                    time.sleep(1)  # 1초 대기 후 다시 확인

            return response.json()


def process_stream_response(stream, message_placeholder, cancel_flag_getter):
    """
    스트림 응답을 처리하고 UI에 표시합니다.

    Args:
        stream: 응답 스트림
        message_placeholder: 메시지를 표시할 placeholder
        cancel_flag_getter: 취소 플래그를 가져오는 함수

    Returns:
        tuple: (전체 응답 텍스트, 메타데이터)
    """
    full_response = ""
    metadata = {"usage": None, "citations": []}

    # OpenAI 라이브러리 응답인 경우
    if hasattr(stream, "__iter__"):
        for chunk in stream:
            # 취소 플래그 확인
            if cancel_flag_getter():
                break

            if (
                hasattr(chunk, "choices")
                and chunk.choices
                and hasattr(chunk.choices[0], "delta")
            ):
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.write(full_response + "▌")
                    # yield chunk.choices[0].delta.content

            # citations 필드가 있는지 확인
            if hasattr(chunk, "search_results"):
                # metadata["citations"].extend(
                #     [
                #         {"title": citation["title"], "url": citation["url"]}
                #         for citation in chunk.search_results
                #         if citation["url"] not in [c["url"] for c in metadata["citations"]]
                #     ]   # 중복 제거
                # )
                metadata["citations"] = chunk.search_results

            if hasattr(chunk, "usage"):
                metadata["usage"] = chunk.usage

        # if hasattr(stream, "chunk") and stream.chunk:
        #     # 메타데이터 추출
        #     if hasattr(stream.chunk, "usage"):
        #         metadata["usage"] = stream.chunk.usage

        #     # 최종 응답에서 citations 확인
        #     if hasattr(stream.chunk, "search_results"):
        #         metadata["citations"] = stream.chunk.search_results

    # 직접 API 호출 응답인 경우
    else:
        # citations = []
        for chunk in stream:
            if cancel_flag_getter():
                break

            if chunk.get("choices") and chunk["choices"][0].get("delta", {}).get(
                "content"
            ):
                content = chunk["choices"][0]["delta"]["content"]
                full_response += content
                message_placeholder.write(full_response + "▌")
                # yield chunk.choices[0].delta.content

            # citations 필드 확인
            # if chunk.get("search_results"):
                # citations.extend(chunk["search_results"])
                # citations = [
                #         {"title": citation["title"], "url": citation["url"]}
                #         for citation in chunk.search_results
                #         if citation["url"] not in [c["url"] for c in metadata["citations"]]
                #     ]  # 중복 제거
            if "search_results" in chunk:
                metadata["citations"] = chunk["search_results"]

            # 메타데이터 추출
            if "usage" in chunk:
                metadata["usage"] = chunk["usage"]

        # metadata["citations"] = citations

    # 최종 응답 표시
    message_placeholder.write(full_response)

    # 참조 링크 추출 (citations에서 추출하지 못한 경우를 위한 백업)
    if not metadata["citations"]:
        metadata["references"] = extract_references(full_response)
    else:
        metadata["references"] = [
            set(
                citation.get("url")
                for citation in metadata["citations"]
                if citation.get("url")
            )
        ]

    # display_metadata(message_placeholder, metadata)
    return full_response, metadata


def extract_references(text):
    """
    텍스트에서 URL 참조를 추출합니다.

    Args:
        text (str): 추출할 텍스트

    Returns:
        list: 추출된 URL 목록
    """
    import re

    urls = re.findall(
        r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*(?:\?[\w=&]*)?", text
    )
    return [set(urls)] if urls else []  # 중복 제거


def display_metadata(metadata):
    """
    메타데이터를 UI에 표시합니다.

    Args:
        metadata (dict): 표시할 메타데이터
    """
    # 토큰 사용량 표시
    if metadata.get("usage"):
        usage = metadata["usage"]
        with st.expander("응답 메타데이터", expanded=False):
            st.write("**토큰 사용량:**")
            st.write(
                f"- 프롬프트 토큰: {usage.prompt_tokens if hasattr(usage, 'prompt_tokens') else usage.get('prompt_tokens', 'N/A')}"
            )
            st.write(
                f"- 완성 토큰: {usage.completion_tokens if hasattr(usage, 'completion_tokens') else usage.get('completion_tokens', 'N/A')}"
            )
            st.write(
                f"- 총 토큰: {usage.total_tokens if hasattr(usage, 'total_tokens') else usage.get('total_tokens', 'N/A')}"
            )

    # 참조 링크 표시
    references = metadata.get("references", [])
    citations = metadata.get("citations", [])

    if references or citations:
        with st.expander("참조 링크", expanded=True):
            # citations 정보가 있는 경우
            if citations:
                st.write("**인용 정보:**")
                for i, citation in enumerate(citations):
                    title = citation.get("title", "제목 없음")
                    url = citation.get("url", "#")
                    st.write(f"{i+1}. [{title}]({url})")

                    # 추가 정보가 있으면 표시
                    if "text" in citation:
                        with st.expander(f"인용 텍스트 {i+1}", expanded=False):
                            st.write(citation["text"])

            # 텍스트에서 추출한 URL이 있는 경우
            if references and not citations:
                st.write("**참조 링크:**")
                for i, ref in enumerate(references):
                    st.write(f"{i+1}. [{ref}]({ref})")
