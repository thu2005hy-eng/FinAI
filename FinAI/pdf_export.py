from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


# ==========================
# FONT TIẾNG VIỆT
# ==========================

font_path = r"C:\Windows\Fonts\times.ttf"

pdfmetrics.registerFont(
    TTFont(
        "TimesNewRoman",
        font_path
    )
)


# ==========================
# XUẤT PDF
# ==========================

def export_pdf(company_name, ratios, comments):

    file_name = "Bao_cao_FinAI.pdf"

    doc = SimpleDocTemplate(
        file_name
    )

    styles = getSampleStyleSheet()


    normal_style = ParagraphStyle(
        "NormalVN",
        parent=styles["Normal"],
        fontName="TimesNewRoman",
        fontSize=12,
        leading=16
    )


    title_style = ParagraphStyle(
        "TitleVN",
        parent=styles["Title"],
        fontName="TimesNewRoman",
        fontSize=16,
        leading=20
    )


    content = []


    # Tiêu đề
    content.append(
        Paragraph(
            "BÁO CÁO PHÂN TÍCH TÀI CHÍNH - FinAI",
            title_style
        )
    )

    content.append(
        Spacer(1, 20)
    )


    # Doanh nghiệp
    content.append(
        Paragraph(
            f"Doanh nghiệp: {company_name}",
            normal_style
        )
    )


    content.append(
        Spacer(1, 10)
    )


    # Chỉ số tài chính
    content.append(
        Paragraph(
            "Chỉ số tài chính:",
            normal_style
        )
    )


    for key, value in ratios.items():

        content.append(
            Paragraph(
                f"{key}: {value}",
                normal_style
            )
        )


    content.append(
        Spacer(1, 10)
    )


    # Nhận xét AI
    content.append(
        Paragraph(
            "Nhận xét AI:",
            normal_style
        )
    )


    for comment in comments:

        content.append(
            Paragraph(
                "• " + comment,
                normal_style
            )
        )


    # Tạo file PDF
    doc.build(content)


    return file_name