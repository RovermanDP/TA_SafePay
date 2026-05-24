# -*- coding: utf-8 -*-
"""SafePay 요구사항 정의서 PDF 생성 스크립트"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)

# 한글 폰트 등록
pdfmetrics.registerFont(TTFont("Malgun", "C:/Windows/Fonts/malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", "C:/Windows/Fonts/malgunbd.ttf"))

OUTPUT_PATH = r"C:/Users/bagje/Desktop/SafePay_요구사항정의서.pdf"

# ---------------- 스타일 정의 ----------------
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "title", parent=styles["Title"], fontName="MalgunBold",
    fontSize=22, leading=28, alignment=TA_CENTER, spaceAfter=18,
)
style_cover_sub = ParagraphStyle(
    "cover_sub", parent=styles["Normal"], fontName="Malgun",
    fontSize=13, leading=20, alignment=TA_CENTER, spaceAfter=8,
)
style_h1 = ParagraphStyle(
    "h1", parent=styles["Heading1"], fontName="MalgunBold",
    fontSize=18, leading=24, spaceBefore=14, spaceAfter=10, textColor=colors.HexColor("#1a3a6c"),
)
style_h2 = ParagraphStyle(
    "h2", parent=styles["Heading2"], fontName="MalgunBold",
    fontSize=14, leading=20, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#2c5282"),
)
style_h3 = ParagraphStyle(
    "h3", parent=styles["Heading3"], fontName="MalgunBold",
    fontSize=12, leading=18, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#2d3748"),
)
style_body = ParagraphStyle(
    "body", parent=styles["Normal"], fontName="Malgun",
    fontSize=10.5, leading=17, spaceAfter=6, alignment=TA_LEFT,
)
style_bullet = ParagraphStyle(
    "bullet", parent=style_body, leftIndent=14, bulletIndent=4,
)
style_toc = ParagraphStyle(
    "toc", parent=styles["Normal"], fontName="Malgun",
    fontSize=11, leading=22,
)
style_toc_sub = ParagraphStyle(
    "toc_sub", parent=style_toc, leftIndent=18, fontSize=10.5,
)

# ---------------- 셀 텍스트 줄바꿈 스타일 ----------------
style_cell = ParagraphStyle(
    "cell", fontName="Malgun", fontSize=9.5, leading=13, alignment=TA_LEFT,
)
style_cell_center = ParagraphStyle(
    "cell_center", fontName="Malgun", fontSize=9.5, leading=13, alignment=TA_CENTER,
)
style_cell_header = ParagraphStyle(
    "cell_header", fontName="MalgunBold", fontSize=9.5, leading=13,
    alignment=TA_CENTER, textColor=colors.white,
)

def wrap_rows(rows, center_cols=None):
    """첫 행은 헤더 스타일, 나머지 행은 본문 스타일로 Paragraph 변환."""
    if center_cols is None:
        center_cols = set()
    out = []
    for r_i, row in enumerate(rows):
        new_row = []
        for c_i, cell in enumerate(row):
            text = str(cell)
            if r_i == 0:
                new_row.append(Paragraph(text, style_cell_header))
            else:
                st = style_cell_center if c_i in center_cols else style_cell
                new_row.append(Paragraph(text, st))
        out.append(new_row)
    return out

# ---------------- 표 스타일 ----------------
def make_table_style(header_bg="#2c5282"):
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "MalgunBold"),
        ("FONTNAME", (0, 1), (-1, -1), "Malgun"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ])

# ---------------- 헤더/푸터 ----------------
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Malgun", 9)
    canvas.setFillColor(colors.HexColor("#4a5568"))
    canvas.drawString(2 * cm, A4[1] - 1.2 * cm, "SafePay - 온라인 쇼핑 사기 탐지 시스템")
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.2 * cm, "요구사항 정의서")
    canvas.setStrokeColor(colors.HexColor("#cbd5e0"))
    canvas.line(2 * cm, A4[1] - 1.4 * cm, A4[0] - 2 * cm, A4[1] - 1.4 * cm)
    canvas.drawCentredString(A4[0] / 2.0, 1.2 * cm, f"- {doc.page} -")
    canvas.restoreState()

# ---------------- 본문 생성 ----------------
def p(text, style=style_body):
    return Paragraph(text, style)

story = []

# ===== 표지 =====
story.append(Spacer(1, 4 * cm))
story.append(p("요 구 사 항 정 의 서", style_title))
story.append(Spacer(1, 1 * cm))
story.append(p("SafePay", style_cover_sub))
story.append(p("온라인 쇼핑 사기 탐지 시스템", style_cover_sub))
story.append(Spacer(1, 5 * cm))

cover_table = Table(
    [
        ["프로젝트명", "SafePay - 온라인 쇼핑 사기 탐지 시스템"],
        ["문서 버전", "v1.0"],
        ["작성일", "2026-05-18"],
        ["작성자", "박정호(2021125025)"],
        ["문서 상태", "초안"],
    ],
    colWidths=[4 * cm, 10 * cm],
)
cover_table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "Malgun"),
    ("FONTNAME", (0, 0), (0, -1), "MalgunBold"),
    ("FONTSIZE", (0, 0), (-1, -1), 11),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf2f7")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(cover_table)
story.append(PageBreak())

# ===== 목차 =====
story.append(p("목 차", style_title))
story.append(Spacer(1, 0.5 * cm))
toc_items = [
    ("1. 서론", style_toc),
    ("1.1 문서의 목적 및 범위", style_toc_sub),
    ("1.2 대상 시스템 개요", style_toc_sub),
    ("1.3 용어 정의", style_toc_sub),
    ("1.4 참조 문서", style_toc_sub),
    ("2. 요구사항 정의", style_toc),
    ("2.1 기능적 요구사항", style_toc_sub),
    ("2.2 비기능적 요구사항", style_toc_sub),
    ("2.3 인터페이스 요구사항", style_toc_sub),
    ("3. 기타 요구사항", style_toc),
    ("3.1 운영 정책", style_toc_sub),
    ("3.2 제약사항", style_toc_sub),
    ("3.3 향후 확장사항", style_toc_sub),
    ("3.4 특이사항", style_toc_sub),
    ("4. 참고문헌 및 부록", style_toc),
    ("4.1 참고 자료", style_toc_sub),
    ("4.2 부록 A. 위험 점수 계산 규칙", style_toc_sub),
    ("4.3 부록 B. 데이터 모델", style_toc_sub),
    ("4.4 부록 C. 변경 이력", style_toc_sub),
]
for text, st in toc_items:
    story.append(p(text, st))
story.append(PageBreak())

# ===== 1. 서론 =====
story.append(p("1. 서 론", style_h1))

story.append(p("1.1 문서의 목적 및 범위", style_h2))
story.append(p(
    "본 문서는 온라인 쇼핑 환경에서 발생하는 결제 사기를 실시간으로 탐지하고 차단하기 위한 "
    "SafePay 시스템 개발 프로젝트의 요구사항을 정의하는 것을 목적으로 한다. 본 문서는 "
    "이해관계자(개발자, 운영자, 관리자) 간의 합의된 기준을 제공하며, 시스템이 만족해야 할 "
    "기능적·비기능적·인터페이스 요구사항을 명확히 기술한다."
))
story.append(p(
    "범위는 거래 데이터 수집 API, 위험 점수 산출 엔진, 사기 탐지 분류 로직, 관리자 대시보드 "
    "화면을 포함하며, 외부 결제 게이트웨이(PG) 연동 및 모바일 앱 개발은 본 문서의 범위에서 제외한다."
))

story.append(p("1.2 대상 시스템 개요", style_h2))
story.append(p("1.2.1 시스템 정의", style_h3))
story.append(p(
    "SafePay는 온라인 쇼핑몰에서 발생한 결제 거래를 수집하여 위험 점수를 계산하고, "
    "위험 등급(정상 / 의심 / 위험)에 따라 거래를 자동 승인, 보류 또는 차단하는 사기 탐지 시스템이다. "
    "관리자는 웹 대시보드를 통해 실시간 거래 현황과 의심 거래를 한 화면에서 확인할 수 있다."
))
story.append(p("1.2.2 주요 기능 요약", style_h3))

feature_data = [
    ["ID", "기능명", "설명"],
    ["F01", "거래 데이터 수집", "쇼핑몰로부터 결제 거래 정보를 REST API로 수집"],
    ["F02", "위험 점수 산출", "결제 금액, 결제 수단, 위치 정보를 기반으로 위험 점수 계산"],
    ["F03", "사기 거래 분류", "위험 점수에 따라 거래를 정상 / 의심 / 위험 등급으로 분류"],
    ["F04", "거래 자동 처리", "위험 등급에 따라 승인(approved) / 보류(held) / 차단(blocked)을 자동 결정"],
    ["F05", "거래 목록 조회", "관리자가 수집된 거래 내역을 시간 역순으로 조회"],
    ["F06", "실시간 대시보드", "실시간 거래 / 의심 / 차단 건수를 카드 형태로 시각화"],
    ["F07", "위험 등급 필터", "위험 등급별로 거래 목록을 필터링하여 조회"],
    ["F08", "수동 새로고침", "관리자가 대시보드 데이터를 수동으로 새로고침"],
]
t = Table(wrap_rows(feature_data, center_cols={0}), colWidths=[1.5 * cm, 3.5 * cm, 11 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.4 * cm))

story.append(p("1.3 용어 정의", style_h2))
terms_data = [
    ["용어", "설명"],
    ["거래(Transaction)", "사용자가 온라인 쇼핑몰에서 결제한 단위 행위로, 금액·결제수단·IP·위치 등의 속성을 포함한다."],
    ["위험 점수(Risk Score)", "거래의 사기 가능성을 0~100 범위의 정수로 표현한 값."],
    ["위험 등급(Risk Level)", "위험 점수를 기준으로 분류한 정상(normal) / 의심(suspicious) / 위험(danger) 3단계."],
    ["거래 상태(Status)", "시스템이 위험 등급에 따라 부여하는 처리 결과: 승인(approved) / 보류(held) / 차단(blocked)."],
    ["REST API", "HTTP 프로토콜 기반으로 자원을 URI로 표현하고 표준 메서드(GET/POST 등)로 조작하는 인터페이스 양식."],
    ["대시보드", "관리자에게 거래 현황과 분석 결과를 한 화면에 시각적으로 제공하는 웹 페이지."],
    ["SPA", "Single Page Application. 단일 HTML 문서 위에서 화면 전환이 이루어지는 웹 애플리케이션 구조."],
]
t = Table(wrap_rows(terms_data, center_cols={0}), colWidths=[4 * cm, 12 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.4 * cm))

story.append(p("1.4 참조 문서", style_h2))
ref_data = [
    ["번호", "문서명", "비고"],
    ["[R-01]", "SafePay 시스템 구조 문서 (docs/system-structure.md)", "내부"],
    ["[R-02]", "SafePay README.md", "내부"],
    ["[R-03]", "ISO/IEC/IEEE 29148:2018 - Systems and software engineering – Requirements engineering", "표준"],
    ["[R-04]", "OWASP Top 10 (2021)", "보안 가이드"],
    ["[R-05]", "개인정보 보호법 (법률 제19234호)", "법령"],
]
t = Table(wrap_rows(ref_data, center_cols={0, 2}), colWidths=[2 * cm, 10 * cm, 4 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(PageBreak())

# ===== 2. 요구사항 정의 =====
story.append(p("2. 요구사항 정의", style_h1))

# 2.1 기능적 요구사항
story.append(p("2.1 기능적 요구사항", style_h2))

story.append(p("2.1.1 거래 수집 기능", style_h3))
fr1 = [
    ["분류", "요구사항", "우선순위"],
    ["FR-001", "시스템은 외부 쇼핑몰로부터 POST /api/transactions 엔드포인트로 거래 정보를 수신해야 한다.", "상"],
    ["FR-002", "수신한 거래에 대해 시스템은 고유한 식별자(UUID)를 부여해야 한다.", "상"],
    ["FR-003", "수신 요청 본문에는 userId, amount, paymentMethod, ipAddress, location, purchasedAt이 포함되어야 한다.", "상"],
    ["FR-004", "수집된 거래는 시간 역순(최신 우선)으로 내부 저장소에 보관되어야 한다.", "중"],
]
t = Table(wrap_rows(fr1, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.1.2 위험 점수 산출 기능", style_h3))
fr2 = [
    ["분류", "요구사항", "우선순위"],
    ["FR-005", "시스템은 수집된 거래에 대해 기본 점수 10점을 부여해야 한다.", "상"],
    ["FR-006", "결제 금액이 100,000원을 초과하는 경우 35점을 가산해야 한다.", "상"],
    ["FR-007", "결제 수단이 새로 등록된 카드(new-card)인 경우 20점을 가산해야 한다.", "상"],
    ["FR-008", "결제 위치가 unknown인 경우 20점을 가산해야 한다.", "상"],
    ["FR-009", "최종 위험 점수는 0 이상 100 이하의 정수로 산출되어야 한다.", "상"],
]
t = Table(wrap_rows(fr2, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.1.3 사기 거래 분류 기능", style_h3))
fr3 = [
    ["분류", "요구사항", "우선순위"],
    ["FR-010", "위험 점수가 80점 이상이면 위험(danger) 등급으로 분류해야 한다.", "상"],
    ["FR-011", "위험 점수가 50점 이상 80점 미만이면 의심(suspicious) 등급으로 분류해야 한다.", "상"],
    ["FR-012", "위험 점수가 50점 미만이면 정상(normal) 등급으로 분류해야 한다.", "상"],
    ["FR-013", "danger 등급은 자동으로 거래 상태를 차단(blocked)으로 설정해야 한다.", "상"],
    ["FR-014", "suspicious 등급은 자동으로 거래 상태를 보류(held)로 설정해야 한다.", "상"],
    ["FR-015", "normal 등급은 자동으로 거래 상태를 승인(approved)으로 설정해야 한다.", "상"],
]
t = Table(wrap_rows(fr3, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.1.4 거래 조회 기능", style_h3))
fr4 = [
    ["분류", "요구사항", "우선순위"],
    ["FR-016", "관리자는 GET /api/transactions를 통해 전체 거래 목록을 조회할 수 있어야 한다.", "상"],
    ["FR-017", "응답에는 거래 ID, 사용자 ID, 금액, 결제수단, 위치, 시간, 위험 점수, 위험 등급, 상태가 포함되어야 한다.", "상"],
    ["FR-018", "관리자 대시보드는 거래 목록을 표 형태로 표시해야 한다.", "상"],
    ["FR-019", "관리자는 위험 등급(all / normal / suspicious / danger)별로 거래 목록을 필터링할 수 있어야 한다.", "중"],
    ["FR-020", "관리자는 대시보드의 새로고침 버튼을 통해 거래 데이터를 다시 불러올 수 있어야 한다.", "중"],
]
t = Table(wrap_rows(fr4, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.1.5 대시보드 시각화 기능", style_h3))
fr5 = [
    ["분류", "요구사항", "우선순위"],
    ["FR-021", "대시보드는 실시간 거래 / 의심 거래 / 차단 거래 건수를 요약 카드로 표시해야 한다.", "상"],
    ["FR-022", "데이터 로딩 중에는 카드와 표에 로딩 상태를 표시해야 한다.", "중"],
    ["FR-023", "API 요청 실패 시 사용자에게 오류 메시지를 표시해야 한다.", "상"],
    ["FR-024", "위험 등급과 거래 상태는 한글 라벨 및 색상 뱃지로 시각적으로 구분되어야 한다.", "중"],
]
t = Table(wrap_rows(fr5, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

# 2.2 비기능적 요구사항
story.append(p("2.2 비기능적 요구사항", style_h2))

story.append(p("2.2.1 성능 요구사항", style_h3))
nfr1 = [
    ["분류", "요구사항", "우선순위"],
    ["NFR-001", "단일 거래에 대한 위험 점수 산출은 100ms 이내에 완료되어야 한다.", "상"],
    ["NFR-002", "거래 목록 조회 API 응답 시간은 평균 1초 이내여야 한다.", "상"],
    ["NFR-003", "대시보드 초기 로딩 시간은 3초 이내여야 한다.", "중"],
]
t = Table(wrap_rows(nfr1, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.2.2 보안 요구사항", style_h3))
nfr2 = [
    ["분류", "요구사항", "우선순위"],
    ["NFR-004", "거래 데이터에 포함된 IP 주소 및 사용자 ID는 외부로 노출되지 않도록 관리되어야 한다.", "상"],
    ["NFR-005", "API는 향후 HTTPS 기반 통신만 허용하도록 확장 가능해야 한다.", "상"],
    ["NFR-006", "관리자 화면 접근은 추후 인증 절차를 거치도록 확장 가능해야 한다.", "중"],
]
t = Table(wrap_rows(nfr2, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.2.3 신뢰성 및 가용성 요구사항", style_h3))
nfr3 = [
    ["분류", "요구사항", "우선순위"],
    ["NFR-007", "시스템은 잘못된 요청 본문(필수 필드 누락 등)에도 서버가 중단되지 않아야 한다.", "상"],
    ["NFR-008", "서버는 재시작 후 정상적으로 기본 시드 거래 데이터를 로드해야 한다.", "중"],
]
t = Table(wrap_rows(nfr3, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.2.4 유지보수성 요구사항", style_h3))
nfr4 = [
    ["분류", "요구사항", "우선순위"],
    ["NFR-009", "백엔드와 프론트엔드는 분리된 디렉터리 구조(backend/, frontend/)로 관리되어야 한다.", "중"],
    ["NFR-010", "위험 점수 산출 로직은 별도 모듈(risk.service.ts)로 분리되어 확장 가능해야 한다.", "상"],
    ["NFR-011", "TypeScript 타입 정의를 통해 컴파일 타임 오류를 사전에 방지해야 한다.", "중"],
]
t = Table(wrap_rows(nfr4, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.2.5 사용성 요구사항", style_h3))
nfr5 = [
    ["분류", "요구사항", "우선순위"],
    ["NFR-012", "대시보드 UI는 한국어를 기본 언어로 제공해야 한다.", "상"],
    ["NFR-013", "위험 등급은 색상(녹색/주황/빨강 등)으로 직관적으로 구분 가능해야 한다.", "중"],
    ["NFR-014", "데스크톱 해상도(1280×720 이상)에서 정상적으로 표시되어야 한다.", "중"],
]
t = Table(wrap_rows(nfr5, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

# 2.3 인터페이스 요구사항
story.append(p("2.3 인터페이스 요구사항", style_h2))

story.append(p("2.3.1 외부 인터페이스 (REST API)", style_h3))
ifr1 = [
    ["분류", "요구사항", "우선순위"],
    ["IFR-001", "거래 수집 API: POST /api/transactions, Content-Type: application/json", "상"],
    ["IFR-002", "거래 목록 조회 API: GET /api/transactions, 응답 형식 application/json", "상"],
    ["IFR-003", "성공 응답 코드: 거래 수집은 201 Created, 조회는 200 OK를 반환해야 한다.", "상"],
    ["IFR-004", "응답 JSON은 카멜케이스(camelCase) 키 표기를 따라야 한다.", "중"],
]
t = Table(wrap_rows(ifr1, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.3.2 사용자 인터페이스 (UI)", style_h3))
ifr2 = [
    ["분류", "요구사항", "우선순위"],
    ["IFR-005", "관리자 대시보드는 단일 페이지(DashboardPage)에 모든 구성요소를 배치해야 한다.", "상"],
    ["IFR-006", "요약 영역에는 RiskSummaryCard 컴포넌트 3개(실시간/의심/차단)를 표시해야 한다.", "상"],
    ["IFR-007", "거래 목록 영역에는 TransactionTable 컴포넌트와 필터·새로고침 컨트롤을 함께 표시해야 한다.", "상"],
    ["IFR-008", "오류 메시지는 표 상단에 빨간색 강조 텍스트로 표시되어야 한다.", "중"],
]
t = Table(wrap_rows(ifr2, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.3.3 내부 인터페이스 (모듈 간)", style_h3))
ifr3 = [
    ["분류", "요구사항", "우선순위"],
    ["IFR-009", "TransactionController는 TransactionService만을 통해 거래 데이터를 다뤄야 한다.", "상"],
    ["IFR-010", "TransactionService는 FraudDetectionService를 호출하여 거래를 분류해야 한다.", "상"],
    ["IFR-011", "FraudDetectionService는 RiskService를 통해 위험 점수를 산출해야 한다.", "상"],
    ["IFR-012", "프론트엔드는 services/api.ts를 통해서만 백엔드 API를 호출해야 한다.", "상"],
]
t = Table(wrap_rows(ifr3, center_cols={0, 2}), colWidths=[2.2 * cm, 11.3 * cm, 2.0 * cm])
t.setStyle(make_table_style())
story.append(t)

story.append(PageBreak())

# ===== 3. 기타 요구사항 =====
story.append(p("3. 기타 요구사항", style_h1))

story.append(p("3.1 운영 정책", style_h2))
ops = [
    ["분류", "요구사항"],
    ["OP-001", "운영 환경은 Node.js LTS 버전(20.x 이상)을 기준으로 한다."],
    ["OP-002", "백엔드는 Express + TypeScript 기반으로 동작하며 단일 서버 프로세스로 구동된다."],
    ["OP-003", "프론트엔드는 Vite 개발 서버(npm run dev)로 구동되며 빌드 산출물은 정적 호스팅이 가능해야 한다."],
    ["OP-004", "거래 데이터는 현재 메모리 저장소(인메모리 배열)에 보관하며, 서버 재시작 시 시드 데이터로 초기화된다."],
    ["OP-005", "장애 발생 시 콘솔 로그를 통해 1차 원인을 분석하고, 향후 외부 로깅 시스템과 연계할 수 있도록 한다."],
]
t = Table(wrap_rows(ops, center_cols={0}), colWidths=[2.5 * cm, 13 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("3.2 제약사항", style_h2))
cons = [
    ["분류", "요구사항"],
    ["CT-001", "본 프로젝트는 학습/시연 목적의 골격 프로젝트로, 영구 저장소(DB)는 본 단계의 범위에서 제외한다."],
    ["CT-002", "외부 결제 게이트웨이(PG, 카드사) 직접 연동은 본 문서의 범위에 포함되지 않는다."],
    ["CT-003", "사용자 인증(로그인) 및 권한 관리는 본 버전에서 구현하지 않는다."],
    ["CT-004", "위험 점수 산출 로직은 규칙 기반(rule-based)으로 구현하며, 머신러닝 모델 학습은 향후 과제로 분류한다."],
    ["CT-005", "모든 텍스트 응답은 UTF-8 인코딩을 기준으로 한다."],
]
t = Table(wrap_rows(cons, center_cols={0}), colWidths=[2.5 * cm, 13 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("3.3 향후 확장사항", style_h2))
ext = [
    ["분류", "요구사항"],
    ["EX-001", "영구 저장소(PostgreSQL 등) 도입 및 거래 이력 장기 보관."],
    ["EX-002", "관리자 로그인 / 권한 관리(RBAC) 기능 추가."],
    ["EX-003", "사기 탐지 규칙을 머신러닝 기반 모델(예: XGBoost, Isolation Forest)로 고도화."],
    ["EX-004", "실시간 알림(이메일·SMS·Slack) 채널 연동을 통한 위험 거래 즉시 통보."],
    ["EX-005", "관리자 화면에 거래 추세 그래프, 시간대별 통계 등 분석 기능 추가."],
    ["EX-006", "다국어(영어) 지원 및 반응형 UI 확장."],
]
t = Table(wrap_rows(ext, center_cols={0}), colWidths=[2.5 * cm, 13 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("3.4 특이사항", style_h2))
note_text = (
    "1) 본 시스템의 위험 점수 산출 규칙은 데모 시연 편의를 위해 단순화된 임계값을 사용하며, "
    "실제 운영에서는 데이터 분석을 통해 도출된 가중치로 대체되어야 한다.<br/>"
    "2) 거래 데이터를 메모리에 보관하므로 서버 재시작 시 사용자 입력 거래는 소실되며, 시드 거래만 유지된다.<br/>"
    "3) 거래의 시간 정보(purchasedAt)는 ISO 8601 형식의 UTC 문자열을 표준으로 한다.<br/>"
    "4) 본 문서는 프로젝트의 초기 골격을 기준으로 작성되었으며, 기능 추가 시 본 문서도 동기화하여 갱신해야 한다."
)
story.append(p(note_text))

story.append(PageBreak())

# ===== 4. 참고문헌 및 부록 =====
story.append(p("4. 참고문헌 및 부록", style_h1))

story.append(p("4.1 참고 자료", style_h2))
refs = (
    "[1] IEEE Std 29148-2018, Systems and software engineering — Life cycle processes — Requirements engineering, IEEE, 2018.<br/>"
    "[2] OWASP Foundation, OWASP Top 10 - 2021, https://owasp.org/Top10/<br/>"
    "[3] Mozilla Developer Network, REST API 가이드, https://developer.mozilla.org/<br/>"
    "[4] Express.js 공식 문서, https://expressjs.com/<br/>"
    "[5] React 공식 문서, https://react.dev/<br/>"
    "[6] Vite 공식 문서, https://vitejs.dev/<br/>"
    "[7] TypeScript 공식 핸드북, https://www.typescriptlang.org/docs/<br/>"
    "[8] 개인정보 보호법 (법률 제19234호), 국가법령정보센터, https://www.law.go.kr/"
)
story.append(p(refs))
story.append(Spacer(1, 0.3 * cm))

story.append(p("4.2 부록 A. 위험 점수 계산 규칙", style_h2))
score_rule = [
    ["조건", "가산 점수", "비고"],
    ["기본 점수", "+10", "모든 거래에 부여"],
    ["결제 금액 > 100,000원", "+35", "고액 거래"],
    ["결제 수단 = new-card", "+20", "신규 등록 카드"],
    ["결제 위치 = unknown", "+20", "위치 식별 불가"],
    ["최종 점수 상한", "100", "Math.min(score, 100)"],
]
t = Table(wrap_rows(score_rule, center_cols={0, 2}), colWidths=[6 * cm, 3 * cm, 6.5 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("위험 등급 임계값", style_h3))
level_rule = [
    ["위험 점수 범위", "위험 등급", "거래 상태"],
    ["80점 이상", "danger (위험)", "blocked (차단)"],
    ["50점 이상 ~ 80점 미만", "suspicious (의심)", "held (보류)"],
    ["50점 미만", "normal (정상)", "approved (승인)"],
]
t = Table(wrap_rows(level_rule, center_cols={0, 2}), colWidths=[6 * cm, 4.5 * cm, 5 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("4.3 부록 B. 데이터 모델 (Transaction)", style_h2))
data_model = [
    ["필드명", "타입", "설명"],
    ["id", "string (UUID)", "거래 고유 식별자"],
    ["userId", "string", "결제를 수행한 사용자 ID"],
    ["amount", "number", "결제 금액(원화)"],
    ["paymentMethod", "string", "결제 수단 (card / new-card 등)"],
    ["ipAddress", "string", "결제 발생 IP 주소"],
    ["location", "string", "결제 위치(도시 또는 unknown)"],
    ["purchasedAt", "string (ISO8601)", "결제 발생 일시"],
    ["riskScore", "number (0-100)", "산출된 위험 점수"],
    ["riskLevel", "RiskLevel", "normal / suspicious / danger"],
    ["status", "string", "approved / held / blocked"],
]
t = Table(wrap_rows(data_model, center_cols={0}), colWidths=[3.5 * cm, 4 * cm, 8 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("4.4 부록 C. 변경 이력", style_h2))
history = [
    ["버전", "일자", "작성자", "내용"],
    ["v1.0", "2026-05-18", "박정호", "초안 작성 (전체 요구사항 정의)"],
]
t = Table(wrap_rows(history, center_cols={0, 1, 2}), colWidths=[2 * cm, 3 * cm, 3 * cm, 7.5 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)

# ---------------- PDF 생성 ----------------
doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm,
    title="SafePay 요구사항 정의서",
    author="박정호(2021125025)",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF generated: {OUTPUT_PATH}")
print(f"Size: {os.path.getsize(OUTPUT_PATH)} bytes")
