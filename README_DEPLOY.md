# kids_room (성남시 동별 인구 & 키즈룸 시각화)

Streamlit 기반으로 성남시 행정동 별 인구(총인구 / 인구밀도)와 키즈룸(키즈카페 등) 위치를 지도 위에 시각화하는 애플리케이션입니다.

## 1. 로컬 실행
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 2. GitHub 업로드
```bash
git init
git add .
git commit -m "init: kids_room app"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/kids_room.git
git push -u origin main
```

## 3. 카카오 API Key 분리 (.streamlit/secrets.toml)
`.streamlit/secrets.toml` 파일을 만들고:
```toml
KAKAO_REST_API_KEY = "your_rest_key"
```
`geocoding.py`에서 `st.secrets["KAKAO_REST_API_KEY"]`로 참조하도록 수정 가능.

## 4. Streamlit Cloud 배포
1. https://streamlit.io → Sign in (Google 계정 가능)
2. New app 선택 → GitHub repo 연결
3. Branch: `main`, File: `app.py`
4. Advanced settings → Secrets 입력:
```toml
KAKAO_REST_API_KEY = "your_rest_key"
```
5. Deploy

## 5. 문제 해결 체크리스트
- KeyError: 'properties' → Folium.Choropleth에 안전한 FeatureCollection 전달 완료
- 인구/인구밀도 토글 → 사이드바 라디오 버튼
- 투명도 조절 → 슬라이더 (`opacity`)
- 키즈룸 데이터 지속성 → `kidsroom_manager.py` (JSON 저장 구현 필요 시 추가)

## 6. 향후 개선 아이디어
- 연령대별 선택 필터 추가
- 혼합 지표(총인구 vs 밀도 가중) 재도입 (안정화 후)
- 키즈룸 DB/Google Sheet 연동
- Mobile UI 최적화

## 7. 라이선스
개인 학습/포트폴리오 용도.

## 8. GitHub Personal Access Token(PAT) 안전하게 저장하고 계속 쓰는 방법
Git push 시 매번 토큰을 입력하지 않도록 **macOS Keychain** 또는 **Git Credential Store**, **GitHub CLI(gh)**를 사용할 수 있습니다.

### 8.1 macOS Keychain (credential-osxkeychain)
Git은 기본적으로 macOS에서 Keychain Helper를 지원합니다.
```bash
# helper 설정 확인
git config --global credential.helper
# 설정되지 않았다면 추가
git config --global credential.helper osxkeychain
```
처음 `git push` 할 때 Username / Password 프롬프트가 뜨면:
- Username: GitHub 사용자명
- Password: 발급받은 PAT (브라우저에서 복사)
입력 후 Keychain에 저장되어 이후 자동 사용됩니다.

### 8.2 GitHub CLI (gh) 사용
브라우저 인증 플로우 제공.
```bash
brew install gh             # 설치 (이미 있다면 생략)
gh auth login               # GitHub.com → HTTPS → Browser 선택
gh auth status              # 인증 확인
git push -u origin main     # 토큰 자동 처리
```
토큰 회전(재발급) 시:
```bash
gh auth refresh -h github.com -s repo
```
로그아웃:
```bash
gh auth logout
```

### 8.3 Git Credential Store (plaintext 주의)
Keychain이 아닌 단순 파일 캐시 방식.
```bash
git config --global credential.helper store
# 최초 push 후 ~/.git-credentials 파일에 저장됨 (암호화 안됨 → 민감하지 않은 환경에서만)
```
`~/.git-credentials` 내용 예시:
```
https://<USERNAME>:<PAT>@github.com
```
민감하면 사용 지양.

### 8.4 환경변수 사용 (CI나 임시 세션)
CI/CD에서만 권장. 로컬에서��� 불편.
```bash
export GITHUB_TOKEN="<PAT>"
# 일부 도구(gh 등)가 자동 감지
```

### 8.5 SSH 키 대안
PAT 대신 SSH 활용:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub   # GitHub Settings → SSH Keys 등록
git remote set-url origin git@github.com:<YOUR_USERNAME>/kids_room.git
git push -u origin main
```
장점: 토큰 만료/회전 관리 불필요.

### 8.6 PAT 관리 모범 사례
| 항목 | 권장 | 비고 |
|------|------|------|
| 노출 | 금지 | README, 코드, 이슈에 붙여넣지 말 것 |
| 범위 | 최소(repo 정도) | 필요 이상 scopes 금지 |
| 만료 | 유효기간 설정 | 너무 긴 무기한 토큰 지양 |
| 회전 | 3~6개월 | 만료 전 새 토큰 발급 후 업데이트 |
| 폐기 | 노출 감지 즉시 revoke | Settings → Developer settings → Tokens |

### 8.7 기존 잘못 저장된 토큰 제거
1. Keychain 열기 → 검색 `github.com` → 관련 항목 삭제
2. `~/.git-credentials` 존재 시 해당 줄 삭제 또는 파일 삭제
3. 다시 push → 새 토큰 입력/저장

### 8.8 Push 재시도 절차 Quick Guide
```bash
git remote -v
# origin 확인 후 문제 있으면 재설정
git remote set-url origin https://github.com/<YOUR_USERNAME>/kids_room.git
# 자격 증명 초기화 (원하는 경우)
git config --global --unset credential.helper
git config --global credential.helper osxkeychain
# 최초 push (프롬프트 → PAT 입력)
git push -u origin main
```

### 8.9 토큰이 동작하지 않을 때 점검
- 401 / 403 → 토큰 scope 부족 또는 만료
- 404 → URL 오타 또는 권한 없음(private repo)
- 422 → 브랜치 보호 규칙(block) 확인
- 프록시/회사 네트워크 → HTTPS 차단 여부 점검

### 8.10 Streamlit Cloud에서 Private Repo 사용
Private인 경우 Streamlit Cloud에서 GitHub OAuth 권한(Repo 읽기) 부여 필요.
- 배포 페이지에서 권한 재설정 (Manage GitHub access)

---
**추천 조합:** 로컬은 `credential.helper osxkeychain` + GitHub CLI(편의성), CI는 GitHub Actions 내 `GITHUB_TOKEN` 사용, 장기 접근은 SSH.
