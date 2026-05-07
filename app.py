import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="VN30F Terminal PRO v3",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ... (Phần CSS và Session State của bạn giữ nguyên ở đây) ...

# ══════════════════════════════════════════════════════════════
# DỮ LIỆU – VNSTOCK THỰC + FALLBACK MÔ PHỎNG
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=30, show_spinner=False)
def fetch_data(symbol: str, tf_minutes: int, days_back: int = 7) -> pd.DataFrame:
    """Lấy dữ liệu thật, tự động lùi ngày quét qua cuối tuần nhưng không ép đủ số ngày."""
    
    # Cộng thêm 4 ngày vào chu kỳ quét để bù trừ Thứ 7, CN hoặc nghỉ lễ.
    start_date = (datetime.now() - timedelta(days=days_back + 4)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")

    df = None

    # --- Thử vnstock3 (phiên bản mới) ---
    try:
        from vnstock3 import Vnstock
        vn = Vnstock().stock(symbol=symbol, source="VCI")
        df_temp = vn.quote.history(start=start_date, end=today, interval=f"{tf_minutes}m")
        if df_temp is not None and not df_temp.empty:
            df = df_temp
    except Exception:
        pass

    # --- Thử vnstock cũ (0.2.x) nếu vnstock3 lỗi ---
    if df is None or df.empty:
        try:
            from vnstock import stock_historical_data
            df_temp = stock_historical_data(symbol=symbol, start_date=start_date, end_date=today,
                                       resolution=str(tf_minutes), type="derivative")
            if df_temp is not None and not df_temp.empty:
                df = df_temp
        except Exception:
            pass

    # --- Xử lý dữ liệu nếu lấy thành công ---
    if df is not None and not df.empty:
        df.columns = [c.lower() for c in df.columns]
        
        if "time" not in df.columns:
            df["time"] = df.index
            
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values("time").set_index("time")
        
        return df[["open", "high", "low", "close", "volume"]]

    # --- Fallback mô phỏng ---
    return _simulate(tf_minutes, n=350, seed=hash(symbol + str(tf_minutes)) % 9999)

# ... (Các hàm khác như _simulate, add_indicators... giữ nguyên bên dưới) ...
