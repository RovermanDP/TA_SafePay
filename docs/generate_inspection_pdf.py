# -*- coding: utf-8 -*-
"""SafePay 인스팩션 수행 결과 보고서 PDF 생성 스크립트"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)

pdfmetrics.registerFont(TTFont("Malgun", "C:/Windows/Fonts/malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", "C:/Windows/Fonts/malgunbd.ttf"))

OUTPUT_PATH = r"C:/Users/bagje/Desktop/SafePay_인스팩션수행결과보고서.pdf"

styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "title", parent=styles["Title"], fontName="MalgunBold",
    fontSize=20, leading=26, alignment=TA_CENTER, spaceAfter=14,
)
style_section = ParagraphStyle(
    "section", parent=styles["Heading2"], fontName="MalgunBold",
    fontSize=13, leading=18, spaceBefore=12, spaceAfter=6,
    textColor=colors.HexColor("#1a3a6c"),
)
style_body = ParagraphStyle(
    "body", parent=styles["Normal"], fontName="Malgun",
    fontSize=10, leading=15, alignment=TA_LEFT,
)
style_cell = ParagraphStyle(
    "cell", fontName="Malgun", fontSize=9, leading=12, alignment=TA_LEFT,
)
style_cell_c = ParagraphStyle(
    "cell_c", fontName="Malgun", fontSize=9, leading=12, alignment=TA_CENTER,
)
style_cell_b = ParagraphStyle(
    "cell_b", fontName="MalgunBold", fontSize=9, leading=12, alignment=TA_CENTER,
)
style_cell_h = ParagraphStyle(
    "cell_h", fontName="MalgunBold", fontSize=9.5, leading=12,
    alignment=TA_CENTER, textColor=colors.black,
)


def P(text, st=style_body):
    return Paragraph(text, st)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Malgun", 9)
    canvas.setFillColor(colors.black)
    canvas.drawCentredString(A4[0] / 2.0, 1.2 * cm, f"- {doc.page} -")
    canvas.restoreState()


# ---------------- Header / Cover ----------------
story = []
story.append(P("Team Project Peer Review Form", style_title))
story.append(Spacer(1, 0.2 * cm))

# ---------------- Team / Project Info ----------------
team_info = [
    [P("Team Name<br/>of Reviewer", style_cell_h),
     P("SafePay (검토팀)", style_cell_c),
     P("Team Name<br/>to be reviewed", style_cell_h),
     P("SafePay (피검토팀)", style_cell_c)],
    [P("Project Name", style_cell_h),
     P("SafePay - 온라인 쇼핑 사기 탐지 시스템", style_cell_c), "", ""],
    [P("Project Phase", style_cell_h),
     P("Design Phase", style_cell_c),
     P("Meeting Type", style_cell_h),
     P("Inspection", style_cell_c)],
    [P("Doc. ID. Number", style_cell_h),
     P("2026-SafePay-Design-Doc", style_cell_c),
     P("Doc. Size", style_cell_h),
     P("38 Pages / Loc", style_cell_c)],
    [P("Meeting Date", style_cell_h),
     P("2026.05.18", style_cell_c),
     P("Meeting Place", style_cell_h),
     P("과학관 209호", style_cell_c)],
]
t = Table(team_info, colWidths=[3.2 * cm, 5.3 * cm, 3.2 * cm, 5.3 * cm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#bee3f8")),
    ("SPAN", (1, 1), (3, 1)),
    ("BACKGROUND", (1, 1), (3, 1), colors.white),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)

# ---------------- Participants ----------------
part_data = [
    [P("Participants", style_cell_h),
     P("Name", style_cell_h),
     P("Affiliation (Team Name)", style_cell_h),
     P("Role", style_cell_h),
     P("Signature", style_cell_h)],
    ["", P("박정호", style_cell_c), P("SafePay", style_cell_c),
     P("Moderator / 팀장", style_cell_c), ""],
    ["", P("홍길동", style_cell_c), P("SafePay", style_cell_c),
     P("Author / 설계자", style_cell_c), ""],
    ["", P("김용길", style_cell_c), P("SafePay", style_cell_c),
     P("Reviewer / 검토자", style_cell_c), ""],
    ["", P("정약용", style_cell_c), P("SafePay", style_cell_c),
     P("Scribe / 서기", style_cell_c), ""],
]
t = Table(part_data, colWidths=[3.2 * cm, 2.5 * cm, 4.2 * cm, 3.3 * cm, 3.8 * cm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#bee3f8")),
    ("SPAN", (0, 1), (0, 4)),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

# ---------------- Meeting Preparation Checklist ----------------
story.append(P("▶ Meeting Preparation Checklist", style_section))
chk_rows = [
    [P("Check Items", style_cell_h), P("Yes / No", style_cell_h),
     P("Remark", style_cell_h)],
    [P("검토 대상 문서가 충분히 준비 되었는가 ?", style_cell),
     P("YES", style_cell_c), P("설계서, 요구사항 정의서, 분석서 모두 배포", style_cell)],
    [P("문서의 구성과 내용이 적절한가 ? (누락된 것이 있는가 ?)", style_cell),
     P("NO", style_cell_c), P("일부 모듈/메소드 상세 설명 누락 발견", style_cell)],
    [P("문서의 변경 관리가 이루어졌는가 ? (최종버전인가 ?)", style_cell),
     P("YES", style_cell_c), P("v1.0 최종본 기준 검토", style_cell)],
    [P("문서 페이지 번호가 있는가 ?", style_cell),
     P("YES", style_cell_c), ""],
    [P("문서 오타 점검이 이루어졌는가 ?", style_cell),
     P("NO", style_cell_c), P("Typo 다수 발견됨", style_cell)],
    [P("설계 산출물과 구현 코드 간 일관성이 검토되었는가 ?", style_cell),
     P("NO", style_cell_c), P("인터페이스/시그니처 불일치 발견", style_cell)],
]
t = Table(chk_rows, colWidths=[8.5 * cm, 2 * cm, 6.5 * cm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#bee3f8")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

# ---------------- Meeting Information ----------------
story.append(P("▶ Meeting Information", style_section))
mi_rows = [
    [P("Meeting Start Date", style_cell_h),
     P("2026.05.11", style_cell_c),
     P("Meeting End Date", style_cell_h),
     P("2026.05.18", style_cell_c)],
    [P("Number of People<br/>at Meeting", style_cell_h),
     P("4 명", style_cell_c),
     P("Elapsed Time for<br/>Decision Making", style_cell_h),
     P("8 hours", style_cell_c)],
]
t = Table(mi_rows, colWidths=[4 * cm, 4.5 * cm, 4 * cm, 4.5 * cm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#bee3f8")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

# ---------------- Final Meeting Result ----------------
story.append(P("▶ Final Meeting Result", style_section))
fr_rows = [
    [P("Disposition", style_cell_h),
     P("Accept&nbsp;&nbsp;/&nbsp;&nbsp;<b>Conditionally accept</b>&nbsp;&nbsp;/&nbsp;&nbsp;Re-submit&nbsp;&nbsp;/&nbsp;&nbsp;TBD",
       style_cell_c)],
    [P("Supporting Information<br/>or Comments", style_cell_h),
     P(
         "<b>Conditionally accept</b><br/><br/>"
         "1) 다수의 Omission(설명 누락) 및 Typo가 발견되어 설계 산출물 보완이 필요함.<br/>"
         "2) 설계서의 시그니처/식별자와 실제 구현 코드 간 불일치(Incorrect, Interface Error)가 다수 확인됨.<br/>"
         "3) 일부 흐름(예외 처리, 입력 검증)이 누락되어 신뢰성 측면 보강이 요구되나, 핵심 기능 흐름은 정상이므로 "
         "지적된 결함을 반영하는 조건으로 산출물을 승인하기로 결정함.", style_cell)],
]
t = Table(fr_rows, colWidths=[4 * cm, 13 * cm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#bee3f8")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)

story.append(PageBreak())

# ---------------- Findings Definition ----------------
# Findings list: (location, description, severity, fault_type)
# severity = "Major" or "Minor"
findings = [
    # 요구사항/설계 일반 - Typo & Clarification
    ("설계서-1p", "표지 작성일이 '2026-05-18'로 표기되어 미래 일자가 기록됨 (오타 의심)", "Minor", "TY"),
    ("설계서-2p", "참조 문서 [R-05] ISO/IEC/IEEE 42010 표준 인용에 대해 구체적 절(Clause) 명시가 없어 모호함", "Minor", "CL"),
    ("설계서-2p", "용어 정의표에 'IP', 'UUID' 등 약어에 대한 정의 누락", "Minor", "OM"),
    ("설계서-3p", "1.2 용어 정의 항목의 'SPA' 정의에서 'Single Page Application' 외 React/Vite 등 사용 기술과의 관계 설명이 누락됨", "Minor", "OM"),
    # 아키텍처
    ("설계서-4p", "2.1 정적 구조도에서 backend 패키지에 errorMiddleware, routes 컴포넌트가 누락됨", "Major", "OM"),
    ("설계서-4p", "2.1 정적 구조 설명에서 'Controller → Service → Model' 흐름이라고 기술되었으나 실제 코드에는 Model이 데이터 클래스가 아닌 TypeScript 인터페이스로만 존재하므로 표현 일관성 부족", "Minor", "CS"),
    ("설계서-5p", "2.2 동적 구조 시퀀스 다이어그램에서 errorMiddleware로의 예외 분기 흐름이 표현되지 않음", "Major", "LO"),
    ("설계서-5p", "거래 수집 시퀀스 다이어그램에서 응답 코드 '201 Created' 외 실패 응답(400, 500)에 대한 흐름이 누락됨", "Major", "EH"),
    ("설계서-5p", "거래 목록 조회 시퀀스에서 ApiClient의 fetch 실패 시 흐름(예외 경로) 누락", "Minor", "EH"),
    # 모듈 설계
    ("설계서-6p", "3.1.1 Transaction 패키지 설명에서 routes/transaction.routes.ts 구성 요소 누락", "Major", "OM"),
    ("설계서-6p", "CM-001 TransactionController '관련 Use Case'에 U_01, U_02 표기되었으나 요구사항 정의서에는 U_01만 거래 수집을 정의하므로 추적성 오류", "Major", "TR"),
    ("설계서-7p", "CM-001 TransactionController.list() 메소드 파라미터 'req(Request)'로 기술되어 있으나 실제 구현은 사용하지 않는 '_req' (underscore prefix) — 시그니처 불일치", "Minor", "IC"),
    ("설계서-7p", "CM-002 TransactionService 멤버 변수 'transactions: Transaction[] (메모리 저장소)'가 module-level let 변수로 구현되어 클래스 멤버가 아님 — 설계와 구현 불일치", "Major", "IC"),
    ("설계서-7p", "CM-002 TransactionService 멤버 변수에 'seedInputs'가 표기되었지만 'private/public' 가시성(Visibility) 표기 누락", "Minor", "OM"),
    ("설계서-7p", "CM-003 Transaction(Model) 클래스 멤버 변수 나열 시 데이터 타입(string/number 등) 누락", "Minor", "OM"),
    ("설계서-8p", "M-001 collect() 세부 처리 로직에 req.body 유효성 검증 단계가 누락됨", "Major", "EH"),
    ("설계서-8p", "M-001 collect() 세부 처리 로직에 예외 발생 시 처리 흐름이 누락됨 (errorMiddleware 위임 흐름 미기술)", "Major", "EH"),
    ("설계서-8p", "M-002 list() 세부 처리 로직에 페이지네이션/필터링 처리에 대한 설명 누락", "Minor", "OM"),
    ("설계서-8p", "M-003 collectTransaction() 세부 처리에 transactions 배열 무한 증가에 대한 메모리 제한 정책 누락", "Major", "DR"),
    ("설계서-8p", "M-004 listTransactions() 설명 중 '시간 역순(최신 거래 우선)으로 정렬'은 unshift로만 유지되어 외부 입력의 purchasedAt 순서 보장이 안 됨 — 설계와 구현 불일치", "Major", "IC"),
    # FraudDetection
    ("설계서-9p", "3.2 FraudDetection 패키지에서 내부 함수 resolveRiskLevel()이 클래스 멤버 함수 목록에 누락됨", "Minor", "OM"),
    ("설계서-9p", "CL-001 FraudDetectionService 멤버 변수 'riskService(의존성)'가 실제 구현에서는 import로 처리되어 멤버가 아님 — 설계 표현 부정확", "Minor", "IC"),
    ("설계서-9p", "CL-002 RiskService 멤버 변수 'baseScore=10, amountThreshold=100,000, 가중치(35,20,20)'가 코드에 매직 넘버로 하드코딩됨 — 설계서에 상수 추출 의도 명시 필요", "Major", "MA"),
    ("설계서-9p", "RiskService 입력 모델인 ipAddress, purchasedAt 속성이 점수 계산에 전혀 사용되지 않음 — 설계 의도와 구현 모두 누락", "Major", "OM"),
    ("설계서-10p", "M-005 classifyTransaction() 처리 로직 4단계에서 'crypto.randomUUID()' 사용 시 Node.js 19+ 요구 사항에 대한 환경 제약 명시 누락", "Minor", "DR"),
    ("설계서-10p", "M-005 classifyTransaction() 임계값(80, 50)의 산출 근거(설계 합리성) 누락", "Major", "DR"),
    ("설계서-10p", "M-006 calculateRiskScore() 처리 로직 4단계에서 'location === unknown' 비교 조건이 대소문자/공백을 고려하지 않음", "Minor", "DF"),
    ("설계서-10p", "M-006 calculateRiskScore() 처리 로직 중 입력 transaction.amount가 음수/NaN인 경우의 처리 로직 누락", "Major", "EH"),
    # Dashboard
    ("설계서-11p", "3.3 Dashboard 패키지 구성 클래스에 'main.tsx', 'App.tsx' 진입점 컴포넌트 누락", "Major", "OM"),
    ("설계서-11p", "CN-001 DashboardPage 멤버 함수에 useEffect/useMemo/useCallback 등 React Hooks 사용에 대한 표기 누락", "Minor", "OM"),
    ("설계서-11p", "CN-001 DashboardPage 멤버 변수 'error: string | null'은 설계서에 기술되었으나 자식 컴포넌트로 전달되지 않고 page 내에서만 사용 — 자식과의 관계도 누락", "Minor", "OM"),
    ("설계서-12p", "CN-002 RiskSummaryCard 멤버 변수의 'tone' 타입이 'neutral | warning | danger'로 명세되었으나 코드에서 동일 형식 — OK. 그러나 카드 콘텐츠의 'value' 타입이 string으로 정의되어 숫자 포매팅 책임 불명확", "Minor", "CL"),
    ("설계서-12p", "CN-003 TransactionTable 'items: Transaction[]' props 외 'filteredItems'와의 의미 구분이 모호함 — 부모/자식 책임 분리 설명 누락", "Minor", "CL"),
    ("설계서-12p", "CN-003 TransactionTable의 riskLevelLabel / statusLabel 매핑이 Record<string, string>으로 선언되어 RiskLevel 타입 안전성이 손실됨 — 인터페이스 불일치", "Major", "IE"),
    ("설계서-13p", "CN-004 ApiClient의 BASE_URL이 'http://localhost:4000'로 하드코딩되어 있어 설계서에 환경 변수화 정책이 명시되지 않음", "Major", "DR"),
    # Interface
    ("설계서-14p", "4.1 외부 시스템 인터페이스 표에서 API 응답 스키마(JSON) 예시가 누락됨", "Major", "OM"),
    ("설계서-14p", "4.1 외부 시스템 인터페이스 - REST API 'POST /api/transactions'의 요청 본문 필드 목록 누락", "Major", "OM"),
    ("설계서-14p", "4.1 외부 시스템 인터페이스에서 CORS 정책이 'cors()' 기본값(전체 허용)으로 설명되었으나 보안 요구 반영 누락", "Major", "RQ"),
    ("설계서-14p", "API 엔드포인트 표에서 'POST /api/transactions' 응답 상태 코드 201 표기가 본문에는 200으로 잘못 기술됨 — 표기 일관성 오류", "Minor", "CS"),
    ("설계서-15p", "4.2 사용자 인터페이스 목 업의 등급 색상(neutral/warning/danger)에 대한 색상 코드 명세 누락", "Minor", "OM"),
    # Data
    ("설계서-16p", "5. 데이터 설계 - Transaction 모델 속성 'paymentMethod'가 자유 문자열(string)로 정의되어 enum 화 필요성 미기술", "Minor", "DF"),
    ("설계서-16p", "5. 데이터 설계 - Transaction.id는 UUID v4로 기술되어 있으나 길이/형식 명세 누락", "Minor", "OM"),
    ("설계서-16p", "5. 데이터 설계 - 'purchasedAt' 필드 타임존(UTC/KST) 정책 누락", "Major", "DR"),
    ("설계서-16p", "5. 데이터 설계 - 메모리 저장소 사용에 대한 휘발성/세션 재시작 시 데이터 손실 정책 누락", "Major", "RL"),
    # 구현 기술
    ("설계서-17p", "6. 구현 기술 설계 - 'crypto.randomUUID()' 사용에 대한 Node.js 버전 제약(>=19) 미기술", "Minor", "TD"),
    ("설계서-17p", "6. 구현 기술 설계 - errorMiddleware의 응답 본문 'Internal server error'를 모든 오류에 동일하게 반환 — 4xx/5xx 분리 흐름 누락", "Major", "EH"),
    ("설계서-17p", "6. 구현 기술 설계 - 로깅 정책(console.error 외 로그 레벨/포맷) 누락", "Minor", "OM"),
    # 추적표
    ("설계서-18p", "7. 요구사항 추적표 - U_03(필터링), U_04(새로고침) Use Case의 설계 모듈 매핑이 표에는 표기되었으나 본문 3.3 절에서는 메소드 단위로 매칭되지 않음", "Major", "TR"),
    ("설계서-18p", "7. 요구사항 추적표 - 비기능 요구(NFR) 추적 항목 전체 누락", "Major", "TR"),
    # 부록
    ("설계서-19p", "8. 부록 - 변경 이력 (Change History) 항목이 빈 칸으로 남아 있음", "Minor", "OM"),
    ("설계서-19p", "8. 부록 - 다이어그램 범례(Legend) 누락", "Minor", "OM"),
    # 코드/문서 간 표기 오타
    ("설계서-7p", "'TransactionController'의 설명문 'HTTP 요청을 받아 적절한 서비스로 위임' 중 '위임'을 '위탐'으로 오기 (Typo)", "Minor", "TY"),
    ("설계서-9p", "'classifyTransaction()' 설명에서 'normarl' 오타 발견 (정확: normal)", "Minor", "TY"),
    ("설계서-12p", "'RiskSummaryCard' 설명문 'tone'을 'tonn'로 오기 *2", "Minor", "TY"),
    ("설계서-14p", "REST API 표에서 'Resposne'를 'Response'로 정정 필요", "Minor", "TY"),
    ("설계서-3p", "참조 문서 'system-strucutre.md' 표기 오타 (정확: system-structure.md)", "Minor", "TY"),
]

# ---------------- Summary of Findings ----------------
story.append(P("▶ Summary of Findings", style_section))

# Compute counts per fault code
fault_codes_all = ["CC","CL","CS","DF","DR","EH","HW","IC","IE","LO",
                   "MA","OM","OT","RQ","RL","ST","TD","TS","TR","TY","UI"]
counts = {fc: 0 for fc in fault_codes_all}
for f in findings:
    counts[f[3]] = counts.get(f[3], 0) + 1

# Build a 4-column grid: (code, val, code, val) repeated to mirror sample
def cell_text(code):
    return f"<b>{code}</b>"

# Build 5x6 layout similar to sample (CC/CL/CS/DF/DR/EH/HW/IC/IE/LO/MA/OM/OT/RQ/RL/ST/TD/TS/TR/TY/UI)
# Use 4 columns x 6 rows = 24 slots; 21 codes + 3 empty
sof_rows = [
    [P("CC", style_cell_b), P(str(counts["CC"]) if counts["CC"] else "", style_cell_c),
     P("DR", style_cell_b), P(str(counts["DR"]) if counts["DR"] else "", style_cell_c),
     P("IE", style_cell_b), P(str(counts["IE"]) if counts["IE"] else "", style_cell_c),
     P("OT", style_cell_b), P(str(counts["OT"]) if counts["OT"] else "", style_cell_c),
     P("TD", style_cell_b), P(str(counts["TD"]) if counts["TD"] else "", style_cell_c),
     P("TY", style_cell_b), P(str(counts["TY"]) if counts["TY"] else "", style_cell_c)],
    [P("CL", style_cell_b), P(str(counts["CL"]) if counts["CL"] else "", style_cell_c),
     P("EH", style_cell_b), P(str(counts["EH"]) if counts["EH"] else "", style_cell_c),
     P("LO", style_cell_b), P(str(counts["LO"]) if counts["LO"] else "", style_cell_c),
     P("RQ", style_cell_b), P(str(counts["RQ"]) if counts["RQ"] else "", style_cell_c),
     P("TS", style_cell_b), P(str(counts["TS"]) if counts["TS"] else "", style_cell_c),
     P("UI", style_cell_b), P(str(counts["UI"]) if counts["UI"] else "", style_cell_c)],
    [P("CS", style_cell_b), P(str(counts["CS"]) if counts["CS"] else "", style_cell_c),
     P("HW", style_cell_b), P(str(counts["HW"]) if counts["HW"] else "", style_cell_c),
     P("MA", style_cell_b), P(str(counts["MA"]) if counts["MA"] else "", style_cell_c),
     P("RL", style_cell_b), P(str(counts["RL"]) if counts["RL"] else "", style_cell_c),
     P("TR", style_cell_b), P(str(counts["TR"]) if counts["TR"] else "", style_cell_c),
     P("", style_cell_b), P("", style_cell_c)],
    [P("DF", style_cell_b), P(str(counts["DF"]) if counts["DF"] else "", style_cell_c),
     P("IC", style_cell_b), P(str(counts["IC"]) if counts["IC"] else "", style_cell_c),
     P("OM", style_cell_b), P(str(counts["OM"]) if counts["OM"] else "", style_cell_c),
     P("ST", style_cell_b), P(str(counts["ST"]) if counts["ST"] else "", style_cell_c),
     P("", style_cell_b), P("", style_cell_c),
     P("", style_cell_b), P("", style_cell_c)],
]
sof_widths = [1.2 * cm, 1.2 * cm] * 6
t = Table(sof_rows, colWidths=sof_widths)
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (4, 0), (4, -1), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (6, 0), (6, -1), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (8, 0), (8, -1), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (10, 0), (10, -1), colors.HexColor("#bee3f8")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)

# Totals row
total_count = len(findings)
major_count = sum(1 for f in findings if f[2] == "Major")
minor_count = sum(1 for f in findings if f[2] == "Minor")

totals_rows = [
    [P(f"<b>Number of faults found : {total_count}</b>", style_cell_c),
     P("Major", style_cell_h),
     P(str(major_count), style_cell_c),
     P("Minor", style_cell_h),
     P(str(minor_count), style_cell_c)],
]
t = Table(totals_rows, colWidths=[6.4 * cm, 2.2 * cm, 2.5 * cm, 2.2 * cm, 2.5 * cm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#ebf8ff")),
    ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#bee3f8")),
    ("BACKGROUND", (3, 0), (3, 0), colors.HexColor("#bee3f8")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.3 * cm))

# ---------------- List of Findings ----------------
story.append(P("▶ List of Findings", style_section))

list_header = [
    P("Location", style_cell_h),
    P("Descriptions", style_cell_h),
    P("Severity<br/>Major", style_cell_h),
    P("Severity<br/>Minor", style_cell_h),
    P("Fault<br/>type", style_cell_h),
    P("Moderator<br/>checked?", style_cell_h),
    P("Author<br/>checked?", style_cell_h),
]
rows = [list_header]
for loc, desc, sev, ft in findings:
    rows.append([
        P(loc, style_cell_c),
        P(desc, style_cell),
        P("O", style_cell_c) if sev == "Major" else P("", style_cell_c),
        P("O", style_cell_c) if sev == "Minor" else P("", style_cell_c),
        P(ft, style_cell_c),
        P("", style_cell_c),
        P("", style_cell_c),
    ])

t = Table(rows, colWidths=[2.3 * cm, 8.5 * cm, 1.1 * cm, 1.1 * cm,
                            1.0 * cm, 1.5 * cm, 1.5 * cm],
          repeatRows=1)
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#bee3f8")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)
story.append(P("* 위 표의 칸이 부족한 경우 추가로 확장하여 사용 가능함.", style_cell))

story.append(PageBreak())

# ---------------- Fault Codes ----------------
story.append(P("▶ Fault Codes", style_section))
fault_table = [
    [P("Type", style_cell_h), P("Code", style_cell_h),
     P("Description", style_cell_h)],
    [P("CC", style_cell_c), P("Code Comments", style_cell), P("잘못되었거나 적절치 못한 코드 주석일 경우", style_cell)],
    [P("CL", style_cell_c), P("Clarification", style_cell), P("모호하게 기술되었거나 보다 자세한 설명이 필요한 경우", style_cell)],
    [P("CS", style_cell_c), P("Consistency", style_cell), P("기술된 정보나 양식이 비일관적인 경우", style_cell)],
    [P("DF", style_cell_c), P("Data Fault", style_cell), P("데이터의 형식, 초기화와 같은 데이터에 관련된 결점이 있는 경우", style_cell)],
    [P("DR", style_cell_c), P("Design Rationale", style_cell), P("소프트웨어 아키텍쳐나 설계에 오류가 있는 경우", style_cell)],
    [P("EH", style_cell_c), P("Error Handling", style_cell), P("오류나 특별한 경우에 대한 처리가 없거나 누락된 경우", style_cell)],
    [P("HW", style_cell_c), P("Hardware", style_cell), P("본 기능 구현에 필요한 하드웨어 관련 오류일 경우", style_cell)],
    [P("IC", style_cell_c), P("Incorrect", style_cell), P("기술된 정보가 틀린 경우", style_cell)],
    [P("IE", style_cell_c), P("Interface Error", style_cell), P("모듈 간의 인터페이스가 틀리거나 모호한 경우", style_cell)],
    [P("LO", style_cell_c), P("Logic", style_cell), P("프로그램의 흐름이 틀린 경우, 설계와 프로그램이 다른 경우, 코딩이 표준과 다른 경우", style_cell)],
    [P("MA", style_cell_c), P("Maintainability", style_cell), P("향후 유지보수 문제를 발생하여 수 있는 설계일 경우", style_cell)],
    [P("OM", style_cell_c), P("Omission", style_cell), P("기술되어야 할 정보가 누락된 경우", style_cell)],
    [P("OT", style_cell_c), P("Other", style_cell), P("기술된 결함 유형에 포함되지 않는 경우", style_cell)],
    [P("RQ", style_cell_c), P("Requirements", style_cell), P("고객의 요구 또는 정의된 요구사항을 충족하지 못할 경우", style_cell)],
    [P("RL", style_cell_c), P("Reliability", style_cell), P("제품의 신뢰성 문제를 야기시키는 설계일 경우", style_cell)],
    [P("ST", style_cell_c), P("Standards", style_cell), P("제품이 표준이나 템플릿과 일치하지 않을 경우", style_cell)],
    [P("TD", style_cell_c), P("Too Much Detail", style_cell), P("문서가 너무 상세한 내용을 규정한 경우", style_cell)],
    [P("TS", style_cell_c), P("Test Strategy", style_cell), P("요구사항이 시험 가능하지 않거나, 설계 또는 요구사항을 검증하지 못하는 시험일 경우", style_cell)],
    [P("TR", style_cell_c), P("Traceability", style_cell), P("다른 문서로의 추적성이 누락되거나 틀린 경우", style_cell)],
    [P("TY", style_cell_c), P("Typo", style_cell), P("오타가 있는 경우", style_cell)],
    [P("UI", style_cell_c), P("Usability", style_cell), P("사용자 인터페이스와 관련되어 사용 용이성 문제일 경우", style_cell)],
]
t = Table(fault_table, colWidths=[1.6 * cm, 3.6 * cm, 11.8 * cm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#4a5568")),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#bee3f8")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(P("* 기타 위에서 언급하지 않은 다른 결함의 유형에 대해서는 추가 가능함.",
               style_cell))

# ---------------- Build ----------------
doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    topMargin=1.8 * cm, bottomMargin=1.8 * cm,
    leftMargin=1.8 * cm, rightMargin=1.8 * cm,
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF generated: {OUTPUT_PATH}")
print(f"Total findings: {total_count}, Major: {major_count}, Minor: {minor_count}")
