---
name: assembler
description: image-maker가 이미지 경로까지 치환해둔 draft.md를 받아서 최종 미리보기 파일(final.md, final.html)을 만드는 에이전트.
tools: Read, Write
---

# Assembler 에이전트

image-maker가 이미지 경로까지 다 박아둔 draft.md를 받아서 최종 미리보기 파일을 만드는 역할.

## 입력

- `output/[주제]/draft.md` (image-maker가 이미지 경로까지 치환해둔 상태)
- `output/[주제]/images/` 폴더

## 작동 방식

1. `draft.md`를 읽는다 (이미 마크다운 이미지 문법으로 경로가 박혀있음).
2. 두 가지 형식의 최종 파일을 생성한다.
   - `output/[주제]/final.md` (마크다운 — 검토용)
   - `output/[주제]/final.html` (HTML — 시각 미리보기용)
3. `final.html`은 완전한 HTML 문서로 작성한다 (`<!DOCTYPE html>`, `<html lang="ko">`, `<head><meta charset="UTF-8">...</head>`, `<body>` 필수). `<meta charset="UTF-8">`이 빠지면 브라우저가 인코딩을 잘못 추측해서 한글이 깨진다.
4. 네이버 블로그 본문 영역과 비슷한 스타일링을 적용한다.
   - 본문 폭 700px 정도
   - 한글 가독성 좋은 폰트
   - 폰트 크기는 `writer.md`에 지정된 값을 그대로 사용 (대제목 26px, 소제목 24px, 본문 16px)
   - 이미지는 본문 폭에 맞춰 자동 리사이즈
   - 제목, 소제목, 본문 위계가 명확하게
5. 마지막에 사용자에게 `final.html`을 브라우저로 열어보라고 안내한다.

## 산출물

- `output/[주제]/final.md`
- `output/[주제]/final.html`
