# BYUN JAEKYU — 새 공식 홈페이지

이 ZIP의 **내용물 전체**를 GitHub 저장소 `byunjaekyu/byunjaekyu.github.io`의 **최상위(root)**에 업로드합니다. ZIP 파일이나 바깥 폴더 자체를 올리지 마세요.

- `index.html`: 홈페이지 화면 (Works / Texts / About / CV / Contact)
- `works.json`: 작품 데이터 (자동 생성)
- `works/<작품명>/info.md`: 작품 설명과 메타데이터
- `works/<작품명>/*.jpg`: 작품 사진
- `.github/workflows/build-works.yml`: 신작 추가 시 데이터 자동 갱신
- `scripts/build.py`: 작품 정보 빌드 프로그램

## 현재 포함된 작품
- 2025 〈리터칭: 지우기를 위한 드로잉〉: 사진 5장과 설명 포함
- 2018 〈잔해를 위한 哀歌: 녹나무 숲〉: 텍스트·Vimeo 링크만 포함. 이미지 파일이 제공되지 않아 이미지 연결을 비워 둠

**중요:** 기존 홈페이지의 나머지 작품과 CV, 논문 자료는 이 버전에 포함되어 있지 않습니다. `Texts`, `About`, `CV`는 추후 입력을 위한 자리표시자입니다. 기존 자료가 필요하면 먼저 별도로 백업하세요.

## 이미지 규칙
- 대표사진: 80% 너비, 중앙 정렬
- 설치전경: 넓은 너비, 바깥 여백
- 상세사진 한 장: 60% 너비, 중앙 정렬
- 상세사진 여러 장: 2열 배치 (모바일 1열)
- 사진 클릭: 원본 열기

## 새 작품 추가
`works/연도-작품명/` 폴더를 만들고 `info.md`와 사진을 업로드하세요. `info.md`의 `cover`, `images[].file`에 정확한 파일명을 적습니다. 설치전경은 `type: installation`을 사용하세요. GitHub Actions가 `works.json`을 자동으로 생성하도록, 저장소 Settings → Actions → General에서 workflow 쓰기 권한이 필요할 수 있습니다.

## 배포
GitHub 저장소 Settings → Pages에서 `Deploy from a branch`, `main`, `/(root)`로 설정합니다.


## 2025 Retouching editorial layout
The `layout:` sequence in `works/2025-retouching/info.md` controls the order of prose and photos.
The first cover image remains at 80% width. Text blocks, installation photos, paired details, and process images are rendered in the sequence listed.
To update the prose or image placement, edit the `layout:` blocks and commit; GitHub Actions rebuilds `works.json`.
