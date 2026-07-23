# app.py

import streamlit as st
import pandas as pd

from analysis import calculate_ratios
from ai_comment import generate_comments, overall_assessment
from pdf_export import export_pdf


# ==========================
# Cấu hình giao diện
# ==========================

st.set_page_config(
    page_title="FinAI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 FinAI")
st.caption("Hệ thống AI hỗ trợ phân tích báo cáo tài chính doanh nghiệp")


# ==========================
# Upload file
# ==========================

file = st.file_uploader(
    "📂 Tải báo cáo tài chính Excel",
    type=["xlsx"]
)


if file:

    # Đọc danh sách sheet
    xls = pd.ExcelFile(file)

    sheet_names = xls.sheet_names

    st.subheader("📑 Danh sách sheet trong file")
    st.write(sheet_names)


    # ==========================
    # Đọc dữ liệu
    # ==========================

    income_statement = pd.read_excel(
        xls,
        sheet_name=sheet_names[0]
)


    balance_sheet = pd.read_excel(
        xls,
        sheet_name=sheet_names[1]
)


    st.write("Tên cột báo cáo KQKD:")
    st.write(income_statement.columns)

    st.write("Tên cột bảng cân đối:")
    st.write(balance_sheet.columns)


    # ==========================
    # Hiển thị báo cáo
    # ==========================

    st.subheader("📄 Bảng cân đối kế toán")

    st.dataframe(
        balance_sheet,
        use_container_width=True
    )


    st.subheader("📄 Báo cáo kết quả kinh doanh")

    st.dataframe(
        income_statement,
        use_container_width=True
    )


    # ==========================
    # Phân tích
    # ==========================

    if st.button("🚀 Bắt đầu phân tích"):


        income = dict(
            zip(
                income_statement.iloc[:,0],
                income_statement.iloc[:,-1]
    )
)


        balance = dict(
            zip(
                balance_sheet.iloc[:,0],
                balance_sheet.iloc[:,-1]
    )
)

        st.write("Dữ liệu KQKD:")
        st.write(income)

        st.write("Dữ liệu BCĐKT:")
        st.write(balance)

        data = {

            "doanh_thu":
                income.get("Doanh thu thuần", 0),

            "loi_nhuan_sau_thue":
                income.get("Lợi nhuận sau thuế", 0),

            "tong_tai_san":
                balance.get("Tổng tài sản", 0),

            "von_chu_so_huu":
                balance.get("Vốn chủ sở hữu", 0),

            "no_phai_tra":
                balance.get("Nợ phải trả", 0),

            "tai_san_ngan_han":
                balance.get("A. TÀI SẢN NGẮN HẠN", 0),

            "no_ngan_han":
                balance.get("Nợ ngắn hạn", 0),
        }
        st.write("Dữ liệu đưa vào tính toán:")
        st.write(data)


        # Tính chỉ số
        for key in data:
            if isinstance(data[key], str):
                data[key] = float(
                    data[key].replace(".", "")
        )

        ratios = calculate_ratios(data)


        # ==========================
        # Hiển thị kết quả
        # ==========================

        st.subheader("📊 Chỉ số tài chính")


        c1, c2, c3 = st.columns(3)


        c1.metric(
            "💰 Biên lợi nhuận",
            f"{ratios['profit_margin']:.2%}"
        )

        c1.metric(
            "💳 Hệ số nợ",
            f"{ratios['debt_ratio']:.2%}"
        )


        c2.metric(
            "📈 ROA",
            f"{ratios['roa']:.2%}"
        )

        c2.metric(
            "🏦 Thanh toán hiện hành",
            f"{ratios['current_ratio']:.2f}"
        )


        c3.metric(
            "📊 ROE",
            f"{ratios['roe']:.2%}"
        )

        c3.metric(
            "🔄 Vòng quay tài sản",
            f"{ratios['asset_turnover']:.2f}"
        )


        # ==========================
        # AI nhận xét
        # ==========================

        comments = generate_comments(ratios)


        st.subheader("🤖 Nhận xét AI")


        for comment in comments:
            st.write("•", comment)


        st.success(
            overall_assessment(ratios)
        )


        # ==========================
        # Xuất PDF
        # ==========================

        pdf = export_pdf(
            "Công ty ABC",
            ratios,
            comments
        )


        with open(pdf, "rb") as f:

            st.download_button(
                label="📄 Tải báo cáo PDF",
                data=f,
                file_name="Bao_cao_FinAI.pdf",
                mime="application/pdf"
            )