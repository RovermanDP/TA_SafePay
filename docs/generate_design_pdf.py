# -*- coding: utf-8 -*-
"""SafePay 소프트웨어 설계서 PDF 생성 스크립트"""

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
    PageBreak,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF

pdfmetrics.registerFont(TTFont("Malgun", "C:/Windows/Fonts/malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", "C:/Windows/Fonts/malgunbd.ttf"))

OUTPUT_PATH = r"C:/Users/bagje/Desktop/SafePay_소프트웨어설계서.pdf"

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
style_h4 = ParagraphStyle(
    "h4", parent=styles["Heading4"], fontName="MalgunBold",
    fontSize=11, leading=16, spaceBefore=6, spaceAfter=3, textColor=colors.HexColor("#2d3748"),
)
style_body = ParagraphStyle(
    "body", parent=styles["Normal"], fontName="Malgun",
    fontSize=10.5, leading=17, spaceAfter=6, alignment=TA_LEFT,
)
style_toc = ParagraphStyle(
    "toc", parent=styles["Normal"], fontName="Malgun",
    fontSize=11, leading=22,
)
style_toc_sub = ParagraphStyle(
    "toc_sub", parent=style_toc, leftIndent=18, fontSize=10.5,
)
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


style_spec_label = ParagraphStyle(
    "spec_label", fontName="MalgunBold", fontSize=9.5, leading=14, alignment=TA_CENTER,
)
style_spec_value = ParagraphStyle(
    "spec_value", fontName="Malgun", fontSize=9.5, leading=14, alignment=TA_LEFT,
)


def wrap_spec_rows(rows):
    """라벨/값 형식의 spec 표 (좌측 라벨 회색 배경, 우측 값) 셀을 Paragraph로 감싼다.
    짝수 인덱스 컬럼은 라벨(굵게), 홀수 인덱스 컬럼은 값으로 처리."""
    out = []
    for row in rows:
        new_row = []
        for c_i, cell in enumerate(row):
            text = str(cell)
            st = style_spec_label if c_i % 2 == 0 else style_spec_value
            new_row.append(Paragraph(text, st))
        out.append(new_row)
    return out


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


def make_spec_table_style():
    return TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Malgun"),
        ("FONTNAME", (0, 0), (0, -1), "MalgunBold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf2f7")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ])


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Malgun", 9)
    canvas.setFillColor(colors.HexColor("#4a5568"))
    canvas.drawString(2 * cm, A4[1] - 1.2 * cm, "SafePay - 온라인 쇼핑 사기 탐지 시스템")
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.2 * cm, "소프트웨어 설계서")
    canvas.setStrokeColor(colors.HexColor("#cbd5e0"))
    canvas.line(2 * cm, A4[1] - 1.4 * cm, A4[0] - 2 * cm, A4[1] - 1.4 * cm)
    canvas.drawCentredString(A4[0] / 2.0, 1.2 * cm, f"- {doc.page} -")
    canvas.restoreState()


def p(text, style=style_body):
    return Paragraph(text, style)


# ---------------- 다이어그램 생성 도구 ----------------
def draw_class_box(d, x, y, w, h, title, attrs, ops):
    d.add(Rect(x, y, w, h, fillColor=colors.HexColor("#ebf4ff"),
               strokeColor=colors.HexColor("#2c5282"), strokeWidth=1))
    d.add(Rect(x, y + h - 18, w, 18, fillColor=colors.HexColor("#2c5282"),
               strokeColor=colors.HexColor("#2c5282"), strokeWidth=1))
    d.add(String(x + w / 2, y + h - 13, title, fontName="MalgunBold",
                 fontSize=9, fillColor=colors.white, textAnchor="middle"))
    line_y = y + h - 18
    # 속성
    for i, a in enumerate(attrs):
        d.add(String(x + 4, line_y - 12 - i * 11, a, fontName="Malgun",
                     fontSize=7.5, fillColor=colors.black))
    # 구분선
    sep_y = line_y - 12 - len(attrs) * 11 - 2
    d.add(Line(x, sep_y, x + w, sep_y, strokeColor=colors.HexColor("#2c5282")))
    # 연산
    for i, o in enumerate(ops):
        d.add(String(x + 4, sep_y - 12 - i * 11, o, fontName="Malgun",
                     fontSize=7.5, fillColor=colors.black))


def static_structure_diagram():
    d = Drawing(460, 320)
    # Transaction Package
    d.add(Rect(5, 200, 450, 115, fillColor=colors.HexColor("#fef5e7"),
               strokeColor=colors.HexColor("#d69e2e"), strokeWidth=1, strokeDashArray=[3, 2]))
    d.add(String(15, 305, "Backend Package - Transaction / FraudDetection",
                 fontName="MalgunBold", fontSize=8.5, fillColor=colors.HexColor("#744210")))

    draw_class_box(d, 15, 210, 95, 80, "TransactionController",
                   ["- service: TransactionService"],
                   ["+ collect()", "+ list()"])
    draw_class_box(d, 120, 210, 100, 80, "TransactionService",
                   ["- transactions: Transaction[]"],
                   ["+ collectTransaction()", "+ listTransactions()"])
    draw_class_box(d, 230, 210, 105, 80, "FraudDetectionService",
                   ["- riskService"],
                   ["+ classifyTransaction()"])
    draw_class_box(d, 345, 210, 100, 80, "RiskService",
                   ["- thresholds"],
                   ["+ calculateRiskScore()"])

    # 연결선 (의존)
    d.add(Line(110, 250, 120, 250, strokeColor=colors.HexColor("#2c5282")))
    d.add(Line(220, 250, 230, 250, strokeColor=colors.HexColor("#2c5282")))
    d.add(Line(335, 250, 345, 250, strokeColor=colors.HexColor("#2c5282")))

    # Frontend Package
    d.add(Rect(5, 60, 450, 130, fillColor=colors.HexColor("#e6fffa"),
               strokeColor=colors.HexColor("#2c7a7b"), strokeWidth=1, strokeDashArray=[3, 2]))
    d.add(String(15, 180, "Frontend Package - Dashboard",
                 fontName="MalgunBold", fontSize=8.5, fillColor=colors.HexColor("#234e52")))

    draw_class_box(d, 15, 70, 100, 100, "DashboardPage",
                   ["- transactions", "- loading", "- riskFilter"],
                   ["+ loadTransactions()", "+ render()"])
    draw_class_box(d, 125, 70, 100, 100, "RiskSummaryCard",
                   ["- title", "- value", "- tone"],
                   ["+ render()"])
    draw_class_box(d, 235, 70, 105, 100, "TransactionTable",
                   ["- items", "- riskFilter", "- loading"],
                   ["+ render()", "+ onRefresh()", "+ onFilterChange()"])
    draw_class_box(d, 350, 70, 95, 100, "ApiClient",
                   ["- BASE_URL"],
                   ["+ fetchTransactions()"])
    d.add(Line(115, 120, 125, 120, strokeColor=colors.HexColor("#2c7a7b")))
    d.add(Line(225, 120, 235, 120, strokeColor=colors.HexColor("#2c7a7b")))
    d.add(Line(340, 120, 350, 120, strokeColor=colors.HexColor("#2c7a7b")))

    # Frontend → Backend 화살표 (REST API)
    d.add(Line(395, 70, 395, 50, strokeColor=colors.HexColor("#e53e3e"), strokeWidth=1.2))
    d.add(Polygon([395, 35, 391, 45, 399, 45], fillColor=colors.HexColor("#e53e3e"),
                  strokeColor=colors.HexColor("#e53e3e")))
    d.add(String(310, 40, "HTTP / JSON (REST)", fontName="Malgun",
                 fontSize=8, fillColor=colors.HexColor("#e53e3e")))

    # Backend Inbound
    d.add(Line(62, 200, 62, 50, strokeColor=colors.HexColor("#e53e3e"), strokeWidth=1.2))
    d.add(Polygon([62, 200, 58, 195, 66, 195], fillColor=colors.HexColor("#e53e3e"),
                  strokeColor=colors.HexColor("#e53e3e")))

    # 외부
    d.add(Rect(150, 5, 160, 25, fillColor=colors.HexColor("#fed7d7"),
               strokeColor=colors.HexColor("#c53030"), strokeWidth=1))
    d.add(String(230, 15, "외부 쇼핑몰 / 관리자 브라우저", fontName="Malgun",
                 fontSize=8, fillColor=colors.black, textAnchor="middle"))
    return d


def sequence_diagram_collect():
    d = Drawing(450, 220)
    actors = [("외부 쇼핑몰", 40), ("Controller", 130), ("Service", 220), ("FraudDetection", 310), ("RiskService", 410)]
    for name, x in actors:
        d.add(Rect(x - 35, 195, 70, 18, fillColor=colors.HexColor("#edf2f7"),
                   strokeColor=colors.HexColor("#4a5568")))
        d.add(String(x, 202, name, fontName="MalgunBold", fontSize=8,
                     textAnchor="middle"))
        d.add(Line(x, 195, x, 30, strokeColor=colors.HexColor("#4a5568"),
                   strokeDashArray=[2, 2]))

    msgs = [
        (40, 130, 175, "POST /api/transactions"),
        (130, 220, 155, "collectTransaction(input)"),
        (220, 310, 135, "classifyTransaction(input)"),
        (310, 410, 115, "calculateRiskScore(input)"),
        (410, 310, 95, "score"),
        (310, 220, 75, "Transaction"),
        (220, 130, 55, "Transaction"),
        (130, 40, 35, "201 Created"),
    ]
    for x1, x2, y, label in msgs:
        d.add(Line(x1, y, x2, y, strokeColor=colors.HexColor("#2c5282"), strokeWidth=1))
        if x2 > x1:
            d.add(Polygon([x2, y, x2 - 5, y + 3, x2 - 5, y - 3],
                          fillColor=colors.HexColor("#2c5282"),
                          strokeColor=colors.HexColor("#2c5282")))
        else:
            d.add(Polygon([x2, y, x2 + 5, y + 3, x2 + 5, y - 3],
                          fillColor=colors.HexColor("#2c5282"),
                          strokeColor=colors.HexColor("#2c5282")))
        cx = (x1 + x2) / 2
        d.add(String(cx, y + 3, label, fontName="Malgun", fontSize=7.5,
                     fillColor=colors.black, textAnchor="middle"))
    return d


def sequence_diagram_list():
    d = Drawing(450, 200)
    actors = [("관리자", 40), ("DashboardPage", 140), ("ApiClient", 240), ("Controller", 340), ("Service", 420)]
    for name, x in actors:
        d.add(Rect(x - 35, 175, 75, 18, fillColor=colors.HexColor("#edf2f7"),
                   strokeColor=colors.HexColor("#4a5568")))
        d.add(String(x, 182, name, fontName="MalgunBold", fontSize=8,
                     textAnchor="middle"))
        d.add(Line(x, 175, x, 20, strokeColor=colors.HexColor("#4a5568"),
                   strokeDashArray=[2, 2]))

    msgs = [
        (40, 140, 155, "대시보드 접속 / 새로고침"),
        (140, 240, 135, "fetchTransactions()"),
        (240, 340, 115, "GET /api/transactions"),
        (340, 420, 95, "listTransactions()"),
        (420, 340, 75, "Transaction[]"),
        (340, 240, 55, "200 OK + JSON"),
        (240, 140, 35, "Transaction[]"),
    ]
    for x1, x2, y, label in msgs:
        d.add(Line(x1, y, x2, y, strokeColor=colors.HexColor("#2c5282"), strokeWidth=1))
        if x2 > x1:
            d.add(Polygon([x2, y, x2 - 5, y + 3, x2 - 5, y - 3],
                          fillColor=colors.HexColor("#2c5282"),
                          strokeColor=colors.HexColor("#2c5282")))
        else:
            d.add(Polygon([x2, y, x2 + 5, y + 3, x2 + 5, y - 3],
                          fillColor=colors.HexColor("#2c5282"),
                          strokeColor=colors.HexColor("#2c5282")))
        cx = (x1 + x2) / 2
        d.add(String(cx, y + 3, label, fontName="Malgun", fontSize=7.5,
                     fillColor=colors.black, textAnchor="middle"))
    return d


def ui_mockup_diagram():
    d = Drawing(450, 270)
    # 브라우저 프레임
    d.add(Rect(10, 10, 430, 250, fillColor=colors.HexColor("#f7fafc"),
               strokeColor=colors.HexColor("#cbd5e0")))
    d.add(Rect(10, 240, 430, 20, fillColor=colors.HexColor("#2c5282"),
               strokeColor=colors.HexColor("#2c5282")))
    d.add(String(25, 246, "SafePay Admin - 사기 탐지 대시보드",
                 fontName="MalgunBold", fontSize=10, fillColor=colors.white))

    # 요약 카드 3개
    cards = [
        (25, 200, "#3182ce", "실시간 거래", "12건"),
        (170, 200, "#dd6b20", "의심 거래", "3건"),
        (315, 200, "#e53e3e", "차단 거래", "2건"),
    ]
    for x, y, c, t, v in cards:
        d.add(Rect(x, y - 50, 110, 50, fillColor=colors.HexColor("#ffffff"),
                   strokeColor=colors.HexColor(c), strokeWidth=1.5))
        d.add(String(x + 8, y - 14, t, fontName="Malgun", fontSize=8.5))
        d.add(String(x + 8, y - 38, v, fontName="MalgunBold", fontSize=14,
                     fillColor=colors.HexColor(c)))

    # 필터/새로고침
    d.add(Rect(25, 110, 100, 20, fillColor=colors.white,
               strokeColor=colors.HexColor("#cbd5e0")))
    d.add(String(35, 116, "▼ 전체 등급", fontName="Malgun", fontSize=8.5))
    d.add(Rect(355, 110, 70, 20, fillColor=colors.HexColor("#2c5282")))
    d.add(String(390, 116, "새로고침", fontName="Malgun", fontSize=8.5,
                 fillColor=colors.white, textAnchor="middle"))

    # 표 헤더
    d.add(Rect(25, 80, 400, 22, fillColor=colors.HexColor("#2c5282")))
    cols = ["거래 ID", "사용자", "금액", "결제수단", "점수", "등급", "상태", "시각"]
    xs = [30, 95, 140, 190, 245, 285, 330, 380]
    for x, c in zip(xs, cols):
        d.add(String(x, 88, c, fontName="MalgunBold", fontSize=7.5,
                     fillColor=colors.white))

    # 표 행
    rows_data = [
        ("a1b2...", "user-01", "250,000", "new-card", "85", "위험", "차단"),
        ("c3d4...", "user-02", "15,000", "card", "10", "정상", "승인"),
        ("e5f6...", "user-03", "175,000", "card", "65", "의심", "보류"),
    ]
    for i, row in enumerate(rows_data):
        y = 60 - i * 18
        bg = colors.HexColor("#f7fafc") if i % 2 == 0 else colors.white
        d.add(Rect(25, y, 400, 18, fillColor=bg, strokeColor=colors.HexColor("#e2e8f0")))
        cells = list(row) + ["12:30"]
        for x, val in zip(xs, cells):
            d.add(String(x, y + 7, val, fontName="Malgun", fontSize=7.5))
    return d


story = []

# ===== 표지 =====
story.append(Spacer(1, 4 * cm))
story.append(p("소 프 트 웨 어 설 계 서", style_title))
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
story.append(Spacer(1, 0.4 * cm))
toc_items = [
    ("1. 서론", style_toc),
    ("1.1 문서의 목적 및 범위", style_toc_sub),
    ("1.2 용어 정의", style_toc_sub),
    ("1.3 참조 문서", style_toc_sub),
    ("2. 소프트웨어 아키텍처", style_toc),
    ("2.1 정적 구조", style_toc_sub),
    ("2.2 동적 구조", style_toc_sub),
    ("3. 모듈/패키지 설계", style_toc),
    ("3.1 SDD-P-001 : Transaction 패키지", style_toc_sub),
    ("3.2 SDD-P-002 : FraudDetection 패키지", style_toc_sub),
    ("3.3 SDD-P-003 : Dashboard 패키지", style_toc_sub),
    ("4. 인터페이스 설계", style_toc),
    ("4.1 외부 시스템 인터페이스", style_toc_sub),
    ("4.2 사용자 인터페이스", style_toc_sub),
    ("5. 데이터 설계", style_toc),
    ("6. 구현 기술 설계", style_toc),
    ("7. 요구사항 추적표", style_toc),
    ("8. 부록", style_toc),
]
for text, st in toc_items:
    story.append(p(text, st))
story.append(PageBreak())

# ===== 1. 서론 =====
story.append(p("1. 서 론", style_h1))

story.append(p("1.1 문서의 목적 및 범위", style_h2))
story.append(p(
    "본 문서는 \"SafePay - 온라인 쇼핑 사기 탐지 시스템\" 프로젝트의 소프트웨어 컴포넌트에 대한 "
    "설계 사항을 기록하고 문서화하는 데 있으며, 내용의 범위는 목차를 근간으로 정적/동적 아키텍처, "
    "모듈(패키지) 설계, 인터페이스 설계, 데이터 설계, 구현 기술 설계 및 요구사항 추적표가 포함될 "
    "것인지를 기록한다."
))
story.append(p(
    "본 문서의 범위는 SafePay 시스템의 백엔드(거래 수집, 위험 점수 산출, 사기 거래 분류) 및 "
    "프론트엔드(관리자 대시보드)에 한하며, 외부 결제 게이트웨이 직접 연동 및 모바일 앱은 본 "
    "문서의 설계 대상에서 제외한다."
))

story.append(p("1.2 용어 정의", style_h2))
terms = [
    ["용어", "설명"],
    ["거래(Transaction)", "사용자가 온라인 쇼핑몰에서 결제한 단위 행위로, 금액·결제수단·IP·위치 등의 속성을 포함한다."],
    ["위험 점수(Risk Score)", "거래의 사기 가능성을 0~100 범위의 정수로 표현한 값."],
    ["위험 등급(Risk Level)", "위험 점수를 기준으로 분류한 normal / suspicious / danger 3단계."],
    ["거래 상태(Status)", "위험 등급에 따라 부여되는 처리 결과: approved / held / blocked."],
    ["REST API", "HTTP 프로토콜 기반으로 자원을 URI로 표현하고 표준 메서드(GET/POST 등)로 조작하는 인터페이스 양식."],
    ["SPA", "Single Page Application. 단일 HTML 문서 위에서 화면 전환이 이루어지는 웹 애플리케이션 구조."],
    ["대시보드", "관리자에게 거래 현황과 분석 결과를 한 화면에 시각적으로 제공하는 웹 페이지."],
]
t = Table(wrap_rows(terms, center_cols={0}), colWidths=[4 * cm, 12 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("1.3 참조 문서", style_h2))
refs = [
    ["번호", "문서명", "비고"],
    ["[R-01]", "SafePay 요구사항 정의서 (SafePay_요구사항정의서.pdf)", "내부"],
    ["[R-02]", "SafePay 요구사항 분석서 (SafePay_요구사항분석서.pdf)", "내부"],
    ["[R-03]", "SafePay 시스템 구조 문서 (docs/system-structure.md)", "내부"],
    ["[R-04]", "SafePay README.md", "내부"],
    ["[R-05]", "ISO/IEC/IEEE 42010 - 아키텍처 기술 표준", "표준"],
    ["[R-06]", "OWASP Top 10 (2021)", "보안 가이드"],
]
t = Table(wrap_rows(refs, center_cols={0, 2}), colWidths=[2 * cm, 10 * cm, 4 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(PageBreak())

# ===== 2. 소프트웨어 아키텍처 =====
story.append(p("2. 소프트웨어 아키텍처", style_h1))

story.append(p("2.1 정적 구조", style_h2))
story.append(p(
    "SafePay 시스템은 단일 페이지 애플리케이션(SPA) 구조의 프론트엔드와 REST API를 제공하는 백엔드 서버로 "
    "구성된다. 백엔드는 계층형(Layered) 아키텍처를 따르며 Controller → Service → Model 흐름으로 책임을 분리한다. "
    "프론트엔드는 컴포넌트 기반(React)으로 페이지/컴포넌트/서비스/타입 계층을 분리한다."
))
story.append(static_structure_diagram())
story.append(Spacer(1, 0.2 * cm))

pkg_table = [
    ["패키지명", "기능 설명", "담당자"],
    ["Transaction", "외부 쇼핑몰로부터 거래 데이터를 수신·저장하고, 관리자에게 거래 목록을 제공한다.", "공통"],
    ["FraudDetection", "수집된 거래에 대해 위험 점수를 산출하고 위험 등급(normal/suspicious/danger) 및 거래 상태를 결정한다.", "공통"],
    ["Dashboard", "관리자에게 실시간 거래 현황과 의심 거래 목록을 시각적으로 제공한다.", "공통"],
]
t = Table(wrap_rows(pkg_table, center_cols={0, 2}), colWidths=[3 * cm, 10.5 * cm, 2.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("2.2 동적 구조", style_h2))
story.append(p(
    "동적 구조는 시스템의 주요 시나리오(거래 수집, 거래 목록 조회)에 대해 객체 간 상호작용을 시퀀스 "
    "다이어그램으로 표현한다."
))
story.append(p("2.2.1 거래 수집 시나리오 (POST /api/transactions)", style_h3))
story.append(sequence_diagram_collect())
story.append(Spacer(1, 0.2 * cm))
story.append(p(
    "외부 쇼핑몰이 거래 데이터를 POST 요청으로 전송하면 TransactionController가 요청을 받아 "
    "TransactionService에 위임하고, Service는 FraudDetectionService를 호출해 거래를 분류한 후 "
    "내부 저장소(메모리)에 추가하고 결과를 응답한다."
))

story.append(p("2.2.2 거래 목록 조회 시나리오 (GET /api/transactions)", style_h3))
story.append(sequence_diagram_list())
story.append(Spacer(1, 0.2 * cm))
story.append(p(
    "관리자가 대시보드에 접속하거나 새로고침 버튼을 누르면 DashboardPage가 ApiClient를 통해 "
    "백엔드에 GET 요청을 보낸다. TransactionController는 TransactionService.listTransactions()를 "
    "호출하여 거래 배열을 반환하고, 결과는 JSON으로 응답된다."
))
story.append(PageBreak())

# ===== 3. 모듈/패키지 설계 =====
story.append(p("3. 모듈/패키지 설계", style_h1))

# 3.1 Transaction
story.append(p("3.1 SDD-P-001 : Transaction 패키지", style_h2))
story.append(p("3.1.1 모듈 설명", style_h3))
desc1 = [
    ["패키지 설명", "외부 쇼핑몰로부터 거래 데이터를 수신·저장하고, 관리자에게 거래 목록을 조회·제공하기 위한 패키지"],
    ["구성 클래스 - TransactionController", "HTTP 요청을 받아 적절한 서비스로 위임하는 클래스"],
    ["구성 클래스 - TransactionService", "거래 데이터 저장소(메모리)를 관리하고, 수집·조회 기능을 제공하는 클래스"],
    ["구성 클래스 - Transaction(Model)", "거래 데이터의 형식과 타입을 정의하는 모델"],
]
t = Table(wrap_spec_rows(desc1), colWidths=[4.5 * cm, 11 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("3.1.2 구성 클래스 설계", style_h3))
story.append(p("(1) CM-001 : TransactionController", style_h4))
cm001 = [
    ["클래스 타입", "Concrete", "관련 Use Case", "U_01, U_02"],
]
t = Table(wrap_spec_rows(cm001), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cm001_body = [
    ["설  명", "HTTP 요청을 받아 TransactionService로 위임하고, 적절한 응답 코드와 JSON 본문을 반환한다."],
    ["멤버 변수", "- service: TransactionService (의존성)"],
    ["멤버 함수", "+ collect(req, res)<br/>+ list(req, res)"],
    ["관계성", "Generalization (a-kind-of):<br/>Aggregation (has-parts):<br/>Other Associations: TransactionService"],
]
t = Table(wrap_rows([["항목", "내용"]] + cm001_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("(2) CM-002 : TransactionService", style_h4))
cm002 = [
    ["클래스 타입", "Concrete", "관련 Use Case", "U_01, U_02"],
]
t = Table(wrap_spec_rows(cm002), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cm002_body = [
    ["설  명", "거래 데이터의 메모리 저장소를 관리하고, 거래 수집/조회 기능을 제공한다."],
    ["멤버 변수", "- transactions: Transaction[] (메모리 저장소)<br/>- seedInputs: 초기 시드 데이터"],
    ["멤버 함수", "+ collectTransaction(input)<br/>+ listTransactions()"],
    ["관계성", "Generalization (a-kind-of):<br/>Aggregation (has-parts): Transaction[]<br/>Other Associations: FraudDetectionService"],
]
t = Table(wrap_rows([["항목", "내용"]] + cm002_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("(3) CM-003 : Transaction (Model)", style_h4))
cm003 = [
    ["클래스 타입", "Concrete / Data Type", "관련 Use Case", "전 패키지"],
]
t = Table(wrap_spec_rows(cm003), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cm003_body = [
    ["설  명", "거래 데이터의 타입을 정의하는 TypeScript 인터페이스. 시스템 전체에서 공통 데이터 모델로 사용된다."],
    ["멤버 변수", "- id, userId, amount, paymentMethod, ipAddress, location, purchasedAt, riskScore, riskLevel, status"],
    ["멤버 함수", "(데이터 타입 정의로 메서드 없음)"],
    ["관계성", "Other Associations: TransactionService, FraudDetectionService, ApiClient"],
]
t = Table(wrap_rows([["항목", "내용"]] + cm003_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("3.1.3 패키지 행위", style_h3))
story.append(sequence_diagram_collect())
story.append(Spacer(1, 0.2 * cm))

story.append(p("3.1.4 멤버 함수(메소드) 설계", style_h3))
story.append(p("(1) M-001 : collect()", style_h4))
m001 = [
    ["소속 클래스", "CM-001 : TransactionController"],
    ["트리거 클래스", "외부 쇼핑몰 (HTTP POST 요청)"],
    ["파라미터", "req(Request), res(Response)"],
    ["세부 처리 로직", "1) req.body를 TransactionService.collectTransaction()에 전달한다.<br/>2) 반환된 Transaction 객체를 201 Created 응답과 함께 JSON으로 전송한다."],
]
t = Table(wrap_spec_rows(m001), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("(2) M-002 : list()", style_h4))
m002 = [
    ["소속 클래스", "CM-001 : TransactionController"],
    ["트리거 클래스", "관리자 브라우저 / DashboardPage (HTTP GET 요청)"],
    ["파라미터", "req(Request), res(Response)"],
    ["세부 처리 로직", "1) TransactionService.listTransactions()를 호출한다.<br/>2) 결과 배열을 200 OK 응답과 함께 JSON으로 전송한다."],
]
t = Table(wrap_spec_rows(m002), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("(3) M-003 : collectTransaction()", style_h4))
m003 = [
    ["소속 클래스", "CM-002 : TransactionService"],
    ["트리거 클래스", "CM-001 : TransactionController"],
    ["파라미터", "input(TransactionInput): 거래 수집 페이로드"],
    ["세부 처리 로직", "1) FraudDetectionService.classifyTransaction(input)을 호출하여 위험 점수/등급/상태를 부여한다.<br/>2) 결과 Transaction 객체를 메모리 저장소 배열 맨 앞에 unshift 한다.<br/>3) 새로 생성된 Transaction을 반환한다."],
]
t = Table(wrap_spec_rows(m003), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("(4) M-004 : listTransactions()", style_h4))
m004 = [
    ["소속 클래스", "CM-002 : TransactionService"],
    ["트리거 클래스", "CM-001 : TransactionController"],
    ["파라미터", "없음"],
    ["세부 처리 로직", "1) 메모리 저장소(transactions 배열)를 그대로 반환한다.<br/>2) 시간 역순(최신 거래 우선)으로 정렬된 상태를 유지한다."],
]
t = Table(wrap_spec_rows(m004), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(PageBreak())

# 3.2 FraudDetection
story.append(p("3.2 SDD-P-002 : FraudDetection 패키지", style_h2))
story.append(p("3.2.1 모듈 설명", style_h3))
desc2 = [
    ["패키지 설명", "수집된 거래에 대해 위험 점수를 산출하고 위험 등급 및 거래 상태를 결정하기 위한 패키지"],
    ["구성 클래스 - FraudDetectionService", "위험 점수를 받아 위험 등급(normal/suspicious/danger)을 결정하고, 거래 상태(approved/held/blocked)를 부여한다."],
    ["구성 클래스 - RiskService", "거래 데이터의 속성(금액·결제수단·위치)을 기반으로 위험 점수를 계산한다."],
]
t = Table(wrap_spec_rows(desc2), colWidths=[4.5 * cm, 11 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("3.2.2 구성 클래스 설계", style_h3))
story.append(p("(1) CL-001 : FraudDetectionService", style_h4))
cl001 = [
    ["클래스 타입", "Concrete", "관련 Use Case", "U_01"],
]
t = Table(wrap_spec_rows(cl001), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cl001_body = [
    ["설  명", "거래 데이터를 받아 RiskService를 통해 위험 점수를 산출하고, 임계값에 따라 위험 등급 및 거래 상태를 부여하여 Transaction 객체를 완성한다."],
    ["멤버 변수", "- riskService (의존성)"],
    ["멤버 함수", "+ classifyTransaction(payload)"],
    ["관계성", "Generalization (a-kind-of):<br/>Aggregation (has-parts):<br/>Other Associations: RiskService, Transaction"],
]
t = Table(wrap_rows([["항목", "내용"]] + cl001_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("(2) CL-002 : RiskService", style_h4))
cl002 = [
    ["클래스 타입", "Concrete", "관련 Use Case", "U_01"],
]
t = Table(wrap_spec_rows(cl002), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cl002_body = [
    ["설  명", "거래 데이터의 속성(금액·결제수단·위치)을 기반으로 규칙 기반 위험 점수를 0~100 범위로 산출한다."],
    ["멤버 변수", "- baseScore = 10<br/>- amountThreshold = 100,000<br/>- 가중치(35, 20, 20)"],
    ["멤버 함수", "+ calculateRiskScore(transaction)"],
    ["관계성", "Generalization (a-kind-of):<br/>Aggregation (has-parts):<br/>Other Associations: Transaction"],
]
t = Table(wrap_rows([["항목", "내용"]] + cl002_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("3.2.3 패키지 행위", style_h3))
story.append(p(
    "FraudDetectionService.classifyTransaction()는 RiskService.calculateRiskScore()를 호출하여 점수를 얻은 후, "
    "내부 함수 resolveRiskLevel()로 위험 등급을 결정하고, 등급에 따라 상태(approved / held / blocked)를 매핑하여 "
    "완성된 Transaction 객체를 TransactionService로 반환한다."
))

story.append(p("3.2.4 멤버 함수(메소드) 설계", style_h3))
story.append(p("(1) M-005 : classifyTransaction()", style_h4))
m005 = [
    ["소속 클래스", "CL-001 : FraudDetectionService"],
    ["트리거 클래스", "CM-002 : TransactionService"],
    ["파라미터", "payload(Omit&lt;Transaction, 'id'|'riskScore'|'riskLevel'|'status'&gt;)"],
    ["세부 처리 로직",
     "1) RiskService.calculateRiskScore(payload)를 호출하여 위험 점수를 산출한다.<br/>"
     "2) 점수가 80 이상이면 danger, 50 이상이면 suspicious, 그 외 normal로 분류한다.<br/>"
     "3) danger → blocked, suspicious → held, normal → approved로 상태를 매핑한다.<br/>"
     "4) crypto.randomUUID()로 id를 생성하고 payload, riskScore, riskLevel, status를 포함한 Transaction을 반환한다."],
]
t = Table(wrap_spec_rows(m005), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("(2) M-006 : calculateRiskScore()", style_h4))
m006 = [
    ["소속 클래스", "CL-002 : RiskService"],
    ["트리거 클래스", "CL-001 : FraudDetectionService"],
    ["파라미터", "transaction(TransactionPayload)"],
    ["세부 처리 로직",
     "1) 기본 점수 10점으로 시작한다.<br/>"
     "2) amount &gt; 100,000원이면 +35점을 가산한다.<br/>"
     "3) paymentMethod === 'new-card'이면 +20점을 가산한다.<br/>"
     "4) location === 'unknown'이면 +20점을 가산한다.<br/>"
     "5) Math.min(score, 100)으로 상한을 적용하여 반환한다."],
]
t = Table(wrap_spec_rows(m006), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(PageBreak())

# 3.3 Dashboard
story.append(p("3.3 SDD-P-003 : Dashboard 패키지", style_h2))
story.append(p("3.3.1 모듈 설명", style_h3))
desc3 = [
    ["패키지 설명", "관리자에게 실시간 거래 현황과 위험 거래 목록을 시각화하여 제공하는 프론트엔드 패키지"],
    ["구성 클래스 - DashboardPage", "대시보드 페이지 컨테이너 컴포넌트. 데이터 로딩과 필터 상태를 관리한다."],
    ["구성 클래스 - RiskSummaryCard", "거래/의심/차단 건수를 카드 형태로 표시하는 UI 컴포넌트"],
    ["구성 클래스 - TransactionTable", "거래 목록을 표 형태로 표시하고 필터·새로고침 컨트롤을 제공하는 컴포넌트"],
    ["구성 클래스 - ApiClient", "백엔드 REST API와의 통신을 담당하는 모듈(fetchTransactions)"],
]
t = Table(wrap_spec_rows(desc3), colWidths=[4.5 * cm, 11 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("3.3.2 구성 클래스 설계", style_h3))
story.append(p("(1) CN-001 : DashboardPage", style_h4))
cn001 = [
    ["클래스 타입", "Concrete (React Component)", "관련 Use Case", "U_02, U_03, U_04"],
]
t = Table(wrap_spec_rows(cn001), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cn001_body = [
    ["설  명", "관리자 대시보드의 최상위 페이지. 거래 목록 상태, 로딩 상태, 위험 등급 필터를 관리하고 자식 컴포넌트에 props로 전달한다."],
    ["멤버 변수", "- transactions: Transaction[]<br/>- loading: boolean<br/>- error: string | null<br/>- riskFilter: RiskFilter"],
    ["멤버 함수", "+ loadTransactions()<br/>+ render()"],
    ["관계성", "Generalization: React.FC<br/>Aggregation: RiskSummaryCard, TransactionTable<br/>Other Associations: ApiClient"],
]
t = Table(wrap_rows([["항목", "내용"]] + cn001_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("(2) CN-002 : RiskSummaryCard", style_h4))
cn002 = [
    ["클래스 타입", "Concrete (React Component)", "관련 Use Case", "U_02"],
]
t = Table(wrap_spec_rows(cn002), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cn002_body = [
    ["설  명", "거래 요약 정보를 카드 형식으로 표시한다. 톤(neutral / warning / danger)에 따라 색상이 다르게 표시된다."],
    ["멤버 변수", "- title: string<br/>- value: string<br/>- tone: 'neutral' | 'warning' | 'danger'"],
    ["멤버 함수", "+ render()"],
    ["관계성", "Generalization: React.FC<br/>Other Associations: DashboardPage"],
]
t = Table(wrap_rows([["항목", "내용"]] + cn002_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("(3) CN-003 : TransactionTable", style_h4))
cn003 = [
    ["클래스 타입", "Concrete (React Component)", "관련 Use Case", "U_02, U_03, U_04"],
]
t = Table(wrap_spec_rows(cn003), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cn003_body = [
    ["설  명", "거래 목록을 표 형태로 표시하고, 위험 등급 필터 드롭다운과 새로고침 버튼을 제공한다. 위험 등급/상태는 색상 뱃지로 표시된다."],
    ["멤버 변수", "- items: Transaction[]<br/>- loading?: boolean<br/>- riskFilter?: RiskFilter<br/>- onRefresh?: () =&gt; void<br/>- onRiskFilterChange?: (RiskFilter) =&gt; void"],
    ["멤버 함수", "+ render()"],
    ["관계성", "Generalization: React.FC<br/>Other Associations: DashboardPage, Transaction"],
]
t = Table(wrap_rows([["항목", "내용"]] + cn003_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("(4) CN-004 : ApiClient", style_h4))
cn004 = [
    ["클래스 타입", "Module (Service)", "관련 Use Case", "U_02"],
]
t = Table(wrap_spec_rows(cn004), colWidths=[3 * cm, 4 * cm, 3 * cm, 5.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
cn004_body = [
    ["설  명", "백엔드 REST API와의 모든 통신을 담당한다. 프론트엔드의 다른 모듈은 본 모듈을 통해서만 API를 호출한다."],
    ["멤버 변수", "- BASE_URL: string ('http://localhost:4000')"],
    ["멤버 함수", "+ fetchTransactions(): Promise&lt;Transaction[]&gt;"],
    ["관계성", "Other Associations: DashboardPage, TransactionController"],
]
t = Table(wrap_rows([["항목", "내용"]] + cn004_body, center_cols={0}),
          colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("3.3.3 패키지 행위", style_h3))
story.append(sequence_diagram_list())
story.append(Spacer(1, 0.2 * cm))

story.append(p("3.3.4 멤버 함수(메소드) 설계", style_h3))
story.append(p("(1) M-007 : loadTransactions()", style_h4))
m007 = [
    ["소속 클래스", "CN-001 : DashboardPage"],
    ["트리거 클래스", "관리자 (페이지 진입 / 새로고침 버튼 클릭)"],
    ["파라미터", "없음"],
    ["세부 처리 로직",
     "1) loading 상태를 true로, error를 null로 초기화한다.<br/>"
     "2) ApiClient.fetchTransactions()를 호출한다.<br/>"
     "3) 성공 시 setTransactions(데이터)로 상태를 갱신한다.<br/>"
     "4) 실패 시 setError(e.message)로 오류 상태를 갱신한다.<br/>"
     "5) finally 블록에서 loading을 false로 변경한다."],
]
t = Table(wrap_spec_rows(m007), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("(2) M-008 : fetchTransactions()", style_h4))
m008 = [
    ["소속 클래스", "CN-004 : ApiClient"],
    ["트리거 클래스", "CN-001 : DashboardPage"],
    ["파라미터", "없음"],
    ["세부 처리 로직",
     "1) fetch('http://localhost:4000/api/transactions')를 호출한다.<br/>"
     "2) 응답이 ok가 아니면 Error를 throw 한다.<br/>"
     "3) JSON으로 파싱한 Transaction 배열을 Promise로 반환한다."],
]
t = Table(wrap_spec_rows(m008), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(Spacer(1, 0.2 * cm))

story.append(p("(3) M-009 : onRiskFilterChange()", style_h4))
m009 = [
    ["소속 클래스", "CN-003 : TransactionTable"],
    ["트리거 클래스", "관리자 (필터 드롭다운 변경)"],
    ["파라미터", "value: RiskFilter"],
    ["세부 처리 로직",
     "1) 드롭다운에서 선택된 값을 부모(DashboardPage)의 setRiskFilter에 전달한다.<br/>"
     "2) DashboardPage는 useMemo를 통해 transactions를 필터링한다.<br/>"
     "3) 필터링된 결과가 표에 즉시 반영된다."],
]
t = Table(wrap_spec_rows(m009), colWidths=[3 * cm, 12.5 * cm])
t.setStyle(make_spec_table_style())
story.append(t)
story.append(PageBreak())

# ===== 4. 인터페이스 설계 =====
story.append(p("4. 인터페이스 설계", style_h1))

story.append(p("4.1 외부 시스템 인터페이스", style_h2))
story.append(p(
    "SafePay의 외부 시스템 인터페이스는 REST API 형태로 제공되며, 외부 쇼핑몰과 관리자 브라우저가 "
    "백엔드와 통신하는 데 사용된다."
))
iface = [
    ["메시지명", "송신 모듈", "수신 모듈", "메시지 형식", "전송 방식"],
    ["거래 수집 요청", "외부 쇼핑몰", "TransactionController", "POST /api/transactions<br/>(JSON Body)", "HTTP / JSON"],
    ["거래 수집 응답", "TransactionController", "외부 쇼핑몰", "201 Created (Transaction JSON)", "HTTP / JSON"],
    ["거래 목록 요청", "DashboardPage (관리자)", "TransactionController", "GET /api/transactions", "HTTP / JSON"],
    ["거래 목록 응답", "TransactionController", "DashboardPage", "200 OK (Transaction[] JSON)", "HTTP / JSON"],
    ["헬스 체크", "운영 모니터링", "Express app", "GET /health", "HTTP / JSON"],
]
t = Table(wrap_rows(iface, center_cols={0, 1, 2, 4}),
         colWidths=[2.8 * cm, 3.2 * cm, 3.4 * cm, 3.9 * cm, 2.4 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("[POST /api/transactions 요청 본문 예시]", style_h3))
req_example = [
    ["필드", "타입", "예시 값"],
    ["userId", "string", "user-01"],
    ["amount", "number", "250000"],
    ["paymentMethod", "string", "new-card"],
    ["ipAddress", "string", "203.0.113.10"],
    ["location", "string", "unknown"],
    ["purchasedAt", "string (ISO8601)", "2026-05-03T09:12:00.000Z"],
]
t = Table(wrap_rows(req_example, center_cols={0, 1}),
         colWidths=[4 * cm, 4 * cm, 7.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.4 * cm))

story.append(p("4.2 사용자 인터페이스", style_h2))
story.append(p(
    "관리자 대시보드는 단일 페이지(SPA)로 구성되며 상단에 요약 카드 3개, 하단에 거래 목록 표를 "
    "배치한다. 표 상단에는 위험 등급 필터 드롭다운과 새로고침 버튼이 위치한다."
))
story.append(ui_mockup_diagram())
story.append(Spacer(1, 0.3 * cm))

ui_table = [
    ["UI 영역", "설명"],
    ["헤더", "SafePay Admin / 대시보드 제목 및 안내 문구"],
    ["요약 카드 영역", "실시간 거래, 의심 거래, 차단 거래 건수를 색상별 카드로 시각화"],
    ["필터/제어 영역", "위험 등급 드롭다운(전체/정상/의심/위험) + 새로고침 버튼"],
    ["거래 목록 표", "거래 ID·사용자·금액·결제수단·위험점수·등급 뱃지·상태 뱃지·구매시각 컬럼"],
    ["오류 영역", "API 요청 실패 시 표 상단에 빨간색 강조 텍스트로 메시지 표시"],
]
t = Table(wrap_rows(ui_table, center_cols={0}), colWidths=[4 * cm, 12 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(PageBreak())

# ===== 5. 데이터 설계 =====
story.append(p("5. 데이터 설계", style_h1))
story.append(p(
    "SafePay 시스템의 데이터는 백엔드 프로세스의 메모리(in-memory)에 보관되며, 서버 재시작 시 시드 "
    "데이터로 초기화된다. 영구 저장소(RDBMS) 도입은 향후 확장 단계의 과제이며 본 설계서는 데이터의 "
    "구조와 저장 방식을 함께 기술한다."
))

story.append(p("(1) DD-01, Transaction (거래 정보)", style_h3))
dd01 = [
    ["번호", "필드명", "자료타입", "값의 범위", "초기 값", "비고"],
    ["1", "id", "string (UUID)", "UUIDv4 형식", "crypto.randomUUID()", "PK"],
    ["2", "userId", "string", "임의의 사용자 식별자", "not Null", ""],
    ["3", "amount", "number", "0 이상의 정수(원화)", "not Null", "결제 금액"],
    ["4", "paymentMethod", "string", "card / new-card 등", "not Null", ""],
    ["5", "ipAddress", "string", "IPv4 문자열", "not Null", ""],
    ["6", "location", "string", "도시명 또는 unknown", "not Null", ""],
    ["7", "purchasedAt", "string", "ISO 8601 (UTC)", "not Null", ""],
    ["8", "riskScore", "number", "0 ~ 100", "0", "산출값"],
    ["9", "riskLevel", "string", "normal / suspicious / danger", "normal", "산출값"],
    ["10", "status", "string", "approved / held / blocked", "approved", "산출값"],
]
t = Table(wrap_rows(dd01, center_cols={0, 2, 3, 4, 5}),
         colWidths=[1.2 * cm, 3 * cm, 2.7 * cm, 4 * cm, 3 * cm, 1.6 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("(2) DD-02, RiskRule (위험 점수 규칙)", style_h3))
dd02 = [
    ["번호", "필드명", "자료타입", "값의 범위", "초기 값", "비고"],
    ["1", "baseScore", "number", "0 이상", "10", "기본 점수"],
    ["2", "amountWeight", "number", "0 이상", "35", "고액 거래 가중치"],
    ["3", "newCardWeight", "number", "0 이상", "20", "신규 카드 가중치"],
    ["4", "unknownLocWeight", "number", "0 이상", "20", "위치 불명 가중치"],
    ["5", "amountThreshold", "number", "0 이상", "100,000", "고액 임계값"],
    ["6", "scoreCap", "number", "0 이상", "100", "점수 상한"],
]
t = Table(wrap_rows(dd02, center_cols={0, 2, 3, 4, 5}),
         colWidths=[1.2 * cm, 3.2 * cm, 2.5 * cm, 2.5 * cm, 2.2 * cm, 3.9 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("(3) DD-03, 저장 방식", style_h3))
storage = [
    ["구분", "설명"],
    ["저장 위치", "백엔드 Node.js 프로세스의 메모리 (Transaction[] 배열)"],
    ["초기화", "서버 기동 시 seedInputs(8건)을 FraudDetectionService로 분류하여 배열에 적재"],
    ["저장 순서", "신규 거래 수집 시 배열 맨 앞(unshift)에 삽입 → 시간 역순 자동 유지"],
    ["영속성", "프로세스 재시작 시 휘발 (시드 데이터로 재초기화됨)"],
    ["확장 계획", "향후 PostgreSQL + Prisma 등의 영구 저장소 도입 예정"],
]
t = Table(wrap_rows(storage, center_cols={0}), colWidths=[3.5 * cm, 12 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(PageBreak())

# ===== 6. 구현 기술 설계 =====
story.append(p("6. 구현 기술 설계", style_h1))
tech = [
    ["구분", "클라이언트", "서버", "비고"],
    ["구현 언어", "TypeScript (React)", "TypeScript (Node.js)", ""],
    ["프레임워크", "React 18 + Vite", "Express 4", "Vite 개발 서버"],
    ["운영체제", "Windows / macOS / Linux<br/>(브라우저 환경)", "Windows / Linux (Node.js)", "단일 서버"],
    ["특수 소프트웨어", "ESLint<br/>TypeScript 컴파일러", "ts-node-dev<br/>cors / dotenv 모듈", "타입 안전성"],
    ["하드웨어 (개발)", "intel i5 8세대 CPU 이상<br/>RAM 8GB<br/>SSD 256GB", "동일", "데모 환경"],
    ["네트워크", "TCP/IP<br/>HTTP 1.1", "TCP/IP<br/>HTTP 1.1", "Port 4000(API), 5173(Vite)"],
    ["데이터 저장", "브라우저 상태(React)", "In-memory 배열", "향후 RDBMS 확장"],
    ["빌드 도구", "Vite (npm run dev / build)", "tsc (npm run build)", ""],
]
t = Table(wrap_rows(tech, center_cols={0}),
         colWidths=[3 * cm, 4.5 * cm, 4.5 * cm, 3.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("6.1 적용 기술 및 개발 환경 보충", style_h2))
notes = [
    "1) 백엔드는 Express + TypeScript 기반 계층 아키텍처(Controller → Service → Model)로 구성한다.",
    "2) 의존성 주입은 모듈 단위 객체 리터럴(transactionService, fraudDetectionService, riskService)로 단순화한다.",
    "3) 프론트엔드는 React 함수형 컴포넌트 + Hooks(useState/useEffect/useMemo/useCallback) 패턴을 적용한다.",
    "4) 위험 점수 산출은 규칙 기반 모듈(risk.service.ts)에 캡슐화하여 향후 머신러닝 모델로 교체 가능하도록 한다.",
    "5) 프론트엔드는 services/api.ts를 단일 진입점으로 사용하여 백엔드 통신을 캡슐화한다.",
    "6) 모든 텍스트 응답과 UI 라벨은 UTF-8 / 한국어를 기본으로 한다.",
]
for note in notes:
    story.append(p(note))
story.append(PageBreak())

# ===== 7. 요구사항 추적표 =====
story.append(p("7. 요구사항 추적표", style_h1))
story.append(p(
    "본 절은 요구사항 정의서의 기능 요구사항(FR)과 본 설계서의 멤버 함수(M-001 ~ M-009) 간의 추적 관계를 "
    "정리한다. 점(●)은 해당 요구사항이 해당 메소드에서 구현됨을 의미한다."
))

trace_header = ["요구사항 \\ 메소드", "M-001<br/>collect", "M-002<br/>list",
                "M-003<br/>collect<br/>Transaction", "M-004<br/>list<br/>Transactions",
                "M-005<br/>classify<br/>Transaction", "M-006<br/>calculate<br/>RiskScore",
                "M-007<br/>load<br/>Transactions", "M-008<br/>fetch<br/>Transactions",
                "M-009<br/>onFilter<br/>Change"]

# 매핑 정의
mapping = {
    "FR-001 거래 수신": [0, 2],
    "FR-002 UUID 부여": [4],
    "FR-003 요청 본문 필드": [0, 2],
    "FR-004 시간 역순 저장": [2],
    "FR-005 기본 점수 10": [5],
    "FR-006 +35점(고액)": [5],
    "FR-007 +20점(new-card)": [5],
    "FR-008 +20점(unknown)": [5],
    "FR-009 0~100 상한": [5],
    "FR-010 ≥80 danger": [4],
    "FR-011 ≥50 suspicious": [4],
    "FR-012 <50 normal": [4],
    "FR-013 danger→blocked": [4],
    "FR-014 suspicious→held": [4],
    "FR-015 normal→approved": [4],
    "FR-016 거래 조회 API": [1, 3, 7],
    "FR-017 응답 필드": [1, 3, 7],
    "FR-018 표 형식 표시": [6, 7],
    "FR-019 위험 등급 필터": [8],
    "FR-020 새로고침": [6, 7],
}

trace_rows = [trace_header]
for req, cols in mapping.items():
    row = [req]
    for i in range(9):
        row.append("●" if i in cols else "")
    trace_rows.append(row)

t = Table(wrap_rows(trace_rows, center_cols=set(range(1, 10))),
         colWidths=[3.0 * cm] + [1.36 * cm] * 9)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "MalgunBold"),
    ("FONTNAME", (0, 1), (-1, -1), "Malgun"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
    ("TEXTCOLOR", (1, 1), (-1, -1), colors.HexColor("#2f855a")),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(PageBreak())

# ===== 8. 부록 =====
story.append(p("8. 부록", style_h1))

story.append(p("부록 A. 위험 점수 / 등급 / 상태 매핑표", style_h2))
appendix_a = [
    ["위험 점수 범위", "위험 등급", "거래 상태", "UI 색상 뱃지"],
    ["80점 이상", "danger (위험)", "blocked (차단)", "빨강"],
    ["50점 이상 ~ 80점 미만", "suspicious (의심)", "held (보류)", "주황"],
    ["50점 미만", "normal (정상)", "approved (승인)", "녹색"],
]
t = Table(wrap_rows(appendix_a, center_cols={0, 1, 2, 3}),
         colWidths=[5 * cm, 4 * cm, 4 * cm, 2.5 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("부록 B. 디렉터리 구조", style_h2))
dir_tree = (
    "SafePay/<br/>"
    "├── backend/<br/>"
    "│   └── src/<br/>"
    "│       ├── app.ts / server.ts<br/>"
    "│       ├── config/env.ts<br/>"
    "│       ├── controllers/transaction.controller.ts<br/>"
    "│       ├── middlewares/error.middleware.ts<br/>"
    "│       ├── models/transaction.model.ts<br/>"
    "│       ├── routes/index.ts, transaction.routes.ts<br/>"
    "│       └── services/transaction.service.ts, fraud-detection.service.ts, risk.service.ts<br/>"
    "├── frontend/<br/>"
    "│   └── src/<br/>"
    "│       ├── App.tsx / main.tsx<br/>"
    "│       ├── pages/DashboardPage.tsx<br/>"
    "│       ├── components/RiskSummaryCard.tsx, TransactionTable.tsx<br/>"
    "│       ├── services/api.ts<br/>"
    "│       └── types/transaction.ts<br/>"
    "└── docs/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;├── system-structure.md<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;├── generate_requirements_pdf.py<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;└── generate_design_pdf.py"
)
story.append(p(dir_tree))
story.append(Spacer(1, 0.3 * cm))

story.append(p("부록 C. 변경 이력", style_h2))
history = [
    ["버전", "일자", "작성자", "내용"],
    ["v1.0", "2026-05-18", "박정호", "초안 작성 (전체 설계 항목)"],
]
t = Table(wrap_rows(history, center_cols={0, 1, 2}),
         colWidths=[2 * cm, 3 * cm, 3 * cm, 7.5 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)

# PDF 생성
doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm,
    title="SafePay 소프트웨어 설계서",
    author="박정호(2021125025)",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF generated: {OUTPUT_PATH}")
print(f"Size: {os.path.getsize(OUTPUT_PATH)} bytes")
