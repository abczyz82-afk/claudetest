@st.cache_data(ttl=30, show_spinner=False)
def fetch_data(symbol: str, tf_minutes: int, days_back: int = 7) -> pd.DataFrame:
    """Thử vnstock3 → vnstock cũ → fallback mô phỏng."""
    # TRICK: Ép buộc quét tối thiểu 15 ngày để luôn bao trọn cuối tuần và ngày lễ dài
    days_back = max(days_back, 15)
    today      = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    # --- Thử vnstock3 (phiên bản mới) ---
    try:
        from vnstock3 import Vnstock
        vn = Vnstock().stock(symbol=symbol, source="VCI")
        df = vn.quote.history(start=start_date, end=today, interval=f"{tf_minutes}m")
        if df is not None and not df.empty:
            # FIX LỖI: Đưa toàn bộ tên cột về chữ thường để tránh lỗi KeyError
            df.columns = [c.lower() for c in df.columns]
            
            if "time" not in df.columns:
                df["time"] = df.index
            df["time"] = pd.to_datetime(df["time"])
            df = df.sort_values("time").set_index("time")
            return df[["open","high","low","close","volume"]]
    except Exception:
        pass

    # --- Thử vnstock cũ (0.2.x) ---
    try:
        from vnstock import stock_historical_data
        df = stock_historical_data(symbol=symbol, start_date=start_date, end_date=today,
                                   resolution=str(tf_minutes), type="derivative")
        if df is not None and not df.empty:
            df.columns = [c.lower() for c in df.columns]
            df["time"] = pd.to_datetime(df["time"])
            return df.sort_values("time").set_index("time")[["open","high","low","close","volume"]]
    except Exception:
        pass

    # --- Fallback mô phỏng (seed theo symbol+tf để ổn định) ---
    return _simulate(tf_minutes, n=350, seed=hash(symbol + str(tf_minutes)) % 9999)
# ══════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════
with st.spinner("Đang tải dữ liệu..."):
    # Tăng days_back lên 15 và 30 để đảm bảo luôn kéo được dữ liệu thật kể cả nghỉ lễ
    df1_raw = fetch_data(symbol, 1,  days_back=15)
    df5_raw = fetch_data(symbol, 5,  days_back=30)
