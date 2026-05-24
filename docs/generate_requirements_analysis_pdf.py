# -*- coding: utf-8 -*-
"""SafePay 요구사항 분석서 PDF 생성 스크립트 (7-Section 양식)"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.graphics.shapes import (
    Drawing, Rect, Line, String, Circle, Ellipse, Polygon
)

# ---------------- 한글 폰트 ----------------
pdfmetrics.registerFont(TTFont("Malgun", "C:/Windows/Fonts/malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", "C:/Windows/Fonts/malgunbd.ttf"))

OUTPUT_PATH = r"C:/Users/bagje/Desktop/SafePay_요구사항분석서.pdf"

# ---------------- 스타일 ----------------
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "title", parent=styles["Title"], fontName="MalgunBold",
    fontSize=24, leading=30, alignment=TA_CENTER, spaceAfter=18,
)
style_cover_sub = ParagraphStyle(
    "cover_sub", parent=styles["Normal"], fontName="Malgun",
    fontSize=13, leading=20, alignment=TA_CENTER, spaceAfter=8,
)
style_toc_title = ParagraphStyle(
    "toc_title", parent=styles["Title"], fontName="MalgunBold",
    fontSize=20, leading=28, alignment=TA_CENTER, spaceAfter=18,
)
style_h1 = ParagraphStyle(
    "h1", parent=styles["Heading1"], fontName="MalgunBold",
    fontSize=18, leading=24, spaceBefore=14, spaceAfter=10,
    textColor=colors.HexColor("#1a3a6c"),
)
style_h2 = ParagraphStyle(
    "h2", parent=styles["Heading2"], fontName="MalgunBold",
    fontSize=14, leading=20, spaceBefore=10, spaceAfter=6,
    textColor=colors.HexColor("#2c5282"),
)
style_h3 = ParagraphStyle(
    "h3", parent=styles["Heading3"], fontName="MalgunBold",
    fontSize=12, leading=18, spaceBefore=8, spaceAfter=4,
    textColor=colors.HexColor("#2d3748"),
)
style_body = ParagraphStyle(
    "body", parent=styles["Normal"], fontName="Malgun",
    fontSize=10.5, leading=17, spaceAfter=6, alignment=TA_LEFT,
)
style_caption = ParagraphStyle(
    "caption", parent=styles["Normal"], fontName="Malgun",
    fontSize=9.5, leading=14, alignment=TA_CENTER,
    textColor=colors.HexColor("#4a5568"), spaceAfter=10,
)
style_toc = ParagraphStyle(
    "toc", parent=styles["Normal"], fontName="MalgunBold",
    fontSize=12, leading=24,
)
style_toc_sub = ParagraphStyle(
    "toc_sub", parent=styles["Normal"], fontName="Malgun",
    fontSize=10.5, leading=20, leftIndent=18,
)

# ---------------- 셀(Paragraph) 스타일 ----------------
cell_normal = ParagraphStyle(
    "cell_normal", parent=styles["Normal"], fontName="Malgun",
    fontSize=9.5, leading=13, alignment=TA_LEFT, spaceAfter=0,
)
cell_center = ParagraphStyle(
    "cell_center", parent=cell_normal, alignment=TA_CENTER,
)
cell_header = ParagraphStyle(
    "cell_header", parent=styles["Normal"], fontName="MalgunBold",
    fontSize=9.5, leading=13, alignment=TA_CENTER, spaceAfter=0,
    textColor=colors.white,
)
cell_label = ParagraphStyle(
    "cell_label", parent=styles["Normal"], fontName="MalgunBold",
    fontSize=9.5, leading=13, alignment=TA_CENTER, spaceAfter=0,
)
cell_label_left = ParagraphStyle(
    "cell_label_left", parent=cell_label, alignment=TA_LEFT,
)

def _to_text(value):
    if value is None:
        return ""
    return str(value).replace("\n", "<br/>")

def WP(text, style=cell_normal):
    """Wrap value as Paragraph (auto-wrap)."""
    if isinstance(text, Paragraph):
        return text
    return Paragraph(_to_text(text), style)

def WC(text):
    return WP(text, cell_center)

def WH(text):
    """Header cell."""
    return WP(text, cell_header)

def WL(text):
    """Label cell (bold, center)."""
    return WP(text, cell_label)

def WLL(text):
    """Label cell (bold, left)."""
    return WP(text, cell_label_left)

def wrap_grid(data, header=True, first_col_label=True):
    """Wrap a 2D list so each cell is a Paragraph that auto-wraps."""
    out = []
    for i, row in enumerate(data):
        new_row = []
        for j, c in enumerate(row):
            if header and i == 0:
                new_row.append(WH(c))
            elif first_col_label and j == 0:
                new_row.append(WL(c))
            else:
                new_row.append(WP(c))
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
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f7fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ])

def make_usecase_table_style():
    return TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Malgun"),
        ("FONTNAME", (0, 0), (0, -1), "MalgunBold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#a0aec0")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf2f7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ])

# ---------------- 헤더/푸터 ----------------
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Malgun", 9)
    canvas.setFillColor(colors.HexColor("#4a5568"))
    canvas.drawString(2 * cm, A4[1] - 1.2 * cm,
                      "SafePay - 온라인 쇼핑 사기 탐지 시스템")
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.2 * cm,
                           "요구사항 분석서")
    canvas.setStrokeColor(colors.HexColor("#cbd5e0"))
    canvas.line(2 * cm, A4[1] - 1.4 * cm,
                A4[0] - 2 * cm, A4[1] - 1.4 * cm)
    canvas.drawCentredString(A4[0] / 2.0, 1.2 * cm, f"- {doc.page} -")
    canvas.restoreState()

def p(text, style=style_body):
    return Paragraph(text, style)

# =========================================================
# 다이어그램: UseCase Diagram
# =========================================================
def draw_usecase_diagram():
    d = Drawing(440, 360)

    # System boundary
    d.add(Rect(70, 20, 300, 320, strokeColor=colors.black,
               fillColor=None, strokeWidth=1))
    d.add(String(220, 330, "<SafePay 사기 탐지 시스템>",
                 fontName="Malgun", fontSize=10,
                 textAnchor="middle"))

    # Actors
    def stickman(cx, cy, label):
        d.add(Circle(cx, cy + 22, 6, strokeColor=colors.black,
                     fillColor=colors.white))
        d.add(Line(cx, cy + 16, cx, cy, strokeColor=colors.black))
        d.add(Line(cx, cy + 12, cx - 8, cy + 4, strokeColor=colors.black))
        d.add(Line(cx, cy + 12, cx + 8, cy + 4, strokeColor=colors.black))
        d.add(Line(cx, cy, cx - 6, cy - 10, strokeColor=colors.black))
        d.add(Line(cx, cy, cx + 6, cy - 10, strokeColor=colors.black))
        d.add(String(cx, cy - 22, label, fontName="Malgun",
                     fontSize=9, textAnchor="middle"))

    stickman(30, 230, "관리자")
    stickman(30, 130, "외부 쇼핑몰")
    stickman(410, 180, "시스템")

    # Use cases (ellipses)
    def uc(cx, cy, txt):
        d.add(Ellipse(cx, cy, 56, 16,
                      strokeColor=colors.black,
                      fillColor=colors.HexColor("#f7fafc")))
        d.add(String(cx, cy - 3, txt, fontName="Malgun",
                     fontSize=8.5, textAnchor="middle"))
        return (cx, cy)

    uc1 = uc(160, 290, "거래를 수집한다")
    uc2 = uc(280, 290, "위험 점수를 계산한다")
    uc3 = uc(160, 240, "사기 거래를 분류한다")
    uc4 = uc(280, 240, "거래 상태를 결정한다")
    uc5 = uc(160, 180, "거래 목록을 조회한다")
    uc6 = uc(280, 180, "위험 등급으로 필터링한다")
    uc7 = uc(160, 120, "대시보드를 새로고침한다")
    uc8 = uc(280, 120, "요약 통계를 확인한다")
    uc9 = uc(220, 60, "오류 메시지를 표시한다")

    def line(a, b):
        d.add(Line(a[0], a[1], b[0], b[1],
                   strokeColor=colors.HexColor("#4a5568"),
                   strokeWidth=0.6))

    # 외부 쇼핑몰 -> 거래 수집
    line((42, 152), (uc1[0] - 56, uc1[1]))
    # 관리자
    line((42, 252), (uc5[0] - 56, uc5[1]))
    line((42, 252), (uc6[0] - 56, uc6[1]))
    line((42, 252), (uc7[0] - 56, uc7[1]))
    line((42, 252), (uc8[0] - 56, uc8[1]))
    # 시스템
    line((398, 200), (uc2[0] + 56, uc2[1]))
    line((398, 200), (uc3[0] + 56, uc3[1]))
    line((398, 200), (uc4[0] + 56, uc4[1]))
    line((398, 200), (uc9[0] + 56, uc9[1]))

    return d

# =========================================================
# 다이어그램: Class Diagram (정적 분석)
# =========================================================
def draw_class_diagram():
    d = Drawing(520, 420)

    def cls(x, y, w, h, name, attrs, methods):
        d.add(Rect(x, y, w, h, strokeColor=colors.black,
                   fillColor=colors.white))
        # title bar
        d.add(Rect(x, y + h - 18, w, 18, strokeColor=colors.black,
                   fillColor=colors.HexColor("#e2e8f0")))
        d.add(String(x + w / 2, y + h - 13, name,
                     fontName="MalgunBold", fontSize=9,
                     textAnchor="middle"))
        # attribute section
        ay = y + h - 32
        for a in attrs:
            d.add(String(x + 4, ay, "- " + a, fontName="Malgun",
                         fontSize=7.5))
            ay -= 11
        # separator
        sep_y = ay + 3
        d.add(Line(x, sep_y, x + w, sep_y, strokeColor=colors.black))
        # methods
        my = sep_y - 11
        for m in methods:
            d.add(String(x + 4, my, "+ " + m, fontName="Malgun",
                         fontSize=7.5))
            my -= 11

    # Transaction (model)
    cls(20, 290, 140, 120, "Transaction",
        ["id: string", "userId: string", "amount: number",
         "paymentMethod: string", "ipAddress: string",
         "location: string", "purchasedAt: string"],
        ["getRiskInfo(): object"])

    # RiskInfo (embedded)
    cls(180, 290, 130, 120, "RiskInfo",
        ["riskScore: number (0-100)", "riskLevel: RiskLevel",
         "status: Status"],
        ["resolveLevel(): RiskLevel"])

    # RiskService
    cls(340, 290, 160, 120, "RiskService",
        ["BASE_SCORE: 10",
         "AMOUNT_THRESHOLD: 100000",
         "HIGH_AMOUNT_ADD: 35",
         "NEW_CARD_ADD: 20",
         "UNKNOWN_LOC_ADD: 20"],
        ["calculateRiskScore(t): number"])

    # FraudDetectionService
    cls(20, 150, 200, 120, "FraudDetectionService",
        ["DANGER_THRESHOLD: 80",
         "SUSPICIOUS_THRESHOLD: 50"],
        ["classifyTransaction(payload):",
         "    Transaction",
         "resolveRiskLevel(score):",
         "    RiskLevel"])

    # TransactionService
    cls(240, 150, 160, 120, "TransactionService",
        ["transactions: Transaction[]",
         "seedInputs: TxInput[]"],
        ["collectTransaction(in):",
         "    Transaction",
         "listTransactions():",
         "    Transaction[]"])

    # TransactionController
    cls(420, 150, 80, 120, "Tx Controller",
        [""],
        ["collect(req,res)",
         "list(req,res)"])

    # Frontend: DashboardPage
    cls(20, 10, 160, 120, "DashboardPage",
        ["transactions: Tx[]",
         "loading: boolean",
         "error: string|null",
         "riskFilter: RiskFilter"],
        ["loadTransactions(): void",
         "render(): JSX"])

    # TransactionTable
    cls(200, 10, 160, 120, "TransactionTable",
        ["items: Transaction[]",
         "riskFilter: RiskFilter"],
        ["onRefresh(): void",
         "onRiskFilterChange(v):",
         "    void"])

    # RiskSummaryCard
    cls(380, 10, 120, 120, "RiskSummaryCard",
        ["title: string",
         "value: string",
         "tone: Tone"],
        ["render(): JSX"])

    # 연관관계 (선)
    def line(x1, y1, x2, y2):
        d.add(Line(x1, y1, x2, y2,
                   strokeColor=colors.HexColor("#2d3748"),
                   strokeWidth=0.6))
    # Transaction --o RiskInfo
    line(160, 350, 180, 350)
    # FraudDetectionService -> RiskService
    line(220, 210, 340, 350)
    # FraudDetectionService -> Transaction
    line(120, 270, 90, 290)
    # TransactionService -> FraudDetectionService
    line(240, 210, 220, 210)
    # TransactionController -> TransactionService
    line(420, 210, 400, 210)
    # DashboardPage -> TransactionTable
    line(180, 70, 200, 70)
    # DashboardPage -> RiskSummaryCard
    line(180, 100, 380, 100)
    # DashboardPage --> TransactionController (HTTP)
    line(100, 130, 460, 150)

    return d

# =========================================================
# 다이어그램: Sequence Diagram helper
# =========================================================
def draw_sequence(title, actors, steps, width=520, height=None):
    """
    actors: [(label, kind)] kind in {"actor", "object"}
    steps:  [(from_idx, to_idx, label, style)] style in {"sync", "async", "return"}
    """
    n = len(actors)
    col_w = width / (n + 1)
    top_band = 40
    step_h = 26
    if height is None:
        height = top_band + 40 + step_h * len(steps) + 30
    d = Drawing(width, height)

    # Title banner
    d.add(Rect(0, height - 20, width, 20,
               strokeColor=colors.HexColor("#cbd5e0"),
               fillColor=colors.HexColor("#edf2f7")))
    d.add(String(width / 2, height - 14, "sd: " + title,
                 fontName="MalgunBold", fontSize=9,
                 textAnchor="middle"))

    # Actor heads and lifelines
    col_x = []
    for i, (label, kind) in enumerate(actors):
        cx = col_w * (i + 1)
        col_x.append(cx)
        if kind == "actor":
            # stickman
            base_y = height - 40
            d.add(Circle(cx, base_y - 4, 5, strokeColor=colors.black,
                         fillColor=colors.white))
            d.add(Line(cx, base_y - 9, cx, base_y - 19,
                       strokeColor=colors.black))
            d.add(Line(cx, base_y - 12, cx - 6, base_y - 16,
                       strokeColor=colors.black))
            d.add(Line(cx, base_y - 12, cx + 6, base_y - 16,
                       strokeColor=colors.black))
            d.add(Line(cx, base_y - 19, cx - 5, base_y - 27,
                       strokeColor=colors.black))
            d.add(Line(cx, base_y - 19, cx + 5, base_y - 27,
                       strokeColor=colors.black))
            d.add(String(cx, base_y - 38, label,
                         fontName="Malgun", fontSize=8.5,
                         textAnchor="middle"))
            top_y = base_y - 42
        else:
            box_w = max(70, len(label) * 7)
            box_x = cx - box_w / 2
            box_y = height - 60
            d.add(Rect(box_x, box_y, box_w, 18,
                       strokeColor=colors.black,
                       fillColor=colors.HexColor("#f7fafc")))
            d.add(String(cx, box_y + 5, ":" + label,
                         fontName="Malgun", fontSize=8.5,
                         textAnchor="middle"))
            top_y = box_y
        # lifeline (dashed)
        d.add(Line(cx, top_y, cx, 20,
                   strokeColor=colors.HexColor("#718096"),
                   strokeDashArray=[2, 2]))

    # Steps
    y = height - 80
    for (f, t, label, kind) in steps:
        x1 = col_x[f]
        x2 = col_x[t]
        if kind == "return":
            d.add(Line(x1, y, x2, y,
                       strokeColor=colors.HexColor("#2d3748"),
                       strokeDashArray=[3, 2], strokeWidth=0.7))
        else:
            d.add(Line(x1, y, x2, y,
                       strokeColor=colors.HexColor("#2d3748"),
                       strokeWidth=0.8))
        # arrow head
        if x2 > x1:
            d.add(Polygon([x2, y, x2 - 5, y + 3, x2 - 5, y - 3],
                          strokeColor=colors.HexColor("#2d3748"),
                          fillColor=colors.HexColor("#2d3748")))
        elif x2 < x1:
            d.add(Polygon([x2, y, x2 + 5, y + 3, x2 + 5, y - 3],
                          strokeColor=colors.HexColor("#2d3748"),
                          fillColor=colors.HexColor("#2d3748")))
        # label
        lx = (x1 + x2) / 2
        d.add(String(lx, y + 3, label, fontName="Malgun",
                     fontSize=8, textAnchor="middle"))
        y -= step_h

    return d

# =========================================================
# Story 구성
# =========================================================
story = []

# ===== 표지 =====
story.append(Spacer(1, 4 * cm))
story.append(p("요 구 사 항 분 석 서", style_title))
story.append(Spacer(1, 0.8 * cm))
story.append(p("SafePay", style_cover_sub))
story.append(p("온라인 쇼핑 사기 탐지 시스템", style_cover_sub))
story.append(Spacer(1, 5 * cm))

cover_cell_label = ParagraphStyle(
    "cover_label", parent=cell_label, fontSize=11, leading=15)
cover_cell_value = ParagraphStyle(
    "cover_value", parent=cell_normal, fontSize=11, leading=15)
cover_table = Table(
    [
        [WP("프로젝트명", cover_cell_label),
         WP("SafePay - 온라인 쇼핑 사기 탐지 시스템", cover_cell_value)],
        [WP("문서명", cover_cell_label),
         WP("요구사항 분석서", cover_cell_value)],
        [WP("문서 버전", cover_cell_label),
         WP("v1.0", cover_cell_value)],
        [WP("작성일", cover_cell_label),
         WP("2026-05-18", cover_cell_value)],
        [WP("작성자", cover_cell_label),
         WP("박정호 (2021125025)", cover_cell_value)],
        [WP("문서 상태", cover_cell_label),
         WP("초안", cover_cell_value)],
    ],
    colWidths=[4 * cm, 10 * cm],
)
cover_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf2f7")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(cover_table)
story.append(PageBreak())

# ===== 목 차 =====
story.append(p("목 &nbsp;&nbsp;&nbsp; 차", style_toc_title))
story.append(Spacer(1, 0.5 * cm))

toc_items = [
    ("1. 서론", style_toc),
    ("1.1 목적 및 범위", style_toc_sub),
    ("1.2 용어 정의", style_toc_sub),
    ("1.3 참조 문서", style_toc_sub),
    ("2. 시스템 개요", style_toc),
    ("2.1 소프트웨어 컨텍스트(Context)", style_toc_sub),
    ("2.2 기능 분류 및 설명", style_toc_sub),
    ("3. 요구사항 명세", style_toc),
    ("3.1 정적 분석", style_toc_sub),
    ("3.2 CRC 카드", style_toc_sub),
    ("3.3 동적 분석", style_toc_sub),
    ("4. 인터페이스 분석", style_toc),
    ("5. 제약사항", style_toc),
    ("6. 요구사항 추적표", style_toc),
    ("7. 참고문헌 및 부록", style_toc),
]
for text, st in toc_items:
    story.append(p(text, st))
story.append(PageBreak())

# =========================================================
# 1. 서 론
# =========================================================
story.append(p("1. 서 론", style_h1))

story.append(p("1.1 목적 및 범위", style_h2))
story.append(p(
    "본 문서는 온라인 쇼핑 환경에서 발생하는 결제 사기를 실시간으로 탐지하고 차단하기 위한 "
    "<b>SafePay</b> 시스템 개발 프로젝트의 요구사항을 객체지향 관점에서 분석·명세하는 것을 "
    "목적으로 한다. 본 문서는 이해관계자(개발자·운영자·관리자) 간의 합의된 기준을 제공하며, "
    "정적 분석(클래스 다이어그램), 동적 분석(시퀀스 다이어그램), CRC 카드 등 객체/행위 분석 "
    "자료를 통해 시스템의 구조와 행위를 정의한다."
))
story.append(p(
    "본 문서의 범위는 거래 데이터 수집 API, 위험 점수 산출 엔진, 사기 탐지 분류 로직, "
    "관리자 대시보드 화면을 포함하며, 외부 결제 게이트웨이(PG) 연동·모바일 앱 개발·머신러닝 "
    "기반 탐지 모델은 본 문서의 범위에서 제외한다."
))

story.append(p("1.2 용어 정의", style_h2))
terms_data = [
    ["용어", "설명"],
    ["거래(Transaction)",
     "사용자가 온라인 쇼핑몰에서 결제한 단위 행위. 금액·결제수단·IP·위치·시각의 속성을 가진다."],
    ["위험 점수(Risk Score)",
     "거래의 사기 가능성을 0 ~ 100 정수로 표현한 값."],
    ["위험 등급(Risk Level)",
     "위험 점수를 기준으로 분류한 정상(normal) / 의심(suspicious) / 위험(danger) 3단계."],
    ["거래 상태(Status)",
     "위험 등급에 따라 자동 부여되는 처리 결과. 승인(approved) / 보류(held) / 차단(blocked)."],
    ["REST API",
     "HTTP 프로토콜 기반으로 자원을 URI로 표현하고 표준 메서드(GET·POST 등)로 조작하는 인터페이스."],
    ["대시보드",
     "관리자에게 거래 현황과 분석 결과를 한 화면에서 시각적으로 제공하는 웹 페이지."],
    ["SPA",
     "Single Page Application. 단일 HTML 문서 위에서 화면 전환이 이루어지는 웹 애플리케이션 구조."],
    ["CRC 카드",
     "Class-Responsibility-Collaborator 카드. 클래스의 책임과 협력자를 기술하는 객체지향 분석 도구."],
]
t = Table(wrap_grid(terms_data), colWidths=[3.5 * cm, 12.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("1.3 참조 문서", style_h2))
ref_data = [
    ["번호", "문서명", "비고"],
    ["[R-01]", "SafePay 시스템 구조 문서 (docs/system-structure.md)", "내부"],
    ["[R-02]", "SafePay README.md", "내부"],
    ["[R-03]", "ISO/IEC/IEEE 29148:2018 - Requirements engineering", "표준"],
    ["[R-04]", "OMG UML 2.5.1 Specification", "표준"],
    ["[R-05]", "OWASP Top 10 (2021)", "보안 가이드"],
    ["[R-06]", "개인정보 보호법 (법률 제19234호)", "법령"],
]
t = Table(wrap_grid(ref_data), colWidths=[2 * cm, 10 * cm, 4 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(PageBreak())

# =========================================================
# 2. 시스템 개요
# =========================================================
story.append(p("2. 시스템 개요", style_h1))

story.append(p("2.1 소프트웨어 컨텍스트(Context)", style_h2))

story.append(p("2.1.1 Actor Table", style_h3))
actor_data = [
    ["Actor", "Role"],
    ["관리자", "SafePay 대시보드를 통해 거래 현황을 모니터링하고 의심·차단 거래를 관리하는 사용자."],
    ["외부 쇼핑몰", "결제가 발생할 때마다 거래 데이터를 SafePay에 전송하는 외부 시스템 (REST API 클라이언트)."],
    ["시스템", "거래를 수집·분석하여 위험 점수를 산출하고 등급·상태를 자동 결정하는 SafePay 백엔드."],
]
t = Table(wrap_grid(actor_data), colWidths=[3 * cm, 13 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.4 * cm))

story.append(p("2.1.2 UseCase Diagram", style_h3))
story.append(draw_usecase_diagram())
story.append(p("[그림 2-1] SafePay UseCase Diagram", style_caption))

story.append(PageBreak())

# 2.2 기능 분류 및 설명 - UseCase Description 테이블
story.append(p("2.2 기능 분류 및 설명", style_h2))
story.append(p("2.2.1 UseCase Description", style_h3))

def usecase_table(name, uid, importance, primary_actor, uc_type,
                  brief, stakeholders, trigger,
                  relationships, normal_flow, subflows, alt_flow):
    raw = [
        ("Use Case Name", f"{name}    ID : {uid}    Importance Level : {importance}"),
        ("Primary Actor", primary_actor),
        ("Use Case Type", uc_type),
        ("Brief Description", brief),
        ("Stakeholders and Interests", stakeholders),
        ("Trigger", trigger),
        ("Relationships", relationships),
        ("Normal Flow of Events", normal_flow),
        ("Subflows", subflows),
        ("Alternate / Exceptional Flows", alt_flow),
    ]
    rows = [[WLL(label), WP(value)] for label, value in raw]
    t = Table(rows, colWidths=[4 * cm, 12 * cm])
    t.setStyle(make_usecase_table_style())
    return t

# U_01: 거래를 수집한다
story.append(usecase_table(
    "거래를 수집한다", "U_01", "high",
    "외부 쇼핑몰",
    "Detail, essential",
    "외부 쇼핑몰이 결제 정보를 SafePay 시스템에 전송하는 Use Case이다.",
    "외부 쇼핑몰: 결제가 발생할 때마다 SafePay에 데이터를 전송하여 사기 여부 판단을 요청한다.<br/>"
    "시스템: 거래 데이터를 수집하여 위험 분석을 위한 내부 저장소에 보관한다.",
    "외부 쇼핑몰이 POST /api/transactions 요청을 전송한다.",
    "Association : 외부 쇼핑몰<br/>"
    "Include : 사기 거래를 분류한다 (U_03)<br/>"
    "Extend : -<br/>"
    "Generalization : -",
    "1. 외부 쇼핑몰은 거래 정보(userId, amount, paymentMethod, ipAddress, location, purchasedAt)를 전송한다.<br/>"
    "2. 시스템은 거래 정보의 유효성을 확인한다.<br/>"
    "3. 시스템은 거래에 고유 ID(UUID)를 부여한다.<br/>"
    "4. 시스템은 위험 점수와 위험 등급을 산출한다 (U_03 include).<br/>"
    "5. 시스템은 거래를 저장소 최상단에 보관하고 201 Created 응답을 반환한다.",
    "-",
    "2.a1 : 필수 필드가 누락된 경우 시스템은 400 Bad Request를 반환한다.<br/>"
    "2.a2 : 요청 본문이 JSON 형식이 아닌 경우 시스템은 오류 응답을 반환한다.",
))
story.append(Spacer(1, 0.3 * cm))

# U_02: 위험 점수를 계산한다
story.append(usecase_table(
    "위험 점수를 계산한다", "U_02", "high",
    "시스템",
    "Detail, essential",
    "시스템이 거래의 사기 가능성을 0~100점의 위험 점수로 산출하는 Use Case이다.",
    "시스템: 결제 금액·결제수단·위치 정보를 기반으로 가산 점수를 부여하여 위험 점수를 계산한다.",
    "사기 거래 분류(U_03)에서 위험 점수 계산이 요청된 경우.",
    "Association : 시스템<br/>"
    "Include : -<br/>"
    "Extend : -<br/>"
    "Generalization : -",
    "1. 시스템은 기본 점수 10점을 부여한다.<br/>"
    "2. 결제 금액이 100,000원을 초과하면 35점을 가산한다.<br/>"
    "3. 결제 수단이 new-card이면 20점을 가산한다.<br/>"
    "4. 결제 위치가 unknown이면 20점을 가산한다.<br/>"
    "5. 최종 점수는 Math.min(score, 100)으로 상한을 둔다.",
    "-",
    "-",
))
story.append(Spacer(1, 0.3 * cm))

# U_03: 사기 거래를 분류한다
story.append(usecase_table(
    "사기 거래를 분류한다", "U_03", "high",
    "시스템",
    "Detail, essential",
    "산출된 위험 점수를 기준으로 거래를 정상·의심·위험 3단계로 분류하는 Use Case이다.",
    "시스템: 위험 점수를 위험 등급(normal / suspicious / danger)으로 매핑한다.<br/>"
    "관리자: 분류 결과를 통해 의심 거래를 인지한다.",
    "거래 수집(U_01) 시 위험 점수 계산(U_02)이 완료된 직후.",
    "Association : 시스템<br/>"
    "Include : 위험 점수를 계산한다 (U_02), 거래 상태를 결정한다 (U_04)<br/>"
    "Extend : -<br/>"
    "Generalization : -",
    "1. 시스템은 U_02를 호출하여 위험 점수를 획득한다.<br/>"
    "2. 점수가 80점 이상이면 위험 등급을 danger로 설정한다.<br/>"
    "3. 점수가 50점 이상 80점 미만이면 suspicious로 설정한다.<br/>"
    "4. 점수가 50점 미만이면 normal로 설정한다.<br/>"
    "5. 시스템은 U_04를 호출하여 거래 상태를 결정한다.",
    "-",
    "-",
))
story.append(Spacer(1, 0.3 * cm))
story.append(PageBreak())

# U_04: 거래 상태를 결정한다
story.append(usecase_table(
    "거래 상태를 결정한다", "U_04", "high",
    "시스템",
    "Detail, essential",
    "위험 등급을 거래 처리 상태(승인·보류·차단)로 매핑하는 Use Case이다.",
    "시스템: 위험 등급에 따라 거래의 자동 처리 결과를 결정한다.",
    "사기 거래 분류(U_03)에서 위험 등급이 확정된 직후.",
    "Association : 시스템<br/>"
    "Include : -<br/>"
    "Extend : -<br/>"
    "Generalization : -",
    "1. 위험 등급이 danger이면 상태를 blocked(차단)으로 설정한다.<br/>"
    "2. 위험 등급이 suspicious이면 상태를 held(보류)로 설정한다.<br/>"
    "3. 위험 등급이 normal이면 상태를 approved(승인)으로 설정한다.",
    "-",
    "-",
))
story.append(Spacer(1, 0.3 * cm))

# U_05: 거래 목록을 조회한다
story.append(usecase_table(
    "거래 목록을 조회한다", "U_05", "high",
    "관리자",
    "Detail, essential",
    "관리자가 수집·분류된 거래 전체 목록을 대시보드에서 조회하는 Use Case이다.",
    "관리자: 거래 현황을 모니터링하고 의심 거래를 식별하기를 원한다.",
    "관리자가 대시보드 페이지에 접근한다.",
    "Association : 관리자<br/>"
    "Include : 요약 통계를 확인한다 (U_08)<br/>"
    "Extend : -<br/>"
    "Generalization : -",
    "1. 관리자는 SafePay 대시보드 URL에 접속한다.<br/>"
    "2. 시스템은 GET /api/transactions를 호출한다.<br/>"
    "3. 시스템은 거래 목록을 시간 역순으로 응답한다.<br/>"
    "4. 시스템은 거래 ID·사용자·금액·결제수단·점수·등급·상태·구매시각을 표로 표시한다.<br/>"
    "5. 시스템은 요약 카드(실시간/의심/차단)에 통계를 표시한다.",
    "-",
    "2.a1 : API 호출 실패 시 시스템은 오류 메시지를 화면 상단에 빨간색으로 표시한다.<br/>"
    "2.a2 : 거래 데이터가 없는 경우 시스템은 \"거래 데이터가 없습니다.\" 안내를 표시한다.",
))
story.append(Spacer(1, 0.3 * cm))

# U_06: 위험 등급으로 필터링한다
story.append(usecase_table(
    "위험 등급으로 필터링한다", "U_06", "mid",
    "관리자",
    "Detail, essential",
    "관리자가 위험 등급을 기준으로 거래 목록을 필터링하여 조회하는 Use Case이다.",
    "관리자: 특정 위험 등급에 해당하는 거래만 집중적으로 확인하기를 원한다.",
    "관리자가 등급 선택 드롭다운(전체/정상/의심/위험)에서 항목을 선택한다.",
    "Association : 관리자<br/>"
    "Include : -<br/>"
    "Extend : 거래 목록을 조회한다 (U_05)<br/>"
    "Generalization : -",
    "1. 관리자는 필터 드롭다운에서 위험 등급을 선택한다.<br/>"
    "2. 시스템은 선택된 등급(all / normal / suspicious / danger)에 해당하는 거래만 필터링한다.<br/>"
    "3. 시스템은 필터링된 목록을 표에 다시 표시한다.",
    "-",
    "-",
))
story.append(Spacer(1, 0.3 * cm))
story.append(PageBreak())

# U_07: 대시보드를 새로고침한다
story.append(usecase_table(
    "대시보드를 새로고침한다", "U_07", "mid",
    "관리자",
    "Detail, essential",
    "관리자가 거래 데이터를 다시 불러와 대시보드를 최신 상태로 갱신하는 Use Case이다.",
    "관리자: 새로 발생한 거래를 즉시 확인하기를 원한다.",
    "관리자가 새로고침 버튼을 클릭한다.",
    "Association : 관리자<br/>"
    "Include : 거래 목록을 조회한다 (U_05)<br/>"
    "Extend : -<br/>"
    "Generalization : -",
    "1. 관리자는 \"새로고침\" 버튼을 클릭한다.<br/>"
    "2. 시스템은 로딩 상태로 전환하고 버튼을 비활성화한다.<br/>"
    "3. 시스템은 GET /api/transactions를 재호출한다.<br/>"
    "4. 시스템은 응답을 받아 상태를 갱신하고 로딩을 해제한다.",
    "-",
    "3.a1 : 호출 실패 시 시스템은 오류 메시지를 표시하고 로딩을 해제한다.",
))
story.append(Spacer(1, 0.3 * cm))

# U_08: 요약 통계를 확인한다
story.append(usecase_table(
    "요약 통계를 확인한다", "U_08", "high",
    "관리자",
    "Detail, essential",
    "실시간 거래·의심 거래·차단 거래 건수를 카드 형태로 한눈에 확인하는 Use Case이다.",
    "관리자: 거래 현황의 핵심 지표를 빠르게 파악하기를 원한다.",
    "관리자가 대시보드에 접근하거나 데이터가 갱신될 때.",
    "Association : 관리자<br/>"
    "Include : -<br/>"
    "Extend : 거래 목록을 조회한다 (U_05)<br/>"
    "Generalization : -",
    "1. 시스템은 거래 목록 전체 개수를 계산한다.<br/>"
    "2. 시스템은 status가 held인 거래 개수를 계산한다.<br/>"
    "3. 시스템은 status가 blocked인 거래 개수를 계산한다.<br/>"
    "4. 시스템은 RiskSummaryCard 3개에 각 수치를 표시한다.",
    "-",
    "-",
))
story.append(Spacer(1, 0.3 * cm))

# U_09: 오류 메시지를 표시한다
story.append(usecase_table(
    "오류 메시지를 표시한다", "U_09", "mid",
    "시스템",
    "Detail, essential",
    "API 호출 실패 시 관리자에게 오류 메시지를 화면에 표시하는 Use Case이다.",
    "관리자: 시스템 이상 상황을 인지하고 적절한 조치를 취하기를 원한다.<br/>"
    "시스템: 실패 원인을 명확히 전달한다.",
    "fetchTransactions() 호출이 실패 응답(또는 네트워크 오류)을 반환할 때.",
    "Association : 시스템<br/>"
    "Include : -<br/>"
    "Extend : 대시보드를 새로고침한다 (U_07), 거래 목록을 조회한다 (U_05)<br/>"
    "Generalization : -",
    "1. 시스템은 fetch 응답의 ok 필드를 확인한다.<br/>"
    "2. 응답이 실패면 \"거래 데이터를 불러오지 못했습니다.\" 메시지를 캐치한다.<br/>"
    "3. 시스템은 오류 메시지를 표 상단에 빨간색 강조 텍스트로 표시한다.",
    "-",
    "-",
))
story.append(PageBreak())

# =========================================================
# 3. 요구사항 명세
# =========================================================
story.append(p("3. 요구사항 명세", style_h1))

# 3.1 정적 분석
story.append(p("3.1 정적 분석", style_h2))
story.append(p(
    "SafePay의 객체 구조를 클래스 다이어그램으로 표현한다. "
    "백엔드는 Controller → Service → Service 계층으로 책임을 분리하며, "
    "프론트엔드는 Page → Component 구조로 UI를 구성한다."
))
story.append(draw_class_diagram())
story.append(p("[그림 3-1] SafePay Class Diagram", style_caption))
story.append(PageBreak())

# 3.2 CRC 카드
story.append(p("3.2 CRC 카드", style_h2))

def crc_card(name, cid, ctype, description, assoc_uc,
             responsibilities, collaborators, attributes,
             relationships):
    # 단일 테이블 + SPAN으로 head·body 세로선 정렬
    # 6 columns total = 16cm
    #   col 0: 라벨(3)
    #   col 1: 값(4)
    #   col 2: 라벨(1.5)
    #   col 3: 값(1.5)
    #   col 4: 라벨(1.5)
    #   col 5: 값(4.5)
    rows = [
        # row 0: 헤더 — Class Name / ID / Type
        [WLL("Class Name"), WP(name),
         WLL("ID"), WP(cid),
         WLL("Type"), WP(ctype)],
        # row 1: Description / Associated Use Case
        [WLL("Description"), WP(description), "",
         WLL("Associated Use Case"), "", WP(assoc_uc)],
        # row 2: Responsibilities / Collaborators
        [WLL("Responsibilities"), WP(responsibilities), "",
         WLL("Collaborators"), "", WP(collaborators)],
        # row 3: Attributes (전체 값 영역 SPAN)
        [WLL("Attributes"), WP(attributes), "", "", "", ""],
        # row 4: Relationships (전체 값 영역 SPAN)
        [WLL("Relationships"), WP(relationships), "", "", "", ""],
    ]
    t = Table(rows, colWidths=[3 * cm, 4 * cm, 1.5 * cm,
                               1.5 * cm, 1.5 * cm, 4.5 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("VALIGN", (0, 1), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#a0aec0")),
        # row 1 spans
        ("SPAN", (1, 1), (2, 1)),     # Description value
        ("SPAN", (3, 1), (4, 1)),     # Associated Use Case label
        # row 2 spans
        ("SPAN", (1, 2), (2, 2)),     # Responsibilities value
        ("SPAN", (3, 2), (4, 2)),     # Collaborators label
        # row 3, 4 full-width spans
        ("SPAN", (1, 3), (5, 3)),
        ("SPAN", (1, 4), (5, 4)),
        # 헤더 라벨 배경
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#edf2f7")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#edf2f7")),
        ("BACKGROUND", (4, 0), (4, 0), colors.HexColor("#edf2f7")),
        # 좌측 라벨 컬럼(Description ~ Relationships)
        ("BACKGROUND", (0, 1), (0, 4), colors.HexColor("#edf2f7")),
        # 우측 라벨(Associated Use Case / Collaborators)
        ("BACKGROUND", (3, 1), (4, 1), colors.HexColor("#edf2f7")),
        ("BACKGROUND", (3, 2), (4, 2), colors.HexColor("#edf2f7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return [t, Spacer(1, 0.3 * cm)]

# CRC 01: 관리자
for el in crc_card(
    "관리자", "01", "Concrete, Domain",
    "SafePay 대시보드를 사용하는 사용자.",
    "U_05, U_06, U_07, U_08",
    "- 거래 목록 조회 요청() : void<br/>"
    "- 위험 등급 필터 선택() : void<br/>"
    "- 대시보드 새로고침 요청() : void",
    "- DashboardPage<br/>- TransactionTable<br/>- RiskSummaryCard",
    "- 식별자 : String (향후 인증 도입 시)<br/>"
    "- 역할 : String",
    "- Generalization : -<br/>"
    "- Aggregation : -<br/>"
    "- Other Associations : DashboardPage",
):
    story.append(el)

# CRC 02: 외부 쇼핑몰
for el in crc_card(
    "외부 쇼핑몰", "02", "Concrete, Actor",
    "결제 발생 시 SafePay에 거래 데이터를 전송하는 외부 시스템.",
    "U_01",
    "- 거래 데이터 전송() : void",
    "- TransactionController",
    "- 가맹점 ID : String<br/>- API Key : String",
    "- Generalization : -<br/>"
    "- Aggregation : -<br/>"
    "- Other Associations : TransactionController",
):
    story.append(el)

# CRC 03: Transaction (Entity)
for el in crc_card(
    "Transaction", "03", "Entity, Domain",
    "수집된 단일 결제 거래의 도메인 모델.",
    "U_01, U_02, U_03, U_04",
    "- 거래 정보 보유<br/>"
    "- 위험 점수·등급·상태 보유",
    "- TransactionService<br/>- FraudDetectionService",
    "- id : string (UUID)<br/>"
    "- userId : string<br/>"
    "- amount : number<br/>"
    "- paymentMethod : string<br/>"
    "- ipAddress : string<br/>"
    "- location : string<br/>"
    "- purchasedAt : string (ISO8601)<br/>"
    "- riskScore : number (0~100)<br/>"
    "- riskLevel : RiskLevel<br/>"
    "- status : 'approved' | 'held' | 'blocked'",
    "- Generalization : -<br/>"
    "- Aggregation : RiskInfo (riskScore, riskLevel, status)<br/>"
    "- Other Associations : TransactionService",
):
    story.append(el)

story.append(PageBreak())

# CRC 04: RiskService
for el in crc_card(
    "RiskService", "04", "Concrete, Boundary",
    "거래에 대한 위험 점수를 산출하는 규칙 기반 서비스.",
    "U_02",
    "- calculateRiskScore(t) : number",
    "- FraudDetectionService<br/>- Transaction",
    "- BASE_SCORE : 10<br/>"
    "- AMOUNT_THRESHOLD : 100000<br/>"
    "- HIGH_AMOUNT_ADD : 35<br/>"
    "- NEW_CARD_ADD : 20<br/>"
    "- UNKNOWN_LOCATION_ADD : 20",
    "- Generalization : -<br/>"
    "- Aggregation : -<br/>"
    "- Other Associations : FraudDetectionService",
):
    story.append(el)

# CRC 05: FraudDetectionService
for el in crc_card(
    "FraudDetectionService", "05", "Concrete, Control",
    "위험 점수를 위험 등급으로 매핑하고 거래 상태를 결정하는 제어 클래스.",
    "U_03, U_04",
    "- classifyTransaction(payload) : Transaction<br/>"
    "- resolveRiskLevel(score) : RiskLevel",
    "- RiskService<br/>- Transaction<br/>- TransactionService",
    "- DANGER_THRESHOLD : 80<br/>"
    "- SUSPICIOUS_THRESHOLD : 50",
    "- Generalization : -<br/>"
    "- Aggregation : -<br/>"
    "- Other Associations : RiskService, TransactionService",
):
    story.append(el)

# CRC 06: TransactionService
for el in crc_card(
    "TransactionService", "06", "Concrete, Control",
    "거래의 수집·저장·조회를 책임지는 도메인 서비스.",
    "U_01, U_05",
    "- collectTransaction(input) : Transaction<br/>"
    "- listTransactions() : Transaction[]",
    "- FraudDetectionService<br/>- TransactionController",
    "- transactions : Transaction[]<br/>"
    "- seedInputs : TransactionInput[]",
    "- Generalization : -<br/>"
    "- Aggregation : Transaction[]<br/>"
    "- Other Associations : FraudDetectionService, TransactionController",
):
    story.append(el)

# CRC 07: TransactionController
for el in crc_card(
    "TransactionController", "07", "Concrete, Boundary",
    "REST API 요청을 처리하여 TransactionService로 위임하는 컨트롤러.",
    "U_01, U_05",
    "- collect(req, res) : void (POST /api/transactions)<br/>"
    "- list(req, res) : void (GET /api/transactions)",
    "- TransactionService<br/>- 외부 쇼핑몰<br/>- DashboardPage",
    "(상태 없음, 함수형 객체)",
    "- Generalization : -<br/>"
    "- Aggregation : -<br/>"
    "- Other Associations : TransactionService",
):
    story.append(el)

story.append(PageBreak())

# CRC 08: DashboardPage
for el in crc_card(
    "DashboardPage", "08", "Concrete, Boundary",
    "관리자 대시보드 페이지 컴포넌트. 거래 데이터 로딩과 상태 관리를 담당.",
    "U_05, U_06, U_07, U_08, U_09",
    "- loadTransactions() : void<br/>"
    "- handleRiskFilterChange(v) : void<br/>"
    "- render() : JSX",
    "- TransactionTable<br/>- RiskSummaryCard<br/>- api.fetchTransactions",
    "- transactions : Transaction[]<br/>"
    "- loading : boolean<br/>"
    "- error : string | null<br/>"
    "- riskFilter : 'all'|'normal'|'suspicious'|'danger'",
    "- Generalization : -<br/>"
    "- Aggregation : TransactionTable, RiskSummaryCard×3<br/>"
    "- Other Associations : api.ts",
):
    story.append(el)

# CRC 09: TransactionTable
for el in crc_card(
    "TransactionTable", "09", "Concrete, Boundary",
    "거래 목록을 표 형태로 표시하고 필터·새로고침 컨트롤을 제공하는 컴포넌트.",
    "U_05, U_06, U_07",
    "- onRefresh() : void<br/>"
    "- onRiskFilterChange(v) : void<br/>"
    "- render() : JSX",
    "- DashboardPage<br/>- Transaction",
    "- items : Transaction[]<br/>"
    "- riskFilter : RiskFilter<br/>"
    "- loading : boolean",
    "- Generalization : -<br/>"
    "- Aggregation : -<br/>"
    "- Other Associations : DashboardPage",
):
    story.append(el)

# CRC 10: RiskSummaryCard
for el in crc_card(
    "RiskSummaryCard", "10", "Concrete, Boundary",
    "실시간/의심/차단 거래 건수를 카드 형태로 표시하는 시각화 컴포넌트.",
    "U_08",
    "- render() : JSX",
    "- DashboardPage",
    "- title : string<br/>"
    "- value : string<br/>"
    "- tone : 'neutral'|'warning'|'danger'",
    "- Generalization : -<br/>"
    "- Aggregation : -<br/>"
    "- Other Associations : DashboardPage",
):
    story.append(el)

# CRC 11: ApiService
for el in crc_card(
    "ApiService (api.ts)", "11", "Concrete, Boundary",
    "프론트엔드가 백엔드 REST API를 호출하기 위한 단일 진입점.",
    "U_05, U_07, U_09",
    "- fetchTransactions() : Promise&lt;Transaction[]&gt;",
    "- DashboardPage<br/>- TransactionController",
    "- BASE_URL : string ('http://localhost:4000')",
    "- Generalization : -<br/>"
    "- Aggregation : -<br/>"
    "- Other Associations : DashboardPage, TransactionController",
):
    story.append(el)

story.append(PageBreak())

# 3.3 동적 분석
story.append(p("3.3 동적 분석", style_h2))
story.append(p(
    "각 Use Case의 객체 간 상호작용을 시퀀스 다이어그램으로 표현한다. "
    "Actor·Boundary·Control·Entity 간의 메시지 흐름과 반환 관계를 명세한다."
))

# 3.3.1 거래를 수집한다
story.append(p("3.3.1 거래를 수집한다", style_h3))
story.append(draw_sequence(
    "거래를 수집한다",
    [("외부 쇼핑몰", "actor"),
     ("Transaction Controller", "object"),
     ("Transaction Service", "object"),
     ("Fraud Detection Service", "object"),
     ("Risk Service", "object")],
    [
        (0, 1, "POST /api/transactions", "sync"),
        (1, 2, "collectTransaction(input)", "sync"),
        (2, 3, "classifyTransaction(payload)", "sync"),
        (3, 4, "calculateRiskScore(t)", "sync"),
        (4, 3, "score", "return"),
        (3, 2, "Transaction", "return"),
        (2, 1, "Transaction", "return"),
        (1, 0, "201 Created", "return"),
    ],
))
story.append(p("[그림 3-2] 거래 수집 Sequence Diagram", style_caption))

# 3.3.2 위험 점수를 계산한다
story.append(p("3.3.2 위험 점수를 계산한다", style_h3))
story.append(draw_sequence(
    "위험 점수를 계산한다",
    [("Fraud Detection Service", "object"),
     ("Risk Service", "object")],
    [
        (0, 1, "calculateRiskScore(t)", "sync"),
        (1, 1, "score = 10 (기본)", "sync"),
        (1, 1, "if amount > 100000 → +35", "sync"),
        (1, 1, "if new-card → +20", "sync"),
        (1, 1, "if unknown → +20", "sync"),
        (1, 0, "Math.min(score, 100)", "return"),
    ],
))
story.append(p("[그림 3-3] 위험 점수 계산 Sequence Diagram", style_caption))
story.append(PageBreak())

# 3.3.3 사기 거래를 분류한다 + 3.3.4 거래 상태 결정
story.append(p("3.3.3 사기 거래를 분류한다 / 3.3.4 거래 상태를 결정한다", style_h3))
story.append(draw_sequence(
    "사기 거래 분류 및 상태 결정",
    [("Transaction Service", "object"),
     ("Fraud Detection Service", "object"),
     ("Risk Service", "object")],
    [
        (0, 1, "classifyTransaction(payload)", "sync"),
        (1, 2, "calculateRiskScore(t)", "sync"),
        (2, 1, "score", "return"),
        (1, 1, "resolveRiskLevel(score)", "sync"),
        (1, 1, "score>=80 → danger / blocked", "sync"),
        (1, 1, "score>=50 → suspicious / held", "sync"),
        (1, 1, "else → normal / approved", "sync"),
        (1, 0, "Transaction(id, level, status)", "return"),
    ],
))
story.append(p("[그림 3-4] 사기 분류 및 상태 결정 Sequence Diagram", style_caption))

# 3.3.5 거래 목록을 조회한다
story.append(p("3.3.5 거래 목록을 조회한다", style_h3))
story.append(draw_sequence(
    "거래 목록을 조회한다",
    [("관리자", "actor"),
     ("DashboardPage", "object"),
     ("api.ts", "object"),
     ("Tx Controller", "object"),
     ("Tx Service", "object")],
    [
        (0, 1, "대시보드 접근", "sync"),
        (1, 2, "fetchTransactions()", "sync"),
        (2, 3, "GET /api/transactions", "sync"),
        (3, 4, "listTransactions()", "sync"),
        (4, 3, "Transaction[]", "return"),
        (3, 2, "200 OK + JSON", "return"),
        (2, 1, "Transaction[]", "return"),
        (1, 0, "표·요약 카드 렌더링", "return"),
    ],
))
story.append(p("[그림 3-5] 거래 목록 조회 Sequence Diagram", style_caption))
story.append(PageBreak())

# 3.3.6 위험 등급으로 필터링한다
story.append(p("3.3.6 위험 등급으로 필터링한다", style_h3))
story.append(draw_sequence(
    "위험 등급으로 필터링한다",
    [("관리자", "actor"),
     ("TransactionTable", "object"),
     ("DashboardPage", "object")],
    [
        (0, 1, "filter 드롭다운 선택(v)", "sync"),
        (1, 2, "onRiskFilterChange(v)", "sync"),
        (2, 2, "setRiskFilter(v)", "sync"),
        (2, 2, "useMemo 재계산", "sync"),
        (2, 1, "filteredItems[]", "return"),
        (1, 0, "표 재렌더링", "return"),
    ],
))
story.append(p("[그림 3-6] 위험 등급 필터링 Sequence Diagram", style_caption))

# 3.3.7 대시보드를 새로고침한다
story.append(p("3.3.7 대시보드를 새로고침한다", style_h3))
story.append(draw_sequence(
    "대시보드를 새로고침한다",
    [("관리자", "actor"),
     ("TransactionTable", "object"),
     ("DashboardPage", "object"),
     ("api.ts", "object")],
    [
        (0, 1, "새로고침 버튼 클릭", "sync"),
        (1, 2, "onRefresh()", "sync"),
        (2, 2, "setLoading(true)", "sync"),
        (2, 3, "fetchTransactions()", "sync"),
        (3, 2, "Transaction[]", "return"),
        (2, 2, "setTransactions(...)", "sync"),
        (2, 1, "새 데이터 props", "return"),
        (1, 0, "갱신된 표 표시", "return"),
    ],
))
story.append(p("[그림 3-7] 대시보드 새로고침 Sequence Diagram", style_caption))
story.append(PageBreak())

# 3.3.8 요약 통계를 확인한다
story.append(p("3.3.8 요약 통계를 확인한다", style_h3))
story.append(draw_sequence(
    "요약 통계를 확인한다",
    [("관리자", "actor"),
     ("DashboardPage", "object"),
     ("RiskSummaryCard ×3", "object")],
    [
        (0, 1, "대시보드 진입 / 데이터 갱신", "sync"),
        (1, 1, "total = transactions.length", "sync"),
        (1, 1, "held = filter(status='held')", "sync"),
        (1, 1, "blocked = filter(status='blocked')", "sync"),
        (1, 2, "render(실시간, 의심, 차단)", "sync"),
        (2, 0, "3개 카드 표시", "return"),
    ],
))
story.append(p("[그림 3-8] 요약 통계 Sequence Diagram", style_caption))

# 3.3.9 오류 메시지를 표시한다
story.append(p("3.3.9 오류 메시지를 표시한다", style_h3))
story.append(draw_sequence(
    "오류 메시지를 표시한다",
    [("DashboardPage", "object"),
     ("api.ts", "object"),
     ("관리자", "actor")],
    [
        (0, 1, "fetchTransactions()", "sync"),
        (1, 1, "fetch() 실패 또는 !res.ok", "sync"),
        (1, 0, "throw Error(\"...불러오지 못했습니다\")", "return"),
        (0, 0, "setError(message)", "sync"),
        (0, 2, "오류 메시지 빨간색 표시", "sync"),
    ],
))
story.append(p("[그림 3-9] 오류 메시지 표시 Sequence Diagram", style_caption))
story.append(PageBreak())

# =========================================================
# 4. 인터페이스 분석
# =========================================================
story.append(p("4. 인터페이스 분석", style_h1))

story.append(p("4.1 사용자 인터페이스 (UI)", style_h2))
ui_data = [
    ["화면 / 요소", "구성요소", "주요 입력 / 출력"],
    ["대시보드 페이지\n(DashboardPage)",
     "히어로 헤더, 요약 영역, 거래 목록 영역",
     "출력: 페이지 타이틀·설명문 / 입력: 페이지 진입(자동 로드)"],
    ["요약 카드\n(RiskSummaryCard ×3)",
     "실시간 거래·의심 거래·차단 거래 카드",
     "출력: 거래 건수, tone(neutral·warning·danger) 색상 강조"],
    ["거래 목록 테이블\n(TransactionTable)",
     "헤더(거래ID·사용자·금액·결제수단·점수·등급·상태·구매시각), 데이터 행",
     "출력: 거래 행, 한글 라벨 + 색상 뱃지(정상/의심/위험, 승인/보류/차단)"],
    ["위험 등급 필터\n(select 드롭다운)",
     "전체 등급 / 정상 / 의심 / 위험",
     "입력: 사용자 선택 / 출력: 필터링된 거래 목록"],
    ["새로고침 버튼",
     "텍스트 버튼 (\"새로고침\" / \"불러오는 중...\")",
     "입력: 클릭 / 출력: 거래 데이터 재요청, 로딩 상태 토글"],
    ["오류 메시지 영역",
     "빨간색 강조 텍스트(\".error-message\")",
     "출력: API 오류 발생 시 사용자에게 메시지 표시"],
]
t = Table(wrap_grid(ui_data), colWidths=[4 * cm, 5 * cm, 7 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("4.2 시스템 간 연계 (외부 인터페이스)", style_h2))
ext_data = [
    ["연계 시스템", "방향", "프로토콜", "용도"],
    ["외부 쇼핑몰", "→ SafePay", "HTTP / REST / JSON",
     "결제 발생 시 거래 데이터 전송 (POST /api/transactions)"],
    ["프론트엔드 (브라우저)", "→ SafePay 백엔드", "HTTP / REST / JSON",
     "거래 목록 조회 (GET /api/transactions), CORS 허용"],
    ["헬스체크", "→ SafePay 백엔드", "HTTP / GET",
     "/health 응답으로 서버 상태 확인"],
]
t = Table(wrap_grid(ext_data), colWidths=[4 * cm, 2.5 * cm, 3.5 * cm, 6 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("4.3 입력 / 출력 인터페이스 (API 명세)", style_h2))

story.append(p("4.3.1 POST /api/transactions (거래 수집)", style_h3))
api1 = [
    ["구분", "내용"],
    ["URL", "POST /api/transactions"],
    ["요청 헤더", "Content-Type: application/json"],
    ["요청 본문 (입력)",
     "{ userId: string, amount: number, paymentMethod: string,\n"
     "  ipAddress: string, location: string, purchasedAt: string (ISO8601) }"],
    ["응답 코드", "201 Created (성공) / 400 Bad Request (필드 누락 등)"],
    ["응답 본문 (출력)",
     "Transaction 객체 (id, userId, amount, paymentMethod, ipAddress,\n"
     "  location, purchasedAt, riskScore, riskLevel, status)"],
]
t = Table(wrap_grid(api1), colWidths=[3 * cm, 13 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("4.3.2 GET /api/transactions (거래 목록 조회)", style_h3))
api2 = [
    ["구분", "내용"],
    ["URL", "GET /api/transactions"],
    ["요청 헤더", "(없음, CORS 허용)"],
    ["요청 파라미터 (입력)", "(없음)"],
    ["응답 코드", "200 OK"],
    ["응답 본문 (출력)",
     "Transaction[] 배열, 최신 거래가 배열의 앞쪽(시간 역순)에 위치"],
]
t = Table(wrap_grid(api2), colWidths=[3 * cm, 13 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("4.3.3 GET /health (헬스체크)", style_h3))
api3 = [
    ["구분", "내용"],
    ["URL", "GET /health"],
    ["응답 코드", "200 OK"],
    ["응답 본문 (출력)", "{ \"status\": \"ok\" }"],
]
t = Table(wrap_grid(api3), colWidths=[3 * cm, 13 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(PageBreak())

# =========================================================
# 5. 제약사항
# =========================================================
story.append(p("5. 제약사항", style_h1))

story.append(p("5.1 기술적 제약사항", style_h2))
tech_data = [
    ["분류", "내용"],
    ["CT-T-001", "백엔드는 Node.js LTS(20.x 이상) 및 Express + TypeScript 환경에서 동작해야 한다."],
    ["CT-T-002", "프론트엔드는 React 18 이상 + Vite 5 이상의 환경을 전제로 한다."],
    ["CT-T-003", "거래 데이터는 인메모리 배열에 보관하며, 본 단계에서는 영구 DB를 도입하지 않는다."],
    ["CT-T-004", "위험 점수 산출은 규칙 기반(rule-based)이며, 머신러닝 모델은 본 단계의 범위에서 제외한다."],
    ["CT-T-005", "프론트엔드와 백엔드는 CORS가 허용된 별도 포트(기본 5173 / 4000)에서 구동된다."],
    ["CT-T-006", "응답 JSON은 카멜케이스(camelCase) 키 표기를 따른다."],
    ["CT-T-007", "모든 텍스트 응답은 UTF-8 인코딩을 기준으로 한다."],
]
t = Table(wrap_grid(tech_data), colWidths=[2.5 * cm, 13.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("5.2 운영적 제약사항", style_h2))
ops_data = [
    ["분류", "내용"],
    ["CT-O-001", "본 프로젝트는 학습/시연 목적의 골격 프로젝트로, 운영 환경 배포는 별도 후속 단계에서 다룬다."],
    ["CT-O-002", "사용자 인증(로그인)·권한 관리(RBAC)는 본 버전에서 구현하지 않는다."],
    ["CT-O-003", "외부 결제 게이트웨이(PG, 카드사) 직접 연동은 본 문서의 범위에 포함되지 않는다."],
    ["CT-O-004", "서버 재시작 시 사용자 입력 거래는 소실되며, 시드 거래(8건)만 유지된다."],
    ["CT-O-005", "장애 시 1차 분석은 콘솔 로그를 기준으로 한다. 외부 로깅 시스템은 향후 과제."],
    ["CT-O-006", "관리자 화면은 데스크톱 해상도(1280×720 이상)를 기본 타깃으로 한다."],
    ["CT-O-007", "다국어 지원은 본 버전에서 제공하지 않으며, 한국어를 기본 언어로 한다."],
]
t = Table(wrap_grid(ops_data), colWidths=[2.5 * cm, 13.5 * cm])
t.setStyle(make_table_style())
story.append(t)
story.append(PageBreak())

# =========================================================
# 6. 요구사항 추적표
# =========================================================
story.append(p("6. 요구사항 추적표", style_h1))
story.append(p(
    "기능 요구사항(FR)·비기능 요구사항(NFR)·인터페이스 요구사항(IFR)이 Use Case와 어떻게 "
    "연결되는지를 추적성 매트릭스로 표현한다. \"○\" 표시는 해당 요구사항이 해당 Use Case에 "
    "의해 실현됨을 의미한다."
))
story.append(Spacer(1, 0.3 * cm))

uc_ids = ["U_01", "U_02", "U_03", "U_04", "U_05", "U_06", "U_07", "U_08", "U_09"]

req_list = [
    # (id, description, matrix row of marks for each uc_id)
    ("FR_001", "거래 수집 API 수신",          [1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_002", "거래 UUID 부여",              [1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_003", "거래 필수 필드 검증",         [1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_004", "거래 시간 역순 보관",         [1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_005", "기본 점수 10점 부여",         [0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_006", "고액(>10만원) +35점",         [0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_007", "new-card +20점",              [0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_008", "unknown 위치 +20점",          [0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_009", "점수 0~100 정수 산출",        [0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("FR_010", "80점 이상 → danger",          [0, 0, 1, 0, 0, 0, 0, 0, 0]),
    ("FR_011", "50~79점 → suspicious",        [0, 0, 1, 0, 0, 0, 0, 0, 0]),
    ("FR_012", "50점 미만 → normal",          [0, 0, 1, 0, 0, 0, 0, 0, 0]),
    ("FR_013", "danger → blocked 자동 설정",  [0, 0, 0, 1, 0, 0, 0, 0, 0]),
    ("FR_014", "suspicious → held 자동 설정", [0, 0, 0, 1, 0, 0, 0, 0, 0]),
    ("FR_015", "normal → approved 자동 설정", [0, 0, 0, 1, 0, 0, 0, 0, 0]),
    ("FR_016", "거래 목록 조회 API",          [0, 0, 0, 0, 1, 0, 0, 0, 0]),
    ("FR_017", "거래 응답 필드 명세",         [0, 0, 0, 0, 1, 0, 0, 0, 0]),
    ("FR_018", "대시보드 표 형태 표시",       [0, 0, 0, 0, 1, 0, 0, 0, 0]),
    ("FR_019", "위험 등급 필터링",            [0, 0, 0, 0, 0, 1, 0, 0, 0]),
    ("FR_020", "수동 새로고침",               [0, 0, 0, 0, 0, 0, 1, 0, 0]),
    ("FR_021", "요약 카드(실시간/의심/차단)", [0, 0, 0, 0, 0, 0, 0, 1, 0]),
    ("FR_022", "로딩 상태 표시",              [0, 0, 0, 0, 1, 0, 1, 1, 0]),
    ("FR_023", "API 오류 메시지 표시",        [0, 0, 0, 0, 0, 0, 0, 0, 1]),
    ("FR_024", "한글 라벨 + 색상 뱃지",       [0, 0, 0, 0, 1, 0, 0, 0, 0]),
    ("NFR_01", "점수 산출 100ms 이내",        [0, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("NFR_02", "조회 API 응답 1초 이내",      [0, 0, 0, 0, 1, 0, 1, 0, 0]),
    ("NFR_03", "대시보드 초기 로딩 3초",      [0, 0, 0, 0, 1, 0, 0, 1, 0]),
    ("NFR_04", "민감정보 외부 노출 방지",     [1, 0, 0, 0, 1, 0, 0, 0, 0]),
    ("IFR_01", "POST /api/transactions 명세", [1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("IFR_02", "GET /api/transactions 명세",  [0, 0, 0, 0, 1, 0, 1, 0, 0]),
    ("IFR_03", "성공 응답 코드(201/200)",     [1, 0, 0, 0, 1, 0, 0, 0, 0]),
    ("IFR_04", "프론트→백엔드 api.ts 경유",   [0, 0, 0, 0, 1, 0, 1, 0, 1]),
]

# build matrix table
trace_cell_normal = ParagraphStyle(
    "trace_normal", parent=cell_normal, fontSize=8.5, leading=11)
trace_cell_label = ParagraphStyle(
    "trace_label", parent=cell_label, fontSize=8.5, leading=11)
trace_cell_desc = ParagraphStyle(
    "trace_desc", parent=cell_normal, fontSize=8.5, leading=11)
trace_cell_mark = ParagraphStyle(
    "trace_mark", parent=cell_center, fontSize=8.5, leading=11)
trace_cell_header = ParagraphStyle(
    "trace_header", parent=cell_header, fontSize=8.5, leading=11)

def TH(text):
    return WP(text, trace_cell_header)
def TL(text):
    return WP(text, trace_cell_label)
def TD(text):
    return WP(text, trace_cell_desc)
def TM(text):
    return WP(text, trace_cell_mark)

header_row = [TH("분류"), TH("요구사항")] + [TH(u) for u in uc_ids]
body_rows = []
for rid, desc, marks in req_list:
    row = [TL(rid), TD(desc)] + [TM("○" if m else "") for m in marks]
    body_rows.append(row)
trace_table_data = [header_row] + body_rows

col_widths = [1.8 * cm, 5.5 * cm] + [0.9 * cm] * len(uc_ids)
t = Table(trace_table_data, colWidths=col_widths, repeatRows=1)
trace_style = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#a0aec0")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.white, colors.HexColor("#f7fafc")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
])
t.setStyle(trace_style)
story.append(t)
story.append(PageBreak())

# =========================================================
# 7. 참고문헌 및 부록
# =========================================================
story.append(p("7. 참고문헌 및 부록", style_h1))

story.append(p("7.1 참고 자료", style_h2))
story.append(p(
    "[1] IEEE Std 29148-2018, Systems and software engineering — Life cycle processes — Requirements engineering, IEEE, 2018.<br/>"
    "[2] OMG Unified Modeling Language Specification, version 2.5.1, https://www.omg.org/spec/UML/2.5.1/<br/>"
    "[3] OWASP Foundation, OWASP Top 10 - 2021, https://owasp.org/Top10/<br/>"
    "[4] Mozilla Developer Network, REST API 가이드, https://developer.mozilla.org/<br/>"
    "[5] Express.js 공식 문서, https://expressjs.com/<br/>"
    "[6] React 공식 문서, https://react.dev/<br/>"
    "[7] Vite 공식 문서, https://vitejs.dev/<br/>"
    "[8] TypeScript 공식 핸드북, https://www.typescriptlang.org/docs/<br/>"
    "[9] 개인정보 보호법(법률 제19234호), 국가법령정보센터, https://www.law.go.kr/<br/>"
    "[10] Bittner & Spence, \"Use Case Modeling\", Addison-Wesley, 2003."
))

story.append(p("7.2 부록 A. 위험 점수 계산 규칙", style_h2))
score_rule = [
    ["조건", "가산 점수", "비고"],
    ["기본 점수", "+10", "모든 거래에 부여"],
    ["결제 금액 > 100,000원", "+35", "고액 거래"],
    ["결제 수단 = new-card", "+20", "신규 등록 카드"],
    ["결제 위치 = unknown", "+20", "위치 식별 불가"],
    ["최종 점수 상한", "100", "Math.min(score, 100)"],
]
t = Table(wrap_grid(score_rule), colWidths=[7 * cm, 3 * cm, 6 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("7.3 부록 B. 위험 등급 임계값", style_h2))
level_rule = [
    ["위험 점수 범위", "위험 등급", "거래 상태", "UI 라벨"],
    ["80점 이상", "danger", "blocked", "위험 / 차단"],
    ["50점 이상 ~ 80점 미만", "suspicious", "held", "의심 / 보류"],
    ["50점 미만", "normal", "approved", "정상 / 승인"],
]
t = Table(wrap_grid(level_rule), colWidths=[5 * cm, 3 * cm, 3 * cm, 5 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("7.4 부록 C. 데이터 모델 (Transaction)", style_h2))
data_model = [
    ["필드명", "타입", "설명"],
    ["id", "string (UUID)", "거래 고유 식별자"],
    ["userId", "string", "결제를 수행한 사용자 ID"],
    ["amount", "number", "결제 금액 (원화)"],
    ["paymentMethod", "string", "결제 수단 (card / new-card 등)"],
    ["ipAddress", "string", "결제 발생 IP 주소"],
    ["location", "string", "결제 위치 (도시 또는 unknown)"],
    ["purchasedAt", "string (ISO8601)", "결제 발생 일시"],
    ["riskScore", "number (0~100)", "산출된 위험 점수"],
    ["riskLevel", "RiskLevel", "normal / suspicious / danger"],
    ["status", "string", "approved / held / blocked"],
]
t = Table(wrap_grid(data_model), colWidths=[3.5 * cm, 4 * cm, 8.5 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

story.append(p("7.5 부록 D. 변경 이력", style_h2))
history = [
    ["버전", "일자", "작성자", "내용"],
    ["v1.0", "2026-05-18", "박정호 (RovermanDP)",
     "초안 작성 (요구사항 분석서 7-section 양식)"],
]
t = Table(wrap_grid(history), colWidths=[2 * cm, 3 * cm, 4 * cm, 7 * cm])
t.setStyle(make_table_style(header_bg="#2b6cb0"))
story.append(t)

# ---------------- PDF 생성 ----------------
doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm,
    title="SafePay 요구사항 분석서",
    author="박정호 (RovermanDP)",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF generated: {OUTPUT_PATH}")
print(f"Size: {os.path.getsize(OUTPUT_PATH)} bytes")
