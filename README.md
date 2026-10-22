# BYUN JAEKYU — 공식 홈페이지

- 홈페이지: https://byunjaekyu.github.io/
- GitHub 저장소: https://github.com/byunjaekyu/byunjaekyu.github.io
- 메뉴: Works / Texts / About / CV / Contact
- 호스팅: GitHub Pages

이 저장소는 작품별 `info.md`를 읽어 `works.json`을 자동 생성하는 예술가 포트폴리오 홈페이지입니다.
작품 내용 수정과 홈페이지 전체 디자인 수정을 구분해 관리합니다.

## 1. 파일 구조

```text
byunjaekyu.github.io/
├── index.html                    # 전체 홈페이지 디자인과 화면 표시
├── works.json                    # 자동 생성되는 작품 데이터 — 직접 편집하지 않음
├── texts.json                    # Texts(논문·비평문) 목록
├── works/
│   └── 작품폴더/
│       ├── info.md               # 작품별 제목·설명·사진·순서·크기·캡션
│       └── 사진파일.jpg
├── scripts/
│   └── build.py                  # info.md → works.json 생성
└── .github/workflows/
    └── build-works.yml           # 작품 데이터 자동 갱신
```

검색엔진 인증용 HTML 파일은 유지합니다. 해당 파일은 삭제하거나 이름을 바꾸지 않습니다.

## 2. 작품 하나 수정하기

1. GitHub에서 `works/해당-작품폴더/info.md`를 엽니다.
2. 제목, 설명, 이미지 파일명, 순서, 크기 또는 캡션을 수정합니다.
3. **Commit changes**를 누릅니다.
4. GitHub **Actions → Build artwork data**에서 초록색 체크를 확인합니다.
5. 홈페이지를 새로고침합니다. 반영이 보이지 않으면 `Ctrl + Shift + R`을 누릅니다.

일반적인 작품 수정에는 `index.html`을 변경하지 않습니다.

## 3. 새 작품 추가하기

`works/연도-작품명/` 폴더에 `info.md`와 사진 파일을 함께 올립니다.
최소한 `title`과 `year`가 있어야 합니다. `build.py`가 `works.json`에 새 작품을 등록합니다.

사진 파일명은 대소문자까지 실제 파일명과 일치해야 합니다.

## 4. info.md 기본 형식

다음은 참고 예시입니다. 기존 작품의 제목·내용·파일명을 이 예시로 바꾸지 마세요.

```yaml
---
title: '작품 제목'
year: 2024
medium: '재료 및 기법'
cover: main.jpg
cover_width: 80%
images:
- file: main.jpg
  type: hero
  caption: '대표이미지 캡션'
- file: installation01.jpg
  type: installation
  caption: '설치전경'
layout:
- type: text
  paragraphs:
  - '작품설명 문단입니다.'
- type: image
  file: installation01.jpg
  width: 85%
  align: center
---

작품설명 원문은 필요에 따라 이 아래에도 기록할 수 있지만,
현재 홈페이지에서는 layout의 text 블록이 우선 표시됩니다.
중복 수정과 불일치를 피하려면 표시용 설명은 layout에서 관리하세요.
```

- `cover`: 대표 이미지. Vimeo가 지정된 경우 영상이 대표 영역에 표시될 수 있습니다.
- `cover_width`: 대표 이미지 너비(예: `80%`).
- `images[].caption`: 해당 사진의 캡션.
- `layout`: 이미지와 글의 실제 표시 순서.
- `layout[].width`: 개별 이미지 너비(10~100% 범위).
- `layout[].align`: `left`, `center`, `right`.
- `type: image-pair`: 사진 2장을 한 행에 배치하며, 좁은 화면에서는 한 열로 변경됩니다.
- 사진 캡션은 공통 CSS에 의해 이미지 아래 오른쪽 정렬입니다.

**중요:** `layout`에 지정된 이미지와 설명이 웹페이지에 우선 표시됩니다.
파일 하단의 Markdown 설명을 바꿨는데 화면이 그대로라면 `layout`의 `paragraphs`부터 확인하세요.

## 5. 자동화 및 배포

사용 중인 작품 데이터 자동화는 `.github/workflows/build-works.yml` 하나입니다.

- 변경 대상: `works/**`, `scripts/build.py`, 자동화 파일 자체.
- 동작: Python + PyYAML로 `scripts/build.py` 실행 후 `works.json`을 갱신합니다.
- `works.json`은 자동 생성 파일이므로 수동 편집하지 않습니다.
- GitHub Pages의 배포 작업은 GitHub에서 별도로 진행될 수 있습니다.
- 과거 실패한 Actions 실행 기록이나 알림 메일 자체는 현재 파일의 오류를 의미하지 않습니다.

`README.md`, `texts.json`, `index.html`만 수정하는 경우에는 작품 데이터 재생성 작업이 필요하지 않습니다.

## 6. 문제가 생겼을 때

| 증상 | 먼저 확인할 것 |
|---|---|
| 수정한 작품이 반영되지 않음 | `info.md` 저장 여부, **Build artwork data** 성공 여부, 강력 새로고침 |
| 작품 사진이 안 나옴 | `info.md`의 파일명과 실제 업로드된 이미지 경로 |
| 작품설명이 변경되지 않음 | `layout`의 `type: text`와 `paragraphs` |
| 이미지 크기가 다름 | `layout`의 `width`, `images`의 `width`, 대표 이미지의 `cover_width` |
| 자동화 실패 | Actions → 실패한 실행 → 실패 단계의 로그 |
| Texts 내용을 바꾸고 싶음 | `texts.json` |
| 전체 메뉴·디자인·캡션 공통 스타일 변경 | `index.html` |

## 7. 관리 원칙

1. 요청한 작품의 `info.md`만 수정하고, 다른 작품·이미지·영상은 변경하지 않습니다.
2. 전체 디자인 변경이 있을 때만 `index.html`을 수정합니다.
3. 파일 이름과 이미지 경로를 임의로 바꾸지 않습니다.
4. 작품 설명, 사진 순서, 캡션, 전시 기록은 기존 내용을 보존합니다.
5. 수정 파일은 업로드 전에 변경 범위를 확인합니다.
