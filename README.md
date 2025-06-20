# Perplexity Sonar AI 챗봇

Perplexity Sonar API를 활용한 스트리밍 방식의 AI 챗봇 애플리케이션입니다. Streamlit 프레임워크로 개발되었으며, 사용자 친화적인 인터페이스를 제공합니다.

## 기능

- Perplexity Sonar 모델을 활용한 AI 챗봇
- 실시간 스트리밍 응답 표시
- 다양한 모델 파라미터 조정 가능
  - Temperature
  - 최대 토큰 수
- 시스템 메시지 설정 기능
- MCP(Model Context Protocol) 서버 지원
- 대화 기록 유지 및 초기화 기능
- 대화 내용 저장 및 불러오기 기능
- 응답 생성 중 취소 기능
- 파일 업로드 및 처리 기능
  - 텍스트 파일
  - 이미지 파일
  - PDF 파일
  - Excel 파일
  - JSON 파일

## 지원 모델

현재 다음 Perplexity Sonar 모델을 지원합니다:
- sonar-deep-research (128k 컨텍스트)
- sonar-reasoning-pro (128k 컨텍스트)
- sonar-reasoning (128k 컨텍스트)
- sonar-pro (200k 컨텍스트)
- sonar (128k 컨텍스트)

## 설치 방법

1. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

2. API 키 설정:
   ```bash
   cp .env.example .env
   ```
   그리고 `.env` 파일을 열어 `PERPLEXITY_API_KEY` 값을 실제 API 키로 변경하세요.

3. 애플리케이션 실행:
   ```bash
   streamlit run perplexity_chat_app.py
   ```

## 사용 방법

### 기본 사용법
1. 브라우저에서 Streamlit 앱이 실행됩니다 (기본 URL: http://localhost:8501)
2. 채팅 입력창에 메시지를 입력하고 엔터를 누르면 AI가 응답합니다
3. AI의 응답은 실시간으로 스트리밍되어 표시됩니다

### 설정 옵션
사이드바에서 다음 설정을 조정할 수 있습니다:
- **모델 선택**: 다양한 Perplexity Sonar 모델 중 선택
- **Temperature**: 응답의 창의성 조절 (0.0~1.0)
- **최대 토큰 수**: 응답의 최대 길이 설정
- **시스템 메시지**: AI의 역할과 행동을 정의하는 메시지 설정

### MCP 서버 사용
1. 사이드바의 "MCP 서버 설정" 섹션에서 "MCP 기능 활성화" 체크박스를 선택합니다
2. "MCP 서버 URL" 입력란에 서버 URL을 입력합니다
3. "MCP 서버 추가" 버튼을 클릭합니다
4. 추가된 서버는 목록에 표시되며, 필요시 삭제 가능합니다

**참고**: MCP 기능은 OpenAI 라이브러리와 호환성 문제가 있을 수 있습니다. MCP 기능을 활성화하면 requests 라이브러리를 사용하여 API를 직접 호출하는 방식으로 전환됩니다.

### 대화 저장 및 불러오기
1. 사이드바의 "대화 관리" 섹션에서 저장할 파일명을 입력하고 "대화 저장" 버튼을 클릭
2. 저장된 대화 파일(.json)을 "대화 파일 불러오기" 영역에 업로드하고 "불러오기" 버튼을 클릭

### 응답 생성 취소
1. AI가 응답을 생성하는 동안 "응답 생성 취소" 버튼이 표시됩니다
2. 버튼을 클릭하면 현재 생성 중인 응답이 중단됩니다

### 응답 메타데이터 및 참조 링크
1. AI 응답이 생성된 후 "응답 메타데이터" 확장 패널에서 토큰 사용량 정보를 확인할 수 있습니다
2. "참조 링크" 확장 패널에서 다음 정보를 확인할 수 있습니다:
   - Perplexity API가 제공하는 공식 인용 정보 (제목, URL, 인용 텍스트)
   - 응답 텍스트에서 추출된 URL 링크 (공식 인용 정보가 없는 경우)
3. 인용 텍스트를 확장하여 더 자세한 정보를 볼 수 있습니다
4. 이 정보는 응답의 품질과 신뢰성을 평가하는 데 도움이 됩니다

### 파일 업로드 및 처리
1. "파일 업로드" 영역에 파일을 드래그 앤 드롭하거나 클릭하여 선택
2. 업로드된 파일은 목록에 표시되며, 필요시 삭제 가능
3. 메시지 입력 시 업로드된 파일 내용이 함께 AI에 전달됩니다

## MCP(Model Context Protocol) 지원

이 애플리케이션은 MCP 서버를 통해 AI의 기능을 확장할 수 있습니다. MCP는 AI 모델에 추가적인 컨텍스트와 도구를 제공하는 프로토콜입니다.

MCP 서버 구현에 대한 자세한 정보는 다음 링크를 참조하세요:
- [Perplexity MCP 서버 가이드](https://docs.perplexity.ai/guides/mcp-server)

## API 참조

이 프로젝트는 다음 Perplexity API를 활용합니다:
- [Chat Completions API](https://docs.perplexity.ai/api-reference/chat-completions-post)
- [Async Chat Completions API](https://docs.perplexity.ai/api-reference/async-chat-completions-post)

## 요구사항

- Python 3.7+
- Streamlit
- OpenAI Python 라이브러리
- Pandas (파일 처리용)
- Perplexity API 키 (https://www.perplexity.ai/ 에서 발급 가능)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
