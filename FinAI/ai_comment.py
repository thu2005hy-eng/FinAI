def generate_comments(ratios):

    comments = []


    # Sinh lời
    if ratios["profit_margin"] >= 0.05:
        comments.append(
            "Doanh nghiệp có khả năng tạo lợi nhuận tốt trên doanh thu."
        )
    else:
        comments.append(
            "Khả năng sinh lời từ hoạt động kinh doanh còn hạn chế."
        )


    # Thanh toán
    if ratios["current_ratio"] >= 1:
        comments.append(
            "Doanh nghiệp có khả năng thanh toán nợ ngắn hạn tốt."
        )
    else:
        comments.append(
            "Khả năng thanh toán ngắn hạn cần được cải thiện."
        )


    # Nợ
    if ratios["debt_ratio"] <= 0.6:
        comments.append(
            "Cơ cấu nguồn vốn tương đối an toàn, mức sử dụng nợ hợp lý."
        )
    else:
        comments.append(
            "Doanh nghiệp đang sử dụng tỷ trọng nợ khá cao."
        )


    # ROE
    if ratios["roe"] >= 0.15:
        comments.append(
            "Hiệu quả sử dụng vốn chủ sở hữu ở mức tích cực."
        )


    return comments



def overall_assessment(ratios):

    if ratios["roe"] >= 0.15:
        return (
            "Doanh nghiệp có hiệu quả hoạt động tích cực "
            "và khả năng sinh lời tốt."
        )

    return (
        "Doanh nghiệp cần tiếp tục cải thiện "
        "hiệu quả hoạt động tài chính."
    )