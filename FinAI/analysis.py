"""
analysis.py - Financial ratio calculations for FinAI
"""

def safe_div(a, b):

    try:
        if isinstance(a, str):
            a = float(a.replace(".", ""))

        if isinstance(b, str):
            b = float(b.replace(".", ""))

        return a / b if b != 0 else 0

    except:
        return 0
    

def calculate_ratios(data):

    doanh_thu = data.get("doanh_thu", 0)
    loi_nhuan = data.get("loi_nhuan_sau_thue", 0)
    tong_tai_san = data.get("tong_tai_san", 0)
    von_chu = data.get("von_chu_so_huu", 0)
    no = data.get("no_phai_tra", 0)
    ts_ngan_han = data.get("tai_san_ngan_han", 0)
    no_ngan_han = data.get("no_ngan_han", 0)


    def safe_div(a, b):
        return a / b if b else 0


    return {

        "profit_margin":
            safe_div(loi_nhuan, doanh_thu),

        "roa":
            safe_div(loi_nhuan, tong_tai_san),

        "roe":
            safe_div(loi_nhuan, von_chu),

        "debt_ratio":
            safe_div(no, tong_tai_san),

        "current_ratio":
            safe_div(ts_ngan_han, no_ngan_han),

        "asset_turnover":
            safe_div(doanh_thu, tong_tai_san)
    }

if __name__ == "__main__":
    sample = {
        "doanh_thu":1000000000,
        "loi_nhuan_sau_thue":120000000,
        "tong_tai_san":2500000000,
        "von_chu_so_huu":1000000000,
        "no_phai_tra":1500000000,
        "tai_san_ngan_han":900000000,
        "no_ngan_han":500000000,
        "hang_ton_kho":200000000
    }
    print(calculate_ratios(sample))
