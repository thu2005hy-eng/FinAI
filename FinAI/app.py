# app.py

import streamlit as st
import pandas as pd

from analysis import calculate_ratios
from ai_comment import generate_comments, overall_assessment
from pdf_export import export_pdf

def find_value(data_dict, keywords):
    for key, value in data_dict.items():
        key_lower = str(key).lower()

        for word in keywords:
            if word.lower() in key_lower:
                return value

    return 0


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

            "doanh_thu": find_value(
                income,
                [
                    "doanh thu thuần",
                    "doanh thu bán hàng",
                    "doanh thu về bán hàng"
                ]
            ),

            "loi_nhuan_sau_thue": find_value(
                income,
                [
                    "lợi nhuận sau thuế",
                    "lợi nhuận sau thuế tndn",
                    "lnst"
                ]
            ),

            "tong_tai_san": find_value(
                balance,
                ["tổng tài sản"]
            ),

            "von_chu_so_huu": find_value(
                balance,
                ["vốn chủ sở hữu"]
            ),

            "no_phai_tra": find_value(
                balance,
                ["nợ phải trả"]
            ),

            "tai_san_ngan_han": find_value(
                balance,
                ["tài sản ngắn hạn"]
            ),

            "no_ngan_han": find_value(
                balance,
                ["nợ ngắn hạn"]
            ),
        }
        st.write("Trước xử lý:")
        st.write(data)


        # Tính chỉ số
        for key in data:
            if isinstance(data[key], str):

                value = data[key].strip()

                if "(" in value and ")" in value:
                    value = "-" + value.replace("(", "").replace(")", "")

                value = value.replace(".", "").replace(",", "")

                data[key] = float(value)


        st.write("Sau xử lý:")
        st.write(data)


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