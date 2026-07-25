# CLAUDE.md

## 프로젝트 목적

블로그 글 작성을 자동화하는 시스템이다.

나의 블로그 주소: https://blog.naver.com/eomzic_

내 블로그 양식에 맞게 구조화 해야함

## 폴더 구조

- `agents/` — 서브 에이전트 정의 (researcher, writer, image-maker, assembler)
- `guides/` — 스타일/SEO/이미지 가이드 (style-guide.md, seo-guide.md, image-guide.md)
- `output/[주제]/` — 주제별 산출물 (research.md, draft.md, images/, final.md, final.html)

## 메인 에이전트(오케스트레이터) 역할

메인 에이전트는 직접 리서치나 글쓰기를 하지 않는다. 서브 에이전트를 호출해서 작업을 분배하는 오케스트레이터 역할만 한다.

**메인이 직접 글을 쓰거나 리서치하지 말 것 — 반드시 서브 에이전트에게 위임한다.**

## 사용자가 주제를 던졌을 때 따를 단계

1. `agents/researcher.md`를 따라 리서치 → `output/[주제]/research.md` 생성
2. `agents/writer.md`를 따라 글쓰기 → `output/[주제]/draft.md` 생성
3. `agents/image-maker.md`를 따라 이미지 생성 → `draft.md`의 마커를 이미지 경로로 치환
4. `agents/assembler.md`를 따라 통합 → `final.md`, `final.html` 생성

각 단계가 끝날 때마다 사용자에게 진행 상황을 짧게 알린다.
