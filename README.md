# 뉴스 크롤링 서비스

이 프로젝트는 다양한 뉴스 사이트에서 뉴스를 크롤링하여 제공하는 API 서비스입니다. 현재는 네이버 뉴스를 지원하며, 향후 다른 뉴스 플랫폼도 추가할 예정입니다.

## 프로젝트 개요

이 서비스는 다양한 뉴스 소스에서 콘텐츠를 수집하고 제공하는 FastAPI 기반 API 서버입니다. 비동기 처리를 통해 빠른 크롤링이 가능하며, 확장 가능한 구조로 설계되어 새로운 뉴스 소스를 쉽게 추가할 수 있습니다.

## 주요 기능

- **비동기 뉴스 크롤링**: 비동기 처리를 통한 효율적인 뉴스 수집
- **네이버 뉴스 지원**: 현재 네이버 뉴스 크롤링 기능 제공
- **API 인터페이스**: REST API를 통한 뉴스 데이터 제공
- **로깅 시스템**: 크롤링 과정 모니터링을 위한 로깅 기능
- **환경 설정 관리**: 개발/프로덕션 환경에 따른 설정 관리
- **B2 스토리지 연동**: 필요시 크롤링 데이터 저장 기능
- **Docker 지원**: 개발 및 배포를 위한 Docker 설정

## 기술 스택

- **Backend**: FastAPI
- **크롤링 라이브러리**: httpx, BeautifulSoup4
- **서버 실행**: Uvicorn
- **패키지 관리**: pip
- **환경 변수 관리**: python-dotenv
- **태스크 실행**: invoke
- **컨테이너화**: Docker
- **코드 포맷팅/린팅**: Ruff, pre-commit

## 프로젝트 구조

```
.
├── app/                    # 애플리케이션 코드
│   ├── config/             # 환경 설정 및 로깅 설정
│   │   ├── env_settings.py # 환경 변수 설정
│   │   ├── exceptions.py   # 예외 처리 설정
│   │   ├── logger.py       # 로깅 설정
│   │   └── redis_client.py # Redis 클라이언트 설정
│   ├── routers/            # API 라우터
│   │   ├── bucket_router.py # B2 저장소 관련 API
│   │   └── naver_news_router.py # 네이버 뉴스 API
│   ├── services/           # 비즈니스 로직
│   │   ├── bucket_service.py # B2 저장소 관련 서비스
│   │   └── naver_news_service.py # 네이버 뉴스 크롤링 서비스
│   ├── __init__.py         # 애플리케이션 초기화
│   └── main.py             # 애플리케이션 진입점
├── public/                 # 정적 파일
├── test/                   # 테스트 코드
├── .dockerignore           # Docker 무시 파일 설정
├── .env                    # 프로덕션 환경 변수
├── .env.dev                # 개발 환경 변수
├── .gitignore              # Git 무시 파일 설정
├── .pre-commit-config.yaml # pre-commit 설정
├── Dockerfile              # Docker 빌드 설정
├── README.md               # 프로젝트 문서
├── pyproject.toml          # Python 프로젝트 설정
├── requirements.txt        # 의존성 패키지 목록
├── start.sh                # 실행 스크립트
└── tasks.py                # Invoke 태스크 정의
```

## 설치 및 실행 방법

### 요구 사항

- Python 3.9 이상
- Docker (선택 사항)

### 로컬 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/your-username/news_crawler.git
cd news_crawler

# 가상 환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 개발 모드 실행
invoke dev
```

### 환경 변수 설정

`.env.dev` 또는 `.env` 파일에 필요한 환경 변수를 설정합니다:

```
# 기본 설정
CURRENT_ENV=development  # development 또는 production
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# B2 스토리지 설정 (선택 사항)
B2_APPLICATION_KEY_ID=your_key_id
B2_APPLICATION_KEY=your_key
B2_BUCKET_NAME=your_bucket_name

# Redis 설정 (선택 사항)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

### Docker로 실행

```bash
# Docker 이미지 빌드
docker build -t news-crawler .

# Docker 컨테이너 실행
docker run -p 8000:8000 --env-file .env news-crawler
```

## 실행 명령어

이 프로젝트는 invoke 라이브러리를 사용하여 주요 명령어를 관리합니다:

- `invoke dev`: 개발 모드 실행 (.env.dev 환경 변수 적용, DEBUG 로깅)
- `invoke start`: 프로덕션 모드 실행 (.env 환경 변수 적용, INFO 로깅)
- `invoke lint`: Ruff 린터로 코드 검사
- `invoke format`: Ruff로 코드 포맷팅
- `invoke test`: pytest로 테스트 실행

## commit 컨벤션(개발자)
- feat : 새 기능 구현
- fix : 에러 수정
- style : 코드 변경이 없는 경우, 코드 포멧팅(es-lint같은 작엄)
- refactor : 코드 리펙토링
- rename : 파일, 폴더명만 수정하거나 이동하는 작업
- test : 테스트 관련 작업
- config : 기타 프로젝트 내 세팅 설정 변경, 텍스트 수정
- infra : 인프라 관련작업( 깃워크플로우, 코드디플로이 등 )

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 주요 API 엔드포인트

- `GET /`: 기본 라우트, 서버 상태 확인
- `GET /api/get-naver-news`: 네이버 뉴스 데이터 조회
- `GET /api/authorize-b2`: B2 스토리지 인증
- `GET /api/get-upload-url-b2`: B2 업로드 URL 획득

## 뉴스 소스 확장하기

새로운 뉴스 소스를 추가하려면 다음 단계를 따르세요:

1. 새로운 크롤링 서비스 생성:
   - `app/services/` 디렉토리에 새 서비스 파일 생성 (예: `daum_news_service.py`)
   - `app/services/__init__.py`에 서비스 함수 추가

2. 새로운 라우터 추가:
   - `app/routers/` 디렉토리에 새 라우터 파일 생성 (예: `daum_news_router.py`)
   - `app/routers/__init__.py`에 라우터 등록
   - `app/__init__.py`에 새 라우터 포함

## 프로젝트 확장

이 프로젝트는 다음과 같은 확장이 가능합니다:

- **추가 뉴스 소스**: 다음, 구글 뉴스, 조선일보 등 다른 뉴스 사이트 지원
- **데이터베이스 연동**: 크롤링한 뉴스 데이터 저장을 위한 DB 연동
- **콘텐츠 분석**: 수집된 뉴스에 대한 텍스트 분석 및 요약 기능
- **정기적 크롤링**: 스케줄링을 통한 자동 크롤링 기능
- **알림 시스템**: 특정 키워드 포함 뉴스 발견 시 알림 기능

## 기여 가이드

1. 이 저장소를 포크하고 기능 브랜치를 생성합니다.
2. 변경 사항을 커밋하고 브랜치에 푸시합니다.
3. 풀 리퀘스트를 생성합니다.

## 라이센스

이 프로젝트는 MIT 라이센스에 따라 배포됩니다.
