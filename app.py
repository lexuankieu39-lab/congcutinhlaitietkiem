import streamlit as st

st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Máy tính lãi tiền gửi tiết kiệm")
st.write("Tính lãi theo phương pháp lãi đơn hoặc lãi kép.")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📌 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

phuong_phap = st.selectbox(
    "Phương pháp tính lãi",
    ["Lãi đơn", "Lãi kép"]
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính lãi", type="primary", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    elif lai_suat < 0:
        st.error("Lãi suất không được âm.")
    else:
        # Lãi suất theo tháng
        lai_suat_thang = lai_suat / 100 / 12

        # Số tháng trong kỳ hạn
        so_thang = ky_han

        # -------------------------
        # LÃI ĐƠN
        # -------------------------
        if phuong_phap == "Lãi đơn":

            tong_lai = so_tien * lai_suat_thang * so_thang
            tong_tien = so_tien + tong_lai

        # -------------------------
        # LÃI KÉP
        # -------------------------
        else:

            tong_tien = so_tien * (1 + lai_suat_thang) ** so_thang
            tong_lai = tong_tien - so_tien

        # =========================
        # LÃI ĐỊNH KỲ
        # =========================

        if hinh_thuc == "Lãnh lãi theo tháng":
            so_ky = so_thang
            lai_dinh_ky = tong_lai / so_ky

        elif hinh_thuc == "Lãnh lãi theo quý":
            so_ky = so_thang / 3

            if so_ky > 0:
                lai_dinh_ky = tong_lai / so_ky
            else:
                lai_dinh_ky = tong_lai

        else:
            lai_dinh_ky = tong_lai

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================
        st.divider()
        st.subheader("📊 Kết quả")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Tiền lãi định kỳ",
                format_money(lai_dinh_ky)
            )

        with col2:
            st.metric(
                "Tổng tiền lãi",
                format_money(tong_lai)
            )

        st.metric(
            "💰 Tổng tiền gốc + lãi",
            format_money(tong_tien)
        )

        # =========================
        # CHI TIẾT
        # =========================
        st.divider()

        st.write("### 📋 Thông tin khoản gửi")

        st.write(f"**Số tiền gốc:** {format_money(so_tien)}")
        st.write(f"**Kỳ hạn:** {so_thang} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Phương pháp:** {phuong_phap}")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

        if hinh_thuc == "Lãnh lãi theo tháng":
            st.info(
                f"Mỗi tháng nhận khoảng **{format_money(lai_dinh_ky)}** tiền lãi."
            )

        elif hinh_thuc == "Lãnh lãi theo quý":
            st.info(
                f"Mỗi quý nhận khoảng **{format_money(lai_dinh_ky)}** tiền lãi."
            )

        else:
            st.info(
                f"Cuối kỳ nhận tổng tiền khoảng **{format_money(tong_tien)}**."
            )

        # =========================
        # LƯU Ý
        # =========================
        st.caption(
            "Lưu ý: Đây là công cụ mô phỏng theo lãi suất nhập vào. "
            "Cách tính thực tế của ngân hàng có thể khác tùy sản phẩm tiền gửi, "
            "ngày gửi, ngày đáo hạn và quy định của ngân hàng."
        )
