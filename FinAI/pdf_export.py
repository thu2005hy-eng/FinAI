from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def export_pdf(company, ratios, comments):

    file_name = "Bao_cao_FinAI.pdf"

    doc = SimpleDocTemplate(file_name)


    styles = getSampleStyleSheet()

    content = []


    content.append(
        Paragraph(
            f"Doanh nghiệp: {company}",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 12))


    content.append(
        Paragraph(
            "Chỉ số tài chính:",
            styles["Heading3"]
        )
    )


    for key, value in ratios.items():

        content.append(
            Paragraph(
                f"{key}: {value:.2f}",
                styles["Normal"]
            )
        )


    content.append(Spacer(1, 12))


    content.append(
        Paragraph(
            "Nhận xét AI:",
            styles["Heading3"]
        )
    )


    for c in comments:

        content.append(
            Paragraph(
                "• " + c,
                styles["Normal"]
            )
        )


    doc.build(content)


    return file_name
