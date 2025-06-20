# Perplexity Sonar AI 챗봇

Perplexity Sonar API를 활용한 스트리밍 방식의 AI 챗봇 애플리케이션입니다. Streamlit 프레임워크로 개발되었으며, 모듈화된 구조로 사용자 친화적인 인터페이스를 제공합니다.

## 주요 기능

### 🤖 AI 챗봇 기능
- Perplexity Sonar 모델을 활용한 실시간 AI 대화
- 스트리밍 방식의 응답 표시로 빠른 사용자 경험
- 응답 생성 중 취소 기능 지원

### ⚙️ 모델 설정 및 커스터마이징
- 5가지 Perplexity Sonar 모델 선택 가능
- Temperature 조절 (0.0~1.0, 창의성 조절)
- 최대 토큰 수 설정 (100~4000)
- 시스템 메시지 커스터마이징으로 AI 역할 정의

### 📁 파일 처리 기능
- **이미지 파일**: PNG, JPG, JPEG, WebP, GIF 지원 (5MB 미만)
- **텍스트 파일**: 일반 텍스트 파일 처리
- **JSON 파일**: JSON 데이터 구조 분석
- 멀티파일 업로드 지원
- 업로드된 파일 관리 (삭제 기능)

### 💾 대화 관리
- 대화 내용 JSON 형식으로 저장
- 저장된 대화 불러오기 기능
- 대화 기록 초기화
- 타임스탬프 포함 자동 파일명 생성

### 📊 메타데이터 및 참조 정보
- 토큰 사용량 상세 정보 (프롬프트/완성/총 토큰)
- Perplexity API 공식 인용 정보 표시
- 참조 링크 자동 추출 및 표시
- 인용 텍스트 확장 보기 기능

## 지원 모델

현재 다음 Perplexity Sonar 모델을 지원합니다:
- **sonar-deep-research**: 심층 연구용 모델 (128k 컨텍스트)
- **sonar-reasoning-pro**: 고급 추론 모델 (128k 컨텍스트)
- **sonar-reasoning**: 기본 추론 모델 (128k 컨텍스트)
- **sonar-pro**: 프로페셔널 모델 (200k 컨텍스트)
- **sonar**: 기본 모델 (128k 컨텍스트) - 기본값

## 프로젝트 구조

```
perplexity-chatbot/
├── perplexity_chat_app.py      # 메인 애플리케이션 파일
├── mcp_utils.py               # MCP 서버 유틸리티 함수
├── modules/                    # 모듈화된 기능들
│   ├── __init__.py
│   ├── api_client.py          # Perplexity API 클라이언트
│   ├── file_processor.py      # 파일 처리 기능
│   └── ui_components.py       # UI 컴포넌트
├── requirements.txt           # 의존성 패키지 목록
├── .env.example              # 환경 변수 예시 파일
├── .env                      # 환경 변수 파일 (실제 API 키)
└── README.md                 # 프로젝트 문서
```

### 모듈 설명

#### `perplexity_chat_app.py`
- 메인 애플리케이션 파일
- Streamlit 앱의 진입점
- 전체 애플리케이션 플로우 관리

#### `mcp_utils.py`
- MCP 서버 관련 유틸리티 함수
- 서버 유효성 검증 및 정보 조회
- 도구 목록 조회 및 호출 기능

#### `api_client.py`
- `PerplexityClient`: Perplexity API와의 통신을 담당하는 클래스
- 스트리밍 응답 처리 및 메타데이터 추출
- OpenAI 라이브러리와 직접 HTTP 호출 방식 지원
- 인용 정보 및 참조 링크 추출 기능

#### `file_processor.py`
- 다양한 파일 형식 처리 (텍스트, 이미지, JSON)
- 파일 첨부 메시지 생성
- 대화 저장/불러오기 기능
- Base64 인코딩을 통한 이미지 처리

#### `ui_components.py`
- Streamlit UI 컴포넌트 관리
- 사이드바 설정 패널
- 파일 업로드 인터페이스
- 채팅 기록 렌더링
- 세션 상태 관리

## 설치 방법

1. **저장소 클론**:
   ```bash
   git clone <repository-url>
   cd perplexity-chatbot
   ```

2. **가상환경 생성 및 활성화** (권장):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # 또는
   .venv\Scripts\activate     # Windows
   ```

3. **필요한 패키지 설치**:
   ```bash
   pip install -r requirements.txt
   ```

4. **API 키 설정**:
   ```bash
   cp .env.example .env
   ```
   그리고 `.env` 파일을 열어 `PERPLEXITY_API_KEY` 값을 실제 API 키로 변경하세요.

5. **애플리케이션 실행**:
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
**참고**: 현재 버전에서는 MCP 기능이 주석 처리되어 있습니다. MCP 기능을 사용하려면 코드의 주석을 해제해야 합니다.

1. 사이드바의 "MCP 서버 설정" 섹션에서 "MCP 기능 활성화" 체크박스를 선택합니다
2. "MCP 서버 URL" 입력란에 서버 URL을 입력합니다
3. "MCP 서버 추가" 버튼을 클릭합니다
4. 추가된 서버는 목록에 표시되며, 필요시 삭제 가능합니다

**참고**: MCP 기능은 OpenAI 라이브러리와 호환성 문제가 있을 수 있습니다. MCP 기능을 활성화하면 httpx 라이브러리를 사용하여 API를 직접 호출하는 방식으로 전환됩니다.

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
1. "이미지 파일 업로드" 영역에 파일을 드래그 앤 드롭하거나 클릭하여 선택
2. 지원되는 파일 형식:
   - **이미지**: PNG, JPG, JPEG, WebP, GIF (5MB 미만)
   - **텍스트**: 일반 텍스트 파일
   - **JSON**: JSON 데이터 파일
3. 업로드된 파일은 목록에 표시되며, 필요시 삭제 가능
4. 메시지 입력 시 업로드된 파일 내용이 함께 AI에 전달됩니다

## 기술적 특징

### API 클라이언트 구조
- **OpenAI 라이브러리 방식**: 기본적으로 OpenAI 호환 라이브러리를 사용하여 Perplexity API 호출
- **직접 HTTP 호출 방식**: MCP 기능 사용 시 httpx를 통한 직접 API 호출
- **스트리밍 응답 처리**: 실시간으로 응답을 받아 UI에 표시
- **메타데이터 추출**: 토큰 사용량, 인용 정보, 참조 링크 자동 추출

### 파일 처리 시스템
- **이미지 파일**: Base64 인코딩을 통한 이미지 데이터 전송
- **텍스트 파일**: UTF-8 디코딩 및 내용 추출
- **JSON 파일**: JSON 파싱 및 구조화된 데이터 처리
- **오류 처리**: 파일 형식 검증 및 처리 오류 핸들링

### 세션 상태 관리
- **대화 기록**: 메시지 히스토리 유지
- **파일 상태**: 업로드된 파일 정보 관리
- **생성 상태**: 응답 생성 및 취소 상태 추적
- **메타데이터**: 각 응답의 메타데이터 히스토리 보관

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
- Streamlit 1.46.0
- OpenAI Python 라이브러리 1.10.0
- httpx 0.24.1
- python-dotenv 1.0.0
- pandas 2.2.0+
- openpyxl 3.1.2
- Perplexity API 키 (https://www.perplexity.ai/ 에서 발급 가능)

### 주요 의존성 패키지
```
streamlit==1.46.0
python-dotenv==1.0.0
openai==1.10.0
httpx==0.24.1
pandas>=2.2.0
openpyxl==3.1.2
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
