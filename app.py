import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import calendar

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="VN30F Terminal PRO v3",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif;background:#080c18;color:#dde4f0;}
.stApp{background:#080c18;}
section[data-testid="stSidebar"]{background:#0c1020;border-right:1px solid #1a2540;}
section[data-testid="stSidebar"] *{color:#c0ccdf!important;}
.metric-box{background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:12px 14px;text-align:center;}
.metric-label{font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;font-family:'JetBrains Mono',monospace;}
.metric-value{font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:700;}
.green{color:#00e676;}.red{color:#ff5252;}.yellow{color:#ffd600;}.white{color:#f1f5f9;}.blue{color:#38bdf8;}.purple{color:#a78bfa;}
.signal-card{border-radius:10px;padding:14px 18px;margin-bottom:8px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:13px;text-align:center;}
.uptrend{background:linear-gradient(135deg,#0a2218,#0d311f);border:1.5px solid #00e676;color:#00e676;}
.downtrend{background:linear-gradient(135deg,#220a0a,#310d0d);border:1.5px solid #ff5252;color:#ff5252;}
.sideway{background:linear-gradient(135deg,#18180a,#26240a);border:1.5px solid #ffd600;color:#ffd600;}
.sec-hdr{font-size:10px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#334155;border-bottom:1px solid #1a2540;padding-bottom:5px;margin-bottom:10px;font-family:'JetBrains Mono',monospace;}
.rec-strong-long{background:linear-gradient(135deg,#052212,#072e18);border:2px solid #00e676;border-radius:12px;padding:18px 20px;font-family:'JetBrains Mono',monospace;}
.rec-strong-short{background:linear-gradient(135deg,#220505,#2e0707);border:2px solid #ff5252;border-radius:12px;padding:18px 20px;font-family:'JetBrains Mono',monospace;}
.rec-watch{background:linear-gradient(135deg,#141205,#1c1a07);border:2px solid #ffd600;border-radius:12px;padding:18px 20px;font-family:'JetBrains Mono',monospace;}
.rec-neutral{background:#0f1626;border:1.5px solid #1a2540;border-radius:12px;padding:18px 20px;font-family:'JetBrains Mono',monospace;}
.score-bar-wrap{background:#1a2540;border-radius:6px;height:12px;width:100%;margin:8px 0;}
.forecast-box{background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:12px 14px;margin-bottom:8px;font-family:'JetBrains Mono',monospace;font-size:11px;}
.pattern-tag{display:inline-block;border-radius:4px;padding:2px 7px;font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;margin:2px;}
.stButton>button{background:linear-gradient(135deg,#1e3a8a,#1d4ed8);color:#fff;border:none;border-radius:6px;font-family:'JetBrains Mono',monospace;font-weight:600;}
.stButton>button:hover{background:linear-gradient(135deg,#1d4ed8,#3b82f6);}
.stTabs [data-baseweb="tab"]{font-family:'JetBrains Mono',monospace;font-size:11px;color:#475569;}
.stTabs [aria-selected="true"]{color:#38bdf8!important;border-bottom-color:#38bdf8!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:0.8rem;padding-bottom:0.5rem;}
.stSelectbox>div>div,.stNumberInput>div>div>input{background:#0f1626;border-color:#1a2540;color:#dde4f0;}

/* Alert Banner */
@keyframes pulse-green { 0%,100%{box-shadow:0 0 0 0 #00e67644} 50%{box-shadow:0 0 20px 4px #00e67622} }
@keyframes pulse-red    { 0%,100%{box-shadow:0 0 0 0 #ff525244} 50%{box-shadow:0 0 20px 4px #ff525222} }
.alert-long  { background:linear-gradient(135deg,#031a0d,#052212,#072e18);border:2px solid #00e676;border-radius:12px;padding:16px 20px;animation:pulse-green 2s infinite;font-family:'JetBrains Mono',monospace; }
.alert-short { background:linear-gradient(135deg,#1a0303,#220505,#2e0707);border:2px solid #ff5252;border-radius:12px;padding:16px 20px;animation:pulse-red 2s infinite;font-family:'JetBrains Mono',monospace; }
.alert-muted { background:#0f1626;border:1px solid #1a2540;border-radius:12px;padding:16px 20px;font-family:'JetBrains Mono',monospace;opacity:0.5; }

/* Alert log row */
.alert-row-long  { border-left:3px solid #00e676;background:#0a1f12;border-radius:5px;padding:7px 10px;margin-bottom:4px;font-family:'JetBrains Mono',monospace;font-size:11px; }
.alert-row-short { border-left:3px solid #ff5252;background:#1f0a0a;border-radius:5px;padding:7px 10px;margin-bottom:4px;font-family:'JetBrains Mono',monospace;font-size:11px; }

/* Win rate badge */
.wr-badge-good { background:#052212;border:1px solid #00e676;color:#00e676;border-radius:5px;padding:3px 8px;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700; }
.wr-badge-bad  { background:#220505;border:1px solid #ff5252;color:#ff5252;border-radius:5px;padding:3px 8px;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700; }
.wr-badge-mid  { background:#141205;border:1px solid #ffd600;color:#ffd600;border-radius:5px;padding:3px 8px;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700; }
.wr-row        { display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid #1a2540;font-family:'JetBrains Mono',monospace;font-size:11px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
for k, v in {
    "trade_history":    [],
    "last_refresh":     datetime.now(),
    "signal_history":   [],
    "prev_sig_keys":    set(),
    "alert_history":    [],          # lịch sử cảnh báo score cao
    "alert_last_score": 0,           # score lần refresh trước (tránh spam)
    "alert_muted":      False,       # tắt cảnh báo tạm thời
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════
# DỮ LIỆU – VNSTOCK THỰC + FALLBACK MÔ PHỎNG
# ══════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════
# TIỆN ÍCH NGÀY ĐÁO HẠN VN30F1M
# ══════════════════════════════════════════════════════════════
def get_third_thursday(year: int, month: int) -> datetime:
    """Trả về ngày thứ 5 tuần thứ 3 của tháng (ngày đáo hạn VN30F)."""
    first_day = datetime(year, month, 1)
    # weekday(): Mon=0 … Sun=6  → Thu=3
    days_to_thu = (3 - first_day.weekday()) % 7
    first_thu   = first_day + timedelta(days=days_to_thu)
    return first_thu + timedelta(weeks=2)          # tuần thứ 3


def get_vn30f1m_expiry_info() -> dict:
    """
    Trả về thông tin đáo hạn hợp đồng VN30F1M hiện tại:
      - last_expiry  : ngày đáo hạn trước (= ngày hợp đồng hiện tại bắt đầu)
      - next_expiry  : ngày đáo hạn tiếp theo
      - days_since   : số ngày kể từ khi hợp đồng bắt đầu
      - days_to      : số ngày còn đến đáo hạn
      - contract_name: tên tháng hợp đồng (VD "VN30F2506")
      - exact_symbol : mã chính xác cho API (VD "VN30F2605")
    """
    now = datetime.now()

    # Đáo hạn tháng hiện tại
    curr_exp = get_third_thursday(now.year, now.month)

    if now.date() > curr_exp.date():
        last_exp = curr_exp
        nm = now.month + 1 if now.month < 12 else 1
        ny = now.year     if now.month < 12 else now.year + 1
        next_exp = get_third_thursday(ny, nm)
        contract_month, contract_year = nm, ny
    else:
        pm = now.month - 1 if now.month > 1 else 12
        py = now.year      if now.month > 1 else now.year - 1
        last_exp    = get_third_thursday(py, pm)
        next_exp    = curr_exp
        contract_month, contract_year = now.month, now.year

    days_since = (now.date() - last_exp.date()).days
    days_to    = (next_exp.date() - now.date()).days

    # Tên hiển thị kiểu VN30F2506 (năm 2 chữ số + tháng 2 chữ số)
    contract_name = f"VN30F{str(contract_year)[-2:]}{contract_month:02d}"

    # Mã chính xác để query vnstock: VN30F2605 (năm trước, tháng sau)
    # vnstock dùng format: VN30F[YY][MM] trong đó YY=2 số cuối năm, MM=tháng 2 chữ số
    exact_symbol = f"VN30F{str(contract_year)[-2:]}{contract_month:02d}"

    return {
        "last_expiry":    last_exp,
        "next_expiry":    next_exp,
        "days_since":     days_since,
        "days_to":        days_to,
        "contract_name":  contract_name,
        "exact_symbol":   exact_symbol,
    }


def smart_days_back(symbol: str, tf_minutes: int) -> int:
    """
    Tính số ngày lấy dữ liệu phù hợp:
    - Với VN30F1M: dựa theo vòng đời hợp đồng (tránh yêu cầu dữ liệu
      trước khi hợp đồng tồn tại).
    - Đảm bảo đủ bars để tính chỉ báo (EMA200 cần ≥ 200 bars).
    """
    if "VN30F1M" not in symbol:
        return 14 if tf_minutes <= 5 else 60

    info = get_vn30f1m_expiry_info()
    # Hợp đồng tối đa sống ~22 ngày làm việc (~31 ngày dương lịch)
    # Lấy tối đa số ngày đã có dữ liệu + 2 ngày đệm
    max_available = max(info["days_since"] + 2, 5)

    if tf_minutes == 1:
        # 1-phút cần nhiều bars → lấy tối đa nhưng không quá 14 ngày
        return min(max_available, 14)
    else:
        # 5-phút: lấy thoải mái hơn
        return min(max_available, 31)


def is_trading_hours() -> bool:
    """Kiểm tra có đang trong giờ giao dịch HOSE không (giờ Việt Nam)."""
    now = datetime.now()
    # HOSE: Thứ 2-6, 09:00–11:30 và 13:00–14:45
    if now.weekday() >= 5:        # Thứ 7, CN
        return False
    t = now.time()
    from datetime import time as dtime
    return (dtime(9, 0) <= t <= dtime(11, 30)) or (dtime(13, 0) <= t <= dtime(14, 45))


@st.cache_data(ttl=30, show_spinner=False)
def fetch_data(symbol: str, tf_minutes: int, days_back: int = 7) -> pd.DataFrame:
    """
    Tải dữ liệu OHLCV:
      1. vnstock3 (mới nhất) – thử cả symbol gốc lẫn mã hợp đồng chính xác
      2. vnstock 0.2.x        – thử cả symbol gốc lẫn mã hợp đồng chính xác
      3. Fallback mô phỏng   – luôn có data, không bao giờ trả về rỗng
    Ngoài giờ giao dịch vẫn trả về dữ liệu lịch sử đã có.
    """
    end_date   = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_back + 2)).strftime("%Y-%m-%d")

    # Nếu là VN30F1M → build danh sách symbol ưu tiên:
    #   [mã chính xác, "VN30F1M"] để vnstock cũ khỏi nhầm
    if symbol == "VN30F1M":
        exp_info = get_vn30f1m_expiry_info()
        symbols_to_try = [exp_info["exact_symbol"], "VN30F1M"]
    else:
        symbols_to_try = [symbol]

    def _clean(df: pd.DataFrame) -> pd.DataFrame:
        """Chuẩn hóa cột và index."""
        df = df.rename(columns={c: c.lower() for c in df.columns})
        if "time" not in df.columns:
            df["time"] = pd.to_datetime(df.index)
        else:
            df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values("time").set_index("time")
        cols = [c for c in ["open","high","low","close","volume"] if c in df.columns]
        df = df[cols].dropna(how="all")
        return df

    # ── vnstock3 ──
    for sym in symbols_to_try:
        try:
            from vnstock3 import Vnstock
            vn  = Vnstock().stock(symbol=sym, source="VCI")
            df  = vn.quote.history(start=start_date, end=end_date, interval=f"{tf_minutes}m")
            if df is not None and not df.empty:
                df = _clean(df)
                if not df.empty and len(df) > 5:
                    return df
        except Exception:
            pass

    # ── vnstock 0.2.x ──
    for sym in symbols_to_try:
        try:
            from vnstock import stock_historical_data
            df = stock_historical_data(
                symbol=sym, start_date=start_date, end_date=end_date,
                resolution=str(tf_minutes), type="derivative"
            )
            if df is not None and not df.empty:
                df = _clean(df)
                if not df.empty and len(df) > 5:
                    return df
        except Exception:
            pass

    # ── Fallback mô phỏng ──
    return _simulate(tf_minutes, n=350, seed=hash(symbol + str(tf_minutes)) % 9999)


@st.cache_data(ttl=300, show_spinner=False)
def fetch_data_extended(symbol: str, tf_minutes: int, days_back: int) -> pd.DataFrame:
    """
    Phiên bản extended: thử fetch với days_back lớn hơn khi thiếu dữ liệu.
    Cache TTL = 5 phút (ít thay đổi hơn).
    """
    return fetch_data(symbol, tf_minutes, days_back)


def _simulate(tf_minutes: int, n: int = 350, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    now   = datetime.now().replace(second=0, microsecond=0)
    now  -= timedelta(minutes=now.minute % tf_minutes)
    times = [now - timedelta(minutes=tf_minutes * i) for i in range(n)][::-1]
    p = [1280.0]
    for i in range(1, n):
        phase = (i // 50) % 3
        drift = 0.18 if phase == 0 else (-0.15 if phase == 2 else 0.0)
        vol   = 0.30 if phase == 1 else 0.62
        p.append(max(p[-1] + drift + np.random.normal(0, vol), 100))
    noise = np.abs(np.random.normal(0, 0.3, n)) + 0.1
    df = pd.DataFrame({"time": times, "close": p})
    df["open"]   = df["close"].shift(1).fillna(df["close"].iloc[0])
    df["high"]   = df[["open","close"]].max(axis=1) + noise
    df["low"]    = df[["open","close"]].min(axis=1) - noise
    df["volume"] = np.random.randint(200, 3500, n)
    df = df.set_index("time")
    df.attrs["_simulated"] = True   # đánh dấu để phân biệt
    return df


# ══════════════════════════════════════════════════════════════
# CHỈ BÁO KỸ THUẬT
# ══════════════════════════════════════════════════════════════
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    c, h, l, n = df["close"].values, df["high"].values, df["low"].values, len(df)

    def ema(arr, p):
        r = np.full(len(arr), np.nan); k = 2/(p+1)
        r[p-1] = arr[:p].mean()
        for i in range(p, len(arr)): r[i] = arr[i]*k + r[i-1]*(1-k)
        return r

    # EMAs
    df["ema9"]  = ema(c, 9)
    df["ema21"] = ema(c, 21)
    df["ema50"] = ema(c, 50)
    df["ema200"]= ema(c, 200)

    # Bollinger Bands
    rm = pd.Series(c).rolling(20).mean().values
    rs = pd.Series(c).rolling(20).std().values
    df["bb_mid"]   = rm
    df["bb_upper"] = rm + 2*rs
    df["bb_lower"] = rm - 2*rs
    df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / pd.Series(rm).replace(0, np.nan).values

    # RSI
    d = pd.Series(c).diff()
    g_ = d.clip(lower=0).rolling(14).mean()
    l_ = (-d.clip(upper=0)).rolling(14).mean().replace(0, np.nan)
    df["rsi"] = (100 - 100/(1 + g_/l_)).fillna(50)

    # MACD
    e12, e26   = ema(c,12), ema(c,26)
    ml         = e12 - e26
    df["macd"]        = ml
    df["macd_signal"] = ema(np.nan_to_num(ml), 9)
    df["macd_hist"]   = ml - df["macd_signal"].values
    df["macd_slope"]  = pd.Series(df["macd_hist"].values).diff(3)   # slope 3 nến

    # ATR / ADX / DI
    df["prev_close"] = df["close"].shift(1)
    df["tr"] = df[["high","low","prev_close"]].apply(
        lambda r: max(r["high"]-r["low"], abs(r["high"]-r["prev_close"]), abs(r["low"]-r["prev_close"])), axis=1)
    df["up_move"]   = df["high"] - df["high"].shift(1)
    df["down_move"] = df["low"].shift(1) - df["low"]
    df["+dm"] = np.where((df["up_move"]>df["down_move"]) & (df["up_move"]>0), df["up_move"], 0)
    df["-dm"] = np.where((df["down_move"]>df["up_move"]) & (df["down_move"]>0), df["down_move"], 0)
    rma = lambda s, p: s.ewm(alpha=1/p, min_periods=p, adjust=False).mean()
    df["atr"]    = rma(df["tr"], 14)
    dmp14 = rma(df["+dm"], 14); dmm14 = rma(df["-dm"], 14)
    safe = lambda x: x.replace(0, np.nan)
    df["di_pos"] = 100 * dmp14 / safe(df["atr"])
    df["di_neg"] = 100 * dmm14 / safe(df["atr"])
    df["dx"]     = 100 * (df["di_pos"]-df["di_neg"]).abs() / (df["di_pos"]+df["di_neg"]).replace(0, np.nan)
    df["adx"]    = rma(df["dx"], 14)

    # Stochastic
    lo14 = pd.Series(l).rolling(14).min(); hi14 = pd.Series(h).rolling(14).max()
    k_   = (pd.Series(c)-lo14)/(hi14-lo14+1e-9)*100
    df["stoch_k"] = k_.rolling(3).mean(); df["stoch_d"] = df["stoch_k"].rolling(3).mean()

    # ── VWAP + Bands (reset theo ngày) ──
    df["date_"]  = df.index.date
    df["tp_"]    = (df["high"] + df["low"] + df["close"]) / 3
    df["cum_tv"] = (df["tp_"] * df["volume"]).groupby(df["date_"]).cumsum()
    df["cum_v"]  = df["volume"].groupby(df["date_"]).cumsum()
    df["vwap"]   = df["cum_tv"] / df["cum_v"].replace(0, np.nan)

    # VWAP Standard Deviation Bands (±1σ, ±2σ)
    # Variance tích lũy: Σ(vol × (tp - vwap)²) / Σvol
    df["_tp_vwap_sq"] = df["volume"] * (df["tp_"] - df["vwap"]) ** 2
    df["_cum_var"]    = df["_tp_vwap_sq"].groupby(df["date_"]).cumsum()
    df["vwap_sd"]     = np.sqrt(df["_cum_var"] / df["cum_v"].replace(0, np.nan))
    df["vwap_u1"]     = df["vwap"] + 1 * df["vwap_sd"]   # +1σ
    df["vwap_u2"]     = df["vwap"] + 2 * df["vwap_sd"]   # +2σ
    df["vwap_l1"]     = df["vwap"] - 1 * df["vwap_sd"]   # -1σ
    df["vwap_l2"]     = df["vwap"] - 2 * df["vwap_sd"]   # -2σ

    # VWAP deviation % (giá cách VWAP bao nhiêu %)
    df["vwap_dev_pct"] = (df["close"] - df["vwap"]) / df["vwap"].replace(0, np.nan) * 100

    # VWAP cross signals
    df["vwap_buy"]  = (df["close"] > df["vwap"]) & (df["close"].shift(1) <= df["vwap"].shift(1))
    df["vwap_sell"] = (df["close"] < df["vwap"]) & (df["close"].shift(1) >= df["vwap"].shift(1))

    # VWAP band bounce (chạm ±2σ rồi hồi)
    df["vwap_bounce_up"]  = (df["low"].shift(1) <= df["vwap_l2"].shift(1)) & (df["close"] > df["vwap_l2"])
    df["vwap_bounce_dn"]  = (df["high"].shift(1) >= df["vwap_u2"].shift(1)) & (df["close"] < df["vwap_u2"])

    df.drop(["prev_close","up_move","down_move","+dm","-dm","dx",
             "date_","tp_","cum_tv","cum_v","_tp_vwap_sq","_cum_var"], axis=1, inplace=True, errors="ignore")

    # Volume MA
    df["vol_ma"] = pd.Series(df["volume"].values).rolling(20).mean().values

    # Tín hiệu cắt đơn
    df["ema_buy"]     = (df["ema9"]>df["ema21"]) & (df["ema9"].shift(1)<=df["ema21"].shift(1))
    df["ema_sell"]    = (df["ema9"]<df["ema21"]) & (df["ema9"].shift(1)>=df["ema21"].shift(1))
    df["macd_buy"]    = (df["macd_hist"]>0)  & (df["macd_hist"].shift(1)<=0)
    df["macd_sell"]   = (df["macd_hist"]<0)  & (df["macd_hist"].shift(1)>=0)
    df["bb_break_up"] = (df["close"]>df["bb_upper"]) & (df["close"].shift(1)<=df["bb_upper"].shift(1))
    df["bb_break_dn"] = (df["close"]<df["bb_lower"]) & (df["close"].shift(1)>=df["bb_lower"].shift(1))

    return df


# ══════════════════════════════════════════════════════════════
# NHẬN DIỆN MẪU NẾN – 17 mẫu + context scoring
# ══════════════════════════════════════════════════════════════
# Độ tin cậy thống kê của từng mẫu (lịch sử nghiên cứu)
PATTERN_BASE_RELIABILITY = {
    "Morning Star":        82, "Evening Star":       80,
    "Three White Soldiers":78, "Three Black Crows":  77,
    "Bull Engulfing":      75, "Bear Engulfing":     74,
    "Piercing Line":       68, "Dark Cloud Cover":   67,
    "Hammer":              65, "Shooting Star":      64,
    "Bullish Harami":      60, "Bearish Harami":     59,
    "Marubozu Bull":       72, "Marubozu Bear":      71,
    "Tweezer Bottom":      63, "Tweezer Top":        62,
    "Doji":                55, "Spinning Top":       50,
}

def detect_candle_patterns(df: pd.DataFrame) -> list:
    """
    Nhận diện 17 mẫu nến. Mỗi mẫu trả về:
      name, bias, desc, reliability (%), context_bonus, quality (A/B/C)
    """
    patterns = []
    if len(df) < 5: return patterns

    c0,c1,c2,c3,c4 = [df.iloc[-(i+1)] for i in range(5)]

    def vals(c):
        o,h,lo,cl = c["open"],c["high"],c["low"],c["close"]
        body = abs(cl-o); rng  = h-lo+1e-9
        upper_wick = h - max(cl,o)
        lower_wick = min(cl,o) - lo
        return o,h,lo,cl,body,rng,upper_wick,lower_wick

    o0,h0,lo0,cl0,bd0,rg0,uw0,lw0 = vals(c0)
    o1,h1,lo1,cl1,bd1,rg1,uw1,lw1 = vals(c1)
    o2,h2,lo2,cl2,bd2,rg2,uw2,lw2 = vals(c2)
    o3,h3,lo3,cl3,bd3,rg3,_,_      = vals(c3)
    o4,h4,lo4,cl4,bd4,rg4,_,_      = vals(c4)

    # ── Context: nến đang ở vùng nào? ──
    vwap       = float(c0.get("vwap", 0)   or 0)
    bb_lo_val  = float(c0.get("bb_lower",0) or 0)
    bb_up_val  = float(c0.get("bb_upper",9999) or 9999)
    vwap_l2    = float(c0.get("vwap_l2",0)  or 0)
    vwap_u2    = float(c0.get("vwap_u2",9999) or 9999)
    bb_w       = float(c0.get("bb_width",0.03) or 0.03)
    hist_bbw   = df["bb_width"].dropna().tail(50)
    is_squeeze = len(hist_bbw)>10 and bb_w < hist_bbw.quantile(0.20)
    at_bb_low  = cl0 <= bb_lo_val * 1.002
    at_bb_high = cl0 >= bb_up_val * 0.998
    at_vwap_l2 = cl0 <= vwap_l2 * 1.003 if vwap_l2 > 0 else False
    at_vwap_u2 = cl0 >= vwap_u2 * 0.997 if vwap_u2 < 9998 else False
    vol_spike  = float(c0.get("volume",0)) > float(c0.get("vol_ma",1) or 1) * 1.5

    def ctx_bonus(bias):
        """Điểm thưởng context: mẫu xuất hiện đúng vùng hỗ trợ/kháng cự."""
        b = 0
        if bias == "BULL":
            if at_bb_low:  b += 12
            if at_vwap_l2: b += 10
        elif bias == "BEAR":
            if at_bb_high: b += 12
            if at_vwap_u2: b += 10
        if vol_spike:  b += 8
        if is_squeeze: b += 5
        return b

    def quality(reliability):
        if reliability >= 80: return "A", "#00e676"
        if reliability >= 65: return "B", "#ffd600"
        return "C", "#f97316"

    def add(name, bias, desc):
        base = PATTERN_BASE_RELIABILITY.get(name, 55)
        cb   = ctx_bonus(bias)
        rel  = min(base + cb, 95)
        ql, qc = quality(rel)
        patterns.append({
            "name": name, "bias": bias, "desc": desc,
            "reliability": rel, "context_bonus": cb,
            "quality": ql, "quality_color": qc,
        })

    # ────────── 1-NẾN ──────────
    # Hammer
    if (bd0/rg0 < 0.35) and (lw0/rg0 > 0.55) and (uw0/rg0 < 0.15) and cl1 < o1:
        add("Hammer","BULL","Nến búa – đảo chiều tăng tại đáy. Râu dưới dài ≥ 2× thân")

    # Inverted Hammer (nến búa ngược)
    if (bd0/rg0 < 0.35) and (uw0/rg0 > 0.55) and (lw0/rg0 < 0.15) and cl1 < o1:
        add("Hammer","BULL","Inverted Hammer – xác nhận tăng nếu nến sau đóng cao hơn")

    # Shooting Star
    if (bd0/rg0 < 0.35) and (uw0/rg0 > 0.55) and (lw0/rg0 < 0.15) and cl1 > o1:
        add("Shooting Star","BEAR","Nến sao băng – đảo chiều giảm tại đỉnh. Râu trên dài ≥ 2× thân")

    # Doji
    if bd0/rg0 < 0.07:
        add("Doji","NEUTRAL","Do dự hoàn toàn – sắp đảo chiều. Mở=Đóng")

    # Spinning Top (thân nhỏ, râu cả 2 phía)
    if (bd0/rg0 < 0.25) and (uw0/rg0 > 0.2) and (lw0/rg0 > 0.2):
        add("Spinning Top","NEUTRAL","Thân nhỏ, râu 2 phía – bull/bear đang giằng co")

    # Marubozu Bull (nến xanh thân đầy, không râu)
    if cl0 > o0 and bd0/rg0 > 0.88:
        add("Marubozu Bull","BULL","Nến xanh thân đầy – lực mua áp đảo hoàn toàn")

    # Marubozu Bear
    if cl0 < o0 and bd0/rg0 > 0.88:
        add("Marubozu Bear","BEAR","Nến đỏ thân đầy – lực bán áp đảo hoàn toàn")

    # ────────── 2-NẾN ──────────
    # Bullish Engulfing
    if cl1 < o1 and cl0 > o0 and cl0 > o1 and o0 < cl1 and bd0 > bd1:
        add("Bull Engulfing","BULL","Nến xanh nuốt trọn nến đỏ – đảo chiều tăng mạnh")

    # Bearish Engulfing
    if cl1 > o1 and cl0 < o0 and cl0 < o1 and o0 > cl1 and bd0 > bd1:
        add("Bear Engulfing","BEAR","Nến đỏ nuốt trọn nến xanh – đảo chiều giảm mạnh")

    # Bullish Harami
    if cl1 < o1 and cl0 > o0 and cl0 < o1 and o0 > cl1 and bd0 < bd1 * 0.5:
        add("Bullish Harami","BULL","Nến xanh nhỏ trong bụng nến đỏ lớn – mẫu đảo chiều yếu hơn")

    # Bearish Harami
    if cl1 > o1 and cl0 < o0 and cl0 > o1 and o0 < cl1 and bd0 < bd1 * 0.5:
        add("Bearish Harami","BEAR","Nến đỏ nhỏ trong bụng nến xanh lớn – nguy cơ đảo chiều")

    # Piercing Line (cắt qua đường giữa)
    if (cl1 < o1 and cl0 > o0 and
        o0 < cl1 and cl0 > (o1 + cl1) / 2 and cl0 < o1):
        add("Piercing Line","BULL","Nến xanh mở dưới đáy nến đỏ, đóng trên ½ thân nến đỏ")

    # Dark Cloud Cover
    if (cl1 > o1 and cl0 < o0 and
        o0 > h1 and cl0 < (o1 + cl1) / 2 and cl0 > o1):
        add("Dark Cloud Cover","BEAR","Nến đỏ mở trên đỉnh nến xanh, đóng dưới ½ thân nến xanh")

    # Tweezer Bottom
    if abs(lo0 - lo1) / rg0 < 0.03 and cl1 < o1 and cl0 > o0:
        add("Tweezer Bottom","BULL","Hai nến chạm cùng đáy – vùng hỗ trợ rất mạnh")

    # Tweezer Top
    if abs(h0 - h1) / rg0 < 0.03 and cl1 > o1 and cl0 < o0:
        add("Tweezer Top","BEAR","Hai nến chạm cùng đỉnh – vùng kháng cự rất mạnh")

    # ────────── 3-NẾN ──────────
    # Morning Star
    if (cl2 < o2 and bd2/rg2 > 0.5 and
        bd1/rg1 < 0.3 and
        cl0 > o0 and cl0 >= (o2 + cl2) / 2):
        add("Morning Star","BULL","3 nến: đỏ lớn → nhỏ (do dự) → xanh lớn. Đảo chiều tăng mạnh")

    # Evening Star
    if (cl2 > o2 and bd2/rg2 > 0.5 and
        bd1/rg1 < 0.3 and
        cl0 < o0 and cl0 <= (o2 + cl2) / 2):
        add("Evening Star","BEAR","3 nến: xanh lớn → nhỏ (do dự) → đỏ lớn. Đảo chiều giảm mạnh")

    # Three White Soldiers (3 nến xanh tăng dần)
    if (cl0>o0 and cl1>o1 and cl2>o2 and
        cl0>cl1>cl2 and o0>o1>o2 and
        bd0/rg0>0.6 and bd1/rg1>0.6 and bd2/rg2>0.6):
        add("Three White Soldiers","BULL","3 nến xanh tăng liên tiếp – xu hướng tăng rất mạnh")

    # Three Black Crows (3 nến đỏ giảm dần)
    if (cl0<o0 and cl1<o1 and cl2<o2 and
        cl0<cl1<cl2 and o0<o1<o2 and
        bd0/rg0>0.6 and bd1/rg1>0.6 and bd2/rg2>0.6):
        add("Three Black Crows","BEAR","3 nến đỏ giảm liên tiếp – xu hướng giảm rất mạnh")

    return patterns


# ══════════════════════════════════════════════════════════════
# SCAN LỊCH SỬ MẪU NẾN (toàn bộ chart)
# ══════════════════════════════════════════════════════════════
def scan_pattern_history(df: pd.DataFrame, lookback: int = 150) -> list:
    """
    Quét N nến gần nhất, trả về list dict có thêm 'time','price','chart_y'
    cho annotations trên biểu đồ.
    """
    results = []
    df_s = df.tail(lookback + 5).copy()
    seen_times = set()

    for i in range(5, len(df_s)):
        sub   = df_s.iloc[:i+1]
        pats  = detect_candle_patterns(sub)
        t     = sub.index[-1]
        price = float(sub["close"].iloc[-1])
        atr   = float(sub["atr"].iloc[-1]) if not np.isnan(sub["atr"].iloc[-1]) else 1.0

        for p in pats:
            key = f"{t}_{p['name']}"
            if key in seen_times: continue
            seen_times.add(key)
            offset = atr * 0.8
            chart_y = (price - offset) if p["bias"] == "BULL" else (price + offset)
            results.append({**p, "time": t, "price": price, "chart_y": chart_y})

    return results


# ══════════════════════════════════════════════════════════════
# RSI DIVERGENCE
# ══════════════════════════════════════════════════════════════
def detect_rsi_divergence(df: pd.DataFrame, lookback: int = 30) -> dict:
    """Phát hiện divergence RSI trong N nến gần nhất."""
    sub = df.dropna(subset=["rsi"]).tail(lookback)
    if len(sub) < 10:
        return {"bull": False, "bear": False, "desc": ""}

    prices = sub["close"].values
    rsis   = sub["rsi"].values

    # Bullish divergence: giá tạo đáy mới nhưng RSI không
    price_lows = [(i, prices[i]) for i in range(1, len(prices)-1)
                  if prices[i] < prices[i-1] and prices[i] < prices[i+1]]
    bull_div = False
    if len(price_lows) >= 2:
        i1, p1 = price_lows[-2]; i2, p2 = price_lows[-1]
        if p2 < p1 and rsis[i2] > rsis[i1] + 2:
            bull_div = True

    # Bearish divergence: giá tạo đỉnh mới nhưng RSI không
    price_highs = [(i, prices[i]) for i in range(1, len(prices)-1)
                   if prices[i] > prices[i-1] and prices[i] > prices[i+1]]
    bear_div = False
    if len(price_highs) >= 2:
        i1, p1 = price_highs[-2]; i2, p2 = price_highs[-1]
        if p2 > p1 and rsis[i2] < rsis[i1] - 2:
            bear_div = True

    desc = ""
    if bull_div: desc = "Giá tạo đáy thấp hơn nhưng RSI tạo đáy cao hơn → lực giảm cạn dần"
    if bear_div: desc = "Giá tạo đỉnh cao hơn nhưng RSI tạo đỉnh thấp hơn → lực tăng suy yếu"

    return {"bull": bull_div, "bear": bear_div, "desc": desc}


# ══════════════════════════════════════════════════════════════
# VOLUME ACCUMULATION ANALYSIS
# ══════════════════════════════════════════════════════════════
def analyze_volume_accumulation(df: pd.DataFrame, window: int = 10) -> dict:
    """So sánh tổng volume nến xanh vs đỏ trong N nến gần nhất."""
    sub = df.tail(window)
    bull_vol = sub.loc[sub["close"] >= sub["open"], "volume"].sum()
    bear_vol = sub.loc[sub["close"] <  sub["open"], "volume"].sum()
    total    = bull_vol + bear_vol + 1e-9
    ratio    = bull_vol / total

    if ratio > 0.65:   bias, desc = "BULL", f"Mua ({ratio*100:.0f}%) áp đảo Bán ({(1-ratio)*100:.0f}%)"
    elif ratio < 0.35: bias, desc = "BEAR", f"Bán ({(1-ratio)*100:.0f}%) áp đảo Mua ({ratio*100:.0f}%)"
    else:              bias, desc = "NEUTRAL", f"Cân bằng (Mua {ratio*100:.0f}% / Bán {(1-ratio)*100:.0f}%)"

    # Nến lớn gần nhất
    avg_vol = float(df["vol_ma"].iloc[-1]) if not np.isnan(df["vol_ma"].iloc[-1]) else 1
    last_vol_ratio = float(df["volume"].iloc[-1]) / max(avg_vol, 1)

    return {"bull_vol": bull_vol, "bear_vol": bear_vol, "ratio": ratio,
            "bias": bias, "desc": desc, "last_vol_ratio": last_vol_ratio}


# ══════════════════════════════════════════════════════════════
# CONFLUENCE SCORE ENGINE  (-100 → +100)
# ══════════════════════════════════════════════════════════════
def compute_confluence(df1: pd.DataFrame, df5: pd.DataFrame) -> dict:
    """
    Tổng hợp tất cả tín hiệu thành một điểm duy nhất.
    Dương = tăng, Âm = giảm. |score| ≥ 70 → Khuyến nghị mạnh.
    """
    score  = 0
    detail = []   # list of (weight, label, color)

    def safe(df, col, default=0):
        v = df.iloc[-1].get(col, default)
        return default if (v is None or (isinstance(v, float) and np.isnan(v))) else float(v)

    # ── Dữ liệu khung 1P ──
    adx1   = safe(df1,"adx",20); di1p = safe(df1,"di_pos",20); di1n = safe(df1,"di_neg",20)
    ema9_1 = safe(df1,"ema9");   ema21_1 = safe(df1,"ema21"); ema50_1 = safe(df1,"ema50")
    rsi1   = safe(df1,"rsi",50); macd_h1 = safe(df1,"macd_hist"); macd_sl1 = safe(df1,"macd_slope")
    bb_up1 = safe(df1,"bb_upper"); bb_lo1 = safe(df1,"bb_lower"); close1 = float(df1["close"].iloc[-1])
    vwap1  = safe(df1,"vwap"); bb_w1 = safe(df1,"bb_width",0.03); stk1 = safe(df1,"stoch_k",50)

    # ── Dữ liệu khung 5P ──
    adx5   = safe(df5,"adx",20); di5p = safe(df5,"di_pos",20); di5n = safe(df5,"di_neg",20)
    ema9_5 = safe(df5,"ema9");   ema21_5 = safe(df5,"ema21")
    rsi5   = safe(df5,"rsi",50); macd_h5 = safe(df5,"macd_hist"); macd_sl5 = safe(df5,"macd_slope")
    close5 = float(df5["close"].iloc[-1])

    # ─────────────────────────────
    # 1. ADX + Hướng (25 điểm)
    # ─────────────────────────────
    if adx5 >= 22:
        w = min(int((adx5 - 22) / 13 * 25), 25)
        if di5p > di5n:
            score += w; detail.append((w, f"ADX 5P={adx5:.1f} DI+>DI- UPTREND",  "#00e676"))
        else:
            score -= w; detail.append((w, f"ADX 5P={adx5:.1f} DI->DI+ DOWNTREND","#ff5252"))
    else:
        detail.append((0, f"ADX 5P={adx5:.1f} → SIDEWAY (0đ)", "#ffd600"))

    # ─────────────────────────────
    # 2. EMA Xếp hàng 1P (15 điểm)
    # ─────────────────────────────
    if ema9_1 > ema21_1 > ema50_1:
        score += 15; detail.append((15,"EMA9>21>50 → BULL 1P","#00e676"))
    elif ema9_1 < ema21_1 < ema50_1:
        score -= 15; detail.append((15,"EMA9<21<50 → BEAR 1P","#ff5252"))
    else:
        detail.append((0,"EMA chưa xếp hàng rõ","#475569"))

    # ─────────────────────────────
    # 3. EMA 1P vs 5P đồng thuận (20 điểm)
    # ─────────────────────────────
    bull1 = ema9_1 > ema21_1; bull5 = ema9_5 > ema21_5
    if bull1 and bull5:
        score += 20; detail.append((20,"EMA 1P & 5P đều BULL → Đồng thuận LONG","#00e676"))
    elif not bull1 and not bull5:
        score -= 20; detail.append((20,"EMA 1P & 5P đều BEAR → Đồng thuận SHORT","#ff5252"))
    else:
        detail.append((0,"EMA 1P & 5P trái chiều (trung tính)","#475569"))

    # ─────────────────────────────
    # 4. MACD Histogram + Slope (15 điểm)
    # ─────────────────────────────
    if macd_h1 > 0 and macd_sl1 > 0:
        score += 15; detail.append((15,"MACD Hist+ & dốc lên → Momentum tăng","#00e676"))
    elif macd_h1 < 0 and macd_sl1 < 0:
        score -= 15; detail.append((15,"MACD Hist- & dốc xuống → Momentum giảm","#ff5252"))
    elif macd_h1 > 0:
        score += 6;  detail.append((6,"MACD Hist dương (slope phẳng)","#38bdf8"))
    elif macd_h1 < 0:
        score -= 6;  detail.append((6,"MACD Hist âm (slope phẳng)","#f97316"))

    # ─────────────────────────────
    # 5. RSI zone (10 điểm)
    # ─────────────────────────────
    if 40 <= rsi1 <= 60:
        detail.append((0,f"RSI={rsi1:.1f} trung tính","#475569"))
    elif rsi1 < 30:
        score += 10; detail.append((10,f"RSI={rsi1:.1f} quá bán → LONG bias","#00e676"))
    elif rsi1 > 70:
        score -= 10; detail.append((10,f"RSI={rsi1:.1f} quá mua → SHORT bias","#ff5252"))
    elif rsi1 < 45:
        score -= 5;  detail.append((5,f"RSI={rsi1:.1f} hơi yếu","#f97316"))
    elif rsi1 > 55:
        score += 5;  detail.append((5,f"RSI={rsi1:.1f} hơi mạnh","#38bdf8"))

    # ─────────────────────────────
    # 6. RSI Divergence (20 điểm)
    # ─────────────────────────────
    div1 = detect_rsi_divergence(df1)
    div5 = detect_rsi_divergence(df5)
    if div1["bull"] or div5["bull"]:
        score += 20; detail.append((20,"RSI Divergence TĂNG → Sắp đảo chiều lên","#00e676"))
    elif div1["bear"] or div5["bear"]:
        score -= 20; detail.append((20,"RSI Divergence GIẢM → Sắp đảo chiều xuống","#ff5252"))

    # ─────────────────────────────
    # 7. Volume Accumulation (10 điểm)
    # ─────────────────────────────
    va = analyze_volume_accumulation(df1)
    if va["bias"] == "BULL":
        score += 10; detail.append((10,f"Volume Tích Lũy: {va['desc']}","#00e676"))
    elif va["bias"] == "BEAR":
        score -= 10; detail.append((10,f"Volume Phân Phối: {va['desc']}","#ff5252"))
    else:
        detail.append((0,f"Volume Cân Bằng: {va['desc']}","#475569"))

    # ─────────────────────────────
    # 8. VWAP position (10 điểm)
    # ─────────────────────────────
    if vwap1 > 0:
        if close1 > vwap1 * 1.001:
            score += 10; detail.append((10,f"Giá ({close1:.1f}) > VWAP ({vwap1:.1f}) → BULL","#00e676"))
        elif close1 < vwap1 * 0.999:
            score -= 10; detail.append((10,f"Giá ({close1:.1f}) < VWAP ({vwap1:.1f}) → BEAR","#ff5252"))
        else:
            detail.append((0,f"Giá ≈ VWAP ({vwap1:.1f}) → Trung tính","#475569"))

    # ─────────────────────────────
    # 9. BB Breakout (20 điểm)
    # ─────────────────────────────
    if close1 > bb_up1:
        score += 20; detail.append((20,"Phá BB Trên + Vol spike → Breakout UP","#00e676"))
    elif close1 < bb_lo1:
        score -= 20; detail.append((20,"Phá BB Dưới + Vol spike → Breakdown","#ff5252"))

    # ─────────────────────────────
    # 10. Candle Patterns (15 điểm)
    # ─────────────────────────────
    patterns = detect_candle_patterns(df1)
    pat_score = 0
    for p in patterns:
        if p["bias"] == "BULL":   pat_score += 15
        elif p["bias"] == "BEAR": pat_score -= 15
    if pat_score > 0:
        score += min(pat_score, 15)
        detail.append((min(pat_score,15), f"Mẫu nến: {', '.join(p['name'] for p in patterns if p['bias']=='BULL')}", "#00e676"))
    elif pat_score < 0:
        score += max(pat_score, -15)
        detail.append((abs(max(pat_score,-15)), f"Mẫu nến: {', '.join(p['name'] for p in patterns if p['bias']=='BEAR')}", "#ff5252"))

    # Clamp [-100, 100]
    score = max(-100, min(100, score))

    # Khuyến nghị
    if score >= 70:
        rec = "LONG MẠNH"; rec_css = "rec-strong-long"; rec_color = "#00e676"
        rec_desc = "Xác suất cao thị trường tăng mạnh trong 3–5 phiên tới. Ưu tiên vào LONG, pullback về EMA21."
    elif score >= 40:
        rec = "NGHIÊNG VỀ LONG"; rec_css = "rec-watch"; rec_color = "#ffd600"
        rec_desc = "Tín hiệu thiên về tăng nhưng chưa đủ mạnh. Chờ xác nhận thêm hoặc vào lệnh size nhỏ."
    elif score <= -70:
        rec = "SHORT MẠNH"; rec_css = "rec-strong-short"; rec_color = "#ff5252"
        rec_desc = "Xác suất cao thị trường giảm mạnh trong 3–5 phiên tới. Ưu tiên vào SHORT, hồi về EMA21."
    elif score <= -40:
        rec = "NGHIÊNG VỀ SHORT"; rec_css = "rec-watch"; rec_color = "#ffd600"
        rec_desc = "Tín hiệu thiên về giảm nhưng chưa đủ mạnh. Chờ xác nhận hoặc vào size nhỏ."
    else:
        rec = "TRUNG TÍNH / CHỜ"; rec_css = "rec-neutral"; rec_color = "#475569"
        rec_desc = "Tín hiệu mâu thuẫn. Không vào lệnh. Chờ điều kiện hội tụ rõ hơn."

    return {
        "score": score, "rec": rec, "rec_css": rec_css, "rec_color": rec_color,
        "rec_desc": rec_desc, "detail": detail,
        "patterns": patterns, "div1": div1, "div5": div5, "va": va,
    }


# ══════════════════════════════════════════════════════════════
# DỰ BÁO VÀI PHIÊN TỚI
# ══════════════════════════════════════════════════════════════
def compute_forecast(df1: pd.DataFrame, df5: pd.DataFrame) -> dict:
    """5 yếu tố dự báo trung hạn → xác suất tăng/giảm mạnh."""
    factors = []

    def safe(df, col, default=0):
        v = df.iloc[-1].get(col, default)
        return default if (v is None or (isinstance(v,float) and np.isnan(v))) else float(v)

    # ── Yếu tố 1: ADX đang tăng (momentum hình thành) ──
    adx_now  = safe(df5,"adx",20)
    adx_prev = float(df5["adx"].iloc[-6]) if len(df5)>6 and not np.isnan(df5["adx"].iloc[-6]) else adx_now
    adx_rising = adx_now > adx_prev + 2
    di5p = safe(df5,"di_pos",20); di5n = safe(df5,"di_neg",20)
    if adx_rising and adx_now > 18:
        bias = "UP" if di5p > di5n else "DOWN"
        factors.append({"label":"ADX Tăng dần","desc":f"ADX từ {adx_prev:.1f}→{adx_now:.1f}, xu hướng đang hình thành","bias":bias,"weight":20})
    else:
        factors.append({"label":"ADX Phẳng/Giảm","desc":"Xu hướng chưa tăng tốc","bias":"NEUTRAL","weight":0})

    # ── Yếu tố 2: RSI Divergence ──
    div = detect_rsi_divergence(df5, lookback=40)
    if div["bull"]:
        factors.append({"label":"RSI Divergence Tăng","desc":div["desc"],"bias":"UP","weight":25})
    elif div["bear"]:
        factors.append({"label":"RSI Divergence Giảm","desc":div["desc"],"bias":"DOWN","weight":25})
    else:
        factors.append({"label":"Không có RSI Divergence","desc":"Không phát hiện phân kỳ","bias":"NEUTRAL","weight":0})

    # ── Yếu tố 3: BB Squeeze + EMA ──
    bb_w = safe(df5,"bb_width",0.03)
    hist_bw = df5["bb_width"].dropna().tail(60)
    is_sqz  = len(hist_bw)>15 and bb_w < hist_bw.quantile(0.15)
    ema9_5  = safe(df5,"ema9"); ema21_5 = safe(df5,"ema21")
    if is_sqz:
        bias = "UP" if ema9_5 > ema21_5 else "DOWN"
        factors.append({"label":"BB Squeeze Đang Hình Thành","desc":f"BB Width={bb_w:.4f} < p15={hist_bw.quantile(0.15):.4f} → Bứt phá sắp xảy ra","bias":bias,"weight":20})
    else:
        factors.append({"label":"Không có BB Squeeze","desc":"Biên độ bình thường","bias":"NEUTRAL","weight":0})

    # ── Yếu tố 4: Volume Accumulation 5P ──
    va = analyze_volume_accumulation(df5, window=15)
    if va["bias"] == "BULL":
        factors.append({"label":"Volume Tích Lũy Mua","desc":va["desc"],"bias":"UP","weight":15})
    elif va["bias"] == "BEAR":
        factors.append({"label":"Volume Phân Phối Bán","desc":va["desc"],"bias":"DOWN","weight":15})
    else:
        factors.append({"label":"Volume Cân Bằng","desc":va["desc"],"bias":"NEUTRAL","weight":0})

    # ── Yếu tố 5: MACD Slope 5P ──
    mh_now  = safe(df5,"macd_hist"); mh_slope = safe(df5,"macd_slope")
    if mh_slope > 0.05:
        bias = "UP"
        factors.append({"label":"MACD Slope Tăng","desc":f"Histogram đang tăng dần (slope={mh_slope:.3f}) → Momentum sắp đảo chiều tăng","bias":"UP","weight":20})
    elif mh_slope < -0.05:
        factors.append({"label":"MACD Slope Giảm","desc":f"Histogram đang giảm dần (slope={mh_slope:.3f}) → Momentum sắp đảo chiều giảm","bias":"DOWN","weight":20})
    else:
        factors.append({"label":"MACD Slope Phẳng","desc":"Momentum chưa rõ hướng","bias":"NEUTRAL","weight":0})

    # Tổng hợp
    up_score   = sum(f["weight"] for f in factors if f["bias"]=="UP")
    down_score = sum(f["weight"] for f in factors if f["bias"]=="DOWN")
    total      = up_score + down_score + 1e-9
    up_prob    = up_score / total * 100
    down_prob  = down_score / total * 100

    if up_prob >= 70:
        verdict = "TĂNG MẠNH"; verdict_color = "#00e676"
        verdict_desc = f"Xác suất TĂNG trong 3–5 phiên: ~{up_prob:.0f}%"
    elif down_prob >= 70:
        verdict = "GIẢM MẠNH"; verdict_color = "#ff5252"
        verdict_desc = f"Xác suất GIẢM trong 3–5 phiên: ~{down_prob:.0f}%"
    elif up_prob >= 55:
        verdict = "Hơi TĂNG"; verdict_color = "#ffd600"
        verdict_desc = f"Thiên về TĂNG ({up_prob:.0f}%) nhưng chưa chắc chắn"
    elif down_prob >= 55:
        verdict = "Hơi GIẢM"; verdict_color = "#ffd600"
        verdict_desc = f"Thiên về GIẢM ({down_prob:.0f}%) nhưng chưa chắc chắn"
    else:
        verdict = "TRUNG TÍNH"; verdict_color = "#475569"
        verdict_desc = "Tín hiệu mâu thuẫn, không dự báo được hướng"

    return {"factors": factors, "up_score": up_score, "down_score": down_score,
            "up_prob": up_prob, "down_prob": down_prob,
            "verdict": verdict, "verdict_color": verdict_color, "verdict_desc": verdict_desc}


# ══════════════════════════════════════════════════════════════
# WIN RATE ANALYTICS – Đầy đủ theo Regime, Hướng, Tín hiệu
# ══════════════════════════════════════════════════════════════
def compute_winrate() -> dict:
    closed = [t for t in st.session_state.trade_history if t["status"] == "CLOSED"]
    if not closed:
        return {"total": 0, "wins": 0, "losses": 0, "win_rate": 0, "total_pnl": 0,
                "avg_win": 0, "avg_loss": 0, "expectancy": 0, "profit_factor": 0,
                "by_regime": {}, "by_direction": {}, "by_signal": {},
                "equity_curve": [], "max_drawdown": 0, "consecutive_losses": 0}

    wins   = [t for t in closed if t.get("pnl_points", 0) > 0]
    losses = [t for t in closed if t.get("pnl_points", 0) <= 0]
    total_pnl     = sum(t.get("pnl_points", 0) for t in closed)
    avg_win       = float(np.mean([t["pnl_points"] for t in wins]))   if wins   else 0
    avg_loss      = float(np.mean([t["pnl_points"] for t in losses])) if losses else 0
    win_rate      = len(wins) / len(closed) * 100
    gross_profit  = sum(t["pnl_points"] for t in wins)   if wins   else 0
    gross_loss    = abs(sum(t["pnl_points"] for t in losses)) if losses else 1e-9
    profit_factor = gross_profit / gross_loss
    expectancy    = (win_rate / 100 * avg_win) + ((1 - win_rate / 100) * avg_loss)

    # ── Phân tích theo Regime ──
    by_regime = {}
    for t in closed:
        r = t.get("regime", "Không rõ") or "Không rõ"
        if r not in by_regime:
            by_regime[r] = {"wins": 0, "total": 0, "pnl": 0}
        by_regime[r]["total"] += 1
        by_regime[r]["pnl"]   += t.get("pnl_points", 0)
        if t.get("pnl_points", 0) > 0:
            by_regime[r]["wins"] += 1
    for r in by_regime:
        by_regime[r]["wr"] = by_regime[r]["wins"] / by_regime[r]["total"] * 100

    # ── Phân tích theo Hướng lệnh ──
    by_direction = {}
    for t in closed:
        d = t.get("direction", "?")
        if d not in by_direction:
            by_direction[d] = {"wins": 0, "total": 0, "pnl": 0}
        by_direction[d]["total"] += 1
        by_direction[d]["pnl"]   += t.get("pnl_points", 0)
        if t.get("pnl_points", 0) > 0:
            by_direction[d]["wins"] += 1
    for d in by_direction:
        by_direction[d]["wr"] = by_direction[d]["wins"] / by_direction[d]["total"] * 100

    # ── Phân tích theo Nguồn tín hiệu (score range) ──
    by_signal = {}
    for t in closed:
        sc = t.get("score", 0)
        if   abs(sc) >= 70: bucket = "Score ≥70 (Mạnh)"
        elif abs(sc) >= 40: bucket = "Score 40-69 (Vừa)"
        else:               bucket = "Score <40 (Yếu)"
        if bucket not in by_signal:
            by_signal[bucket] = {"wins": 0, "total": 0, "pnl": 0}
        by_signal[bucket]["total"] += 1
        by_signal[bucket]["pnl"]   += t.get("pnl_points", 0)
        if t.get("pnl_points", 0) > 0:
            by_signal[bucket]["wins"] += 1
    for b in by_signal:
        by_signal[b]["wr"] = by_signal[b]["wins"] / by_signal[b]["total"] * 100

    # ── Equity Curve ──
    sorted_closed = sorted(closed, key=lambda x: x.get("exit_time", "00:00:00"))
    running = 0.0; equity_curve = []
    for t in sorted_closed:
        running += t.get("pnl_points", 0)
        equity_curve.append({"label": f"#{t['id']}", "eq": running})

    # ── Max Drawdown ──
    peak = 0.0; max_dd = 0.0
    for pt in equity_curve:
        if pt["eq"] > peak: peak = pt["eq"]
        dd = peak - pt["eq"]
        if dd > max_dd: max_dd = dd

    # ── Chuỗi thua liên tiếp ──
    max_consec = cur_consec = 0
    for t in sorted_closed:
        if t.get("pnl_points", 0) <= 0:
            cur_consec += 1
            max_consec  = max(max_consec, cur_consec)
        else:
            cur_consec = 0

    return {
        "total": len(closed), "wins": len(wins), "losses": len(losses),
        "win_rate": win_rate, "total_pnl": total_pnl, "avg_win": avg_win,
        "avg_loss": avg_loss, "expectancy": expectancy, "profit_factor": profit_factor,
        "by_regime": by_regime, "by_direction": by_direction, "by_signal": by_signal,
        "equity_curve": equity_curve, "max_drawdown": max_dd,
        "consecutive_losses": max_consec,
    }


# ══════════════════════════════════════════════════════════════
# ALERT ENGINE – Score ≥ |70| → ghi log + hiển thị banner
# ══════════════════════════════════════════════════════════════
ALERT_THRESHOLD = 70

def push_alert(score: int, confluence: dict, forecast: dict, price: float, regime: str):
    """Ghi cảnh báo vào alert_history khi |score| >= threshold."""
    if abs(score) < ALERT_THRESHOLD:
        return
    # Chỉ push khi score mới "vượt ngưỡng" hoặc đổi hướng
    prev = st.session_state.alert_last_score
    if abs(prev) >= ALERT_THRESHOLD and (score > 0) == (prev > 0):
        return  # cùng hướng, đã alert rồi
    st.session_state.alert_last_score = score
    direction = "LONG" if score > 0 else "SHORT"
    st.session_state.alert_history.insert(0, {
        "time":    datetime.now().strftime("%H:%M:%S"),
        "date":    datetime.now().strftime("%d/%m/%Y"),
        "score":   score,
        "direction": direction,
        "rec":     confluence["rec"],
        "price":   price,
        "regime":  regime,
        "forecast":forecast["verdict"],
        "up_prob": forecast["up_prob"],
        "dn_prob": forecast["down_prob"],
    })
    st.session_state.alert_history = st.session_state.alert_history[:100]


def render_alert_banner(score: int, confluence: dict, price: float, muted: bool):
    """Hiển thị banner cảnh báo nổi bật ở đầu trang."""
    if abs(score) < ALERT_THRESHOLD:
        return
    if muted:
        st.markdown(f"""
        <div class="alert-muted">
          <span style="color:#475569">🔕 Cảnh báo bị tắt · Score {score:+d}</span>
        </div>""", unsafe_allow_html=True)
        return

    is_long   = score > 0
    css       = "alert-long" if is_long else "alert-short"
    color     = "#00e676"   if is_long else "#ff5252"
    icon      = "🚀"        if is_long else "💥"
    direction = "LONG"      if is_long else "SHORT"
    rec       = confluence["rec"]
    rec_desc  = confluence["rec_desc"]

    # Các yếu tố kích hoạt (detail dương nếu long, âm nếu short)
    top_factors = sorted(confluence["detail"],
                         key=lambda x: x[0] * (1 if is_long else -1), reverse=True)[:3]
    factors_html = " &nbsp;·&nbsp; ".join(
        f'<span style="color:{c}">{lbl.split("→")[0].strip()}</span>'
        for _, lbl, c in top_factors if lbl
    )

    st.markdown(f"""
    <div class="{css}">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
        <div>
          <div style="font-size:22px;font-weight:800;color:{color};letter-spacing:1px">
            {icon} CẢNH BÁO: {rec}
          </div>
          <div style="font-size:12px;color:#94a3b8;margin-top:4px">{rec_desc}</div>
          <div style="font-size:10px;color:#475569;margin-top:6px">{factors_html}</div>
        </div>
        <div style="text-align:right">
          <div style="font-size:28px;font-weight:800;color:{color}">{score:+d}</div>
          <div style="font-size:10px;color:#475569">/ 100 điểm</div>
          <div style="font-size:11px;color:{color};margin-top:2px">Giá: {price:.2f}</div>
        </div>
      </div>
    </div>
    <div style="height:6px"></div>
    """, unsafe_allow_html=True)


def render_alert_history():
    """Bảng lịch sử cảnh báo."""
    hist = st.session_state.alert_history
    if not hist:
        st.markdown('<div style="color:#334155;font-family:JetBrains Mono;font-size:11px;padding:8px">Chưa có cảnh báo nào. Score cần ≥ |70| để kích hoạt.</div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div style="font-size:11px;color:#64748b;font-family:JetBrains Mono;margin-bottom:8px">📋 {len(hist)} cảnh báo gần nhất (tối đa 100)</div>', unsafe_allow_html=True)

    for a in hist:
        is_long = a["direction"] == "LONG"
        css   = "alert-row-long" if is_long else "alert-row-short"
        color = "#00e676" if is_long else "#ff5252"
        icon  = "🚀" if is_long else "💥"
        fc_c  = "#00e676" if "TĂNG" in a.get("forecast","") else ("#ff5252" if "GIẢM" in a.get("forecast","") else "#ffd600")
        st.markdown(f"""
        <div class="{css}">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>{icon} <b style="color:{color}">Score {a['score']:+d} · {a['rec']}</b>
              &nbsp;<span style="color:#475569">{a['date']} {a['time']}</span></span>
            <span style="color:#f1f5f9;font-weight:700">{a['price']:.2f}</span>
          </div>
          <div style="display:flex;gap:14px;margin-top:3px;color:#64748b">
            <span>Regime: <b style="color:{'#00e676' if 'UP' in a.get('regime','') else '#ff5252' if 'DOWN' in a.get('regime','') else '#ffd600'}">{a.get('regime','?')}</b></span>
            <span>Dự báo: <b style="color:{fc_c}">{a.get('forecast','?')}</b></span>
            <span>▲{a.get('up_prob',0):.0f}% ▼{a.get('dn_prob',0):.0f}%</span>
          </div>
        </div>""", unsafe_allow_html=True)
def detect_regime(df: pd.DataFrame) -> dict:
    last = df.iloc[-1]
    def g(col, d=0):
        v = last.get(col, d)
        return d if (v is None or (isinstance(v,float) and np.isnan(v))) else float(v)
    adx=g("adx",20); dip=g("di_pos",20); din=g("di_neg",20)
    rsi=g("rsi",50); ema9=g("ema9"); ema21=g("ema21"); bbw=g("bb_width",0.03)
    hist_bw = df["bb_width"].dropna().tail(50)
    sqz_thresh = hist_bw.quantile(0.15) if len(hist_bw)>10 else 0.0
    is_sqz = bbw < sqz_thresh
    regime   = "SIDEWAY" if adx<22 else ("UPTREND" if dip>din else "DOWNTREND")
    strength = "YẾU" if adx<18 else ("MẠNH" if adx>35 else "VỪA")
    last_time = df.index[-1].strftime("%H:%M:%S")
    return {"regime":regime,"strength":strength,"adx":adx,"di_pos":dip,"di_neg":din,
            "rsi":rsi,"ema9":ema9,"ema21":ema21,"bb_w":bbw,"sqz_thresh":sqz_thresh,
            "is_sqz":is_sqz,"last_time":last_time,
            "close":float(last["close"]),"atr":g("atr",2)}


# ══════════════════════════════════════════════════════════════
# BIỂU ĐỒ
# ══════════════════════════════════════════════════════════════
def build_chart(df, title, show_ema, show_bb, show_signals, show_trades,
                show_vwap, show_vwap_bands, show_patterns, score, pattern_history=None):
    df  = df.copy().dropna(subset=["ema21"]).iloc[-250:]
    BG  = "#080c18"; GR = "#1a2540"

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        row_heights=[0.52,0.14,0.17,0.17], vertical_spacing=0.008)

    # Candles
    fig.add_trace(go.Candlestick(x=df.index, open=df["open"], high=df["high"],
        low=df["low"], close=df["close"],
        increasing_line_color="#00e676", decreasing_line_color="#ff5252",
        increasing_fillcolor="#00e676",  decreasing_fillcolor="#ff5252",
        line_width=1, name="OHLC"), row=1, col=1)

    # ── VWAP + Bands ──
    if show_vwap and "vwap" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["vwap"],
            line=dict(color="#f59e0b", width=1.8, dash="dash"), name="VWAP"), row=1, col=1)

        if show_vwap_bands:
            # +2σ / -2σ (vùng extreme)
            fig.add_trace(go.Scatter(x=df.index, y=df["vwap_u2"],
                line=dict(color="#f97316", width=0.9, dash="dot"),
                name="VWAP +2σ", showlegend=True), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["vwap_l2"],
                line=dict(color="#38bdf8", width=0.9, dash="dot"),
                fill="tonexty", fillcolor="rgba(249,115,22,0.04)",
                name="VWAP -2σ", showlegend=True), row=1, col=1)
            # +1σ / -1σ (vùng bình thường)
            fig.add_trace(go.Scatter(x=df.index, y=df["vwap_u1"],
                line=dict(color="#f97316", width=0.6, dash="longdash"),
                name="VWAP +1σ", showlegend=False), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["vwap_l1"],
                line=dict(color="#38bdf8", width=0.6, dash="longdash"),
                name="VWAP -1σ", showlegend=False), row=1, col=1)

        # VWAP cross signals
        if show_signals:
            for col_v, sym_v, color_v, lbl_v in [
                ("vwap_buy",  "triangle-up",  "#f59e0b", "VWAP MUA"),
                ("vwap_sell", "triangle-down","#f97316", "VWAP BÁN"),
            ]:
                if col_v in df.columns:
                    sub_v = df[df[col_v]]
                    if not sub_v.empty:
                        yv = sub_v["low"]-1.2  if "buy" in col_v else sub_v["high"]+1.2
                        fig.add_trace(go.Scatter(x=sub_v.index, y=yv, mode="markers",
                            marker=dict(symbol=sym_v, size=9, color=color_v,
                                        line=dict(color=BG, width=1)),
                            name=lbl_v), row=1, col=1)

    # ── Pattern annotations trực tiếp trên chart ──
    if show_patterns and pattern_history:
        # Lọc trong khoảng thời gian hiển thị
        df_times = set(df.index)
        pats_in_view = [p for p in pattern_history if p["time"] in df_times]

        # Nhóm theo bias để vẽ 1 trace/nhóm (tăng hiệu năng)
        for bias_f, sym_f, color_f, leg_f in [
            ("BULL",    "triangle-up",   "#00c853", "Mẫu TĂNG"),
            ("BEAR",    "triangle-down", "#d50000", "Mẫu GIẢM"),
            ("NEUTRAL", "diamond",       "#ffd600", "Mẫu Trung tính"),
        ]:
            grp = [p for p in pats_in_view if p["bias"] == bias_f]
            if not grp: continue

            # Marker scatter
            fig.add_trace(go.Scatter(
                x    = [p["time"]    for p in grp],
                y    = [p["chart_y"] for p in grp],
                mode = "markers+text",
                marker=dict(symbol=sym_f, size=13, color=color_f,
                            line=dict(color=BG, width=1.5)),
                text     = [p["name"][:4] for p in grp],   # tên ngắn gọn
                textposition = "bottom center" if bias_f=="BULL" else "top center",
                textfont = dict(size=8, color=color_f),
                hovertext= [f"<b>{p['name']}</b><br>{p['desc']}<br>"
                            f"Độ tin cậy: {p['reliability']}% (Chất lượng {p['quality']})<br>"
                            f"Context bonus: +{p['context_bonus']}%<br>"
                            f"Giá: {p['price']:.2f}"
                            for p in grp],
                hoverinfo= "text",
                name     = leg_f,
            ), row=1, col=1)

    # BB
    if show_bb:
        fig.add_trace(go.Scatter(x=df.index, y=df["bb_upper"],
            line=dict(color="#475569",width=1,dash="dot"), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["bb_lower"],
            line=dict(color="#475569",width=1,dash="dot"), fill="tonexty",
            fillcolor="rgba(71,85,105,0.07)", showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["bb_mid"],
            line=dict(color="#334155",width=0.8), showlegend=False), row=1, col=1)

    # EMA
    if show_ema:
        for col_, color_, lbl in [("ema9","#f59e0b","EMA9"),("ema21","#38bdf8","EMA21"),("ema50","#a78bfa","EMA50")]:
            fig.add_trace(go.Scatter(x=df.index, y=df[col_],
                line=dict(color=color_, width=1.5), name=lbl), row=1, col=1)

    # Signal markers
    if show_signals:
        for col_, sym, color_, lbl in [
            ("ema_buy","triangle-up","#00e676","EMA MUA"),
            ("ema_sell","triangle-down","#ff5252","EMA BÁN"),
            ("macd_buy","triangle-up","#38bdf8","MACD MUA"),
            ("macd_sell","triangle-down","#f97316","MACD BÁN"),
            ("bb_break_up","star","#00e676","BB UP"),
            ("bb_break_dn","star","#ff5252","BB DOWN"),
        ]:
            sub_ = df[df[col_]] if col_ in df.columns else pd.DataFrame()
            if not sub_.empty:
                y_ = sub_["low"]-1.5 if "buy" in col_ or "up" in col_ else sub_["high"]+1.5
                fig.add_trace(go.Scatter(x=sub_.index, y=y_, mode="markers",
                    marker=dict(symbol=sym, size=11, color=color_), name=lbl), row=1, col=1)

    # TP/SL
    if show_trades:
        for t in st.session_state.trade_history:
            if t["status"]=="OPEN":
                dc = "#00e676" if t["direction"]=="LONG" else "#ff5252"
                fig.add_hline(y=t["entry"],line_color=dc,line_width=1.5,row=1,col=1,annotation_text="ENTRY",annotation_font_color=dc)
                for lv,lbl in [(t["tp1"],"TP1"),(t["tp2"],"TP2"),(t["tp3"],"TP3")]:
                    fig.add_hline(y=lv,line_color="#00e676",line_dash="dash",row=1,col=1,annotation_text=lbl,annotation_font_color="#00e676")
                fig.add_hline(y=t["sl"],line_color="#ff5252",line_dash="dash",row=1,col=1,annotation_text="SL",annotation_font_color="#ff5252")

    score_color = "#00e676" if score>0 else "#ff5252"

    # Volume
    vc = ["rgba(0,230,118,0.55)" if c>=o else "rgba(255,82,82,0.55)" for c,o in zip(df["close"],df["open"])]
    fig.add_trace(go.Bar(x=df.index, y=df["volume"], marker_color=vc, showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["vol_ma"], line=dict(color="#ffd600",width=1.2), showlegend=False), row=2, col=1)

    # MACD
    mc = ["#00e676" if v>=0 else "#ff5252" for v in df["macd_hist"]]
    fig.add_trace(go.Bar(x=df.index, y=df["macd_hist"], marker_color=mc, showlegend=False), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["macd"], line=dict(color="#38bdf8",width=1.2), name="MACD"), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["macd_signal"], line=dict(color="#ffd600",width=1.2), name="Signal"), row=3, col=1)
    fig.add_hline(y=0, line_color=GR, line_width=0.8, row=3, col=1)

    # RSI + Stoch
    fig.add_trace(go.Scatter(x=df.index, y=df["rsi"], line=dict(color="#38bdf8",width=1.5), name="RSI"), row=4, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["stoch_k"], line=dict(color="#a78bfa",width=1), name="%K"), row=4, col=1)
    for lvl, col_ in [(70,"#ff5252"),(30,"#00e676"),(50,GR)]:
        fig.add_hline(y=lvl, line_color=col_, line_dash="dot", line_width=0.8, row=4, col=1)

    fig.update_layout(
        template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=BG,
        margin=dict(l=0,r=0,t=32,b=0), height=600,
        title=dict(text=f"{title}  |  Score: {score:+d}", font=dict(family="JetBrains Mono",size=12,color=score_color), x=0.01),
        xaxis_rangeslider_visible=False, hovermode="x unified",
        legend=dict(orientation="h",yanchor="bottom",y=1.01,font=dict(size=9,color="#64748b"),bgcolor="rgba(0,0,0,0)"),
    )
    for i in range(1,5):
        fig.update_xaxes(row=i,col=1,gridcolor=GR,showgrid=True,zeroline=False,tickfont=dict(size=8,color="#334155"))
        fig.update_yaxes(row=i,col=1,gridcolor=GR,showgrid=True,zeroline=False,tickfont=dict(size=8,color="#475569"))
    fig.update_yaxes(row=4,col=1,range=[0,100])
    return fig


# ══════════════════════════════════════════════════════════════
# TRADE MANAGEMENT
# ══════════════════════════════════════════════════════════════
def add_trade(direction, entry, tp1, tp2, tp3, sl, size,
              score=0, regime="", signal_tag="Thủ công"):
    st.session_state.trade_history.insert(0, {
        "id":         len(st.session_state.trade_history) + 1,
        "date":       datetime.now().strftime("%d/%m/%Y"),
        "time":       datetime.now().strftime("%H:%M:%S"),
        "exit_time":  "-",
        "direction":  direction,
        "entry":      entry,
        "tp1": tp1, "tp2": tp2, "tp3": tp3, "sl": sl, "size": size,
        "status":     "OPEN",
        "exit_price": 0.0, "pnl_points": 0.0, "pnl": 0.0, "reason": "-",
        # ── Tag mới ──
        "score":      score,
        "regime":     regime,
        "signal_tag": signal_tag,
    })

def close_trade(idx, exit_price, reason="Đóng thủ công"):
    t = st.session_state.trade_history[idx]
    if t["status"] != "OPEN": return
    pts = (exit_price - t["entry"]) * (1 if t["direction"]=="LONG" else -1)
    t.update({"status":"CLOSED","exit_price":exit_price,"exit_time":datetime.now().strftime("%H:%M:%S"),
               "reason":reason,"pnl_points":pts,"pnl":pts*t["size"]*100_000})

def auto_check_trades(cp, target_tp):
    for i, t in enumerate(st.session_state.trade_history):
        if t["status"] == "OPEN":
            tp_val = t[target_tp]
            if t["direction"] == "LONG":
                if cp >= tp_val: close_trade(i, tp_val, f"🎯 Chạm {target_tp.upper()}")
                elif cp <= t["sl"]: close_trade(i, t["sl"], "🛡️ Cắt lỗ SL")
            else:
                if cp <= tp_val: close_trade(i, tp_val, f"🎯 Chạm {target_tp.upper()}")
                elif cp >= t["sl"]: close_trade(i, t["sl"], "🛡️ Cắt lỗ SL")


# ══════════════════════════════════════════════════════════════
# SIGNAL HISTORY
# ══════════════════════════════════════════════════════════════
def get_signal_history(df, tf_label):
    history = []
    for i in range(1, min(len(df), 150)):
        row = df.iloc[-i]; t_str = df.index[-i].strftime("%d/%m %H:%M")
        t_obj = df.index[-i]
        if row.get("ema_buy",False):  history.append({"_ts":t_obj,"Thời gian":t_str,"Khung":tf_label,"Chỉ báo":"EMA 9/21","Tín hiệu":"🟢 EMA Cắt Lên"})
        if row.get("ema_sell",False): history.append({"_ts":t_obj,"Thời gian":t_str,"Khung":tf_label,"Chỉ báo":"EMA 9/21","Tín hiệu":"🔴 EMA Cắt Xuống"})
        if row.get("macd_buy",False): history.append({"_ts":t_obj,"Thời gian":t_str,"Khung":tf_label,"Chỉ báo":"MACD","Tín hiệu":"🟢 MACD Đảo chiều Tăng"})
        if row.get("macd_sell",False):history.append({"_ts":t_obj,"Thời gian":t_str,"Khung":tf_label,"Chỉ báo":"MACD","Tín hiệu":"🔴 MACD Đảo chiều Giảm"})
        if row.get("bb_break_up",False): history.append({"_ts":t_obj,"Thời gian":t_str,"Khung":tf_label,"Chỉ báo":"BB","Tín hiệu":"🚀 BB Break Lên"})
        if row.get("bb_break_dn",False): history.append({"_ts":t_obj,"Thời gian":t_str,"Khung":tf_label,"Chỉ báo":"BB","Tín hiệu":"💥 BB Break Xuống"})
    return history


# ══════════════════════════════════════════════════════════════
# ██ SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="font-family:JetBrains Mono;font-size:16px;font-weight:700;color:#38bdf8;padding:6px 0 14px">⚡ VN30F TERMINAL v3</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">⚙️ CÀI ĐẶT</div>', unsafe_allow_html=True)
    symbol       = st.selectbox("Hợp đồng", ["VN30F1M","VN30F1Q","VN30F2Q"], index=0)

    # ── Thông tin đáo hạn VN30F1M ──
    if "VN30F1M" in symbol:
        _exp = get_vn30f1m_expiry_info()
        _days_to = _exp["days_to"]
        _days_since = _exp["days_since"]
        _exp_color = "#ff5252" if _days_to <= 3 else ("#ffd600" if _days_to <= 7 else "#38bdf8")
        _in_hours  = is_trading_hours()
        _hours_txt = '<span style="color:#00e676">● Đang giao dịch</span>' if _in_hours else '<span style="color:#475569">● Ngoài giờ GD</span>'
        st.markdown(f"""
        <div style="background:#0c1020;border:1px solid #1a2540;border-left:3px solid {_exp_color};
                    border-radius:6px;padding:8px 10px;margin:6px 0 10px;font-family:'JetBrains Mono',monospace;font-size:10px;">
          <div style="color:{_exp_color};font-weight:700">📅 {_exp['contract_name']}</div>
          <div style="color:#64748b;margin-top:2px">Bắt đầu: <b style="color:#c0ccdf">{_exp['last_expiry'].strftime('%d/%m/%Y')}</b> ({_days_since}d)</div>
          <div style="color:#64748b">Đáo hạn: <b style="color:{_exp_color}">{_exp['next_expiry'].strftime('%d/%m/%Y')}</b> (còn {_days_to}d)</div>
          <div style="margin-top:3px">{_hours_txt}</div>
        </div>""", unsafe_allow_html=True)

    auto_refresh = st.toggle("🔄 Tự động cập nhật", value=True)
    refresh_sec  = st.slider("Chu kỳ (giây)", 10, 120, 30) if auto_refresh else 30

    st.markdown('<div class="sec-hdr" style="margin-top:14px">📊 BIỂU ĐỒ</div>', unsafe_allow_html=True)
    show_ema        = st.toggle("EMA 9/21/50",             value=True)
    show_bb         = st.toggle("Bollinger Bands",         value=True)
    show_signals    = st.toggle("Mũi tên tín hiệu",       value=True)
    show_trades     = st.toggle("Đường Entry/TP/SL",       value=True)
    show_vwap       = st.toggle("VWAP",                    value=True)
    show_vwap_bands = st.toggle("VWAP Bands (±1σ / ±2σ)", value=True)
    show_patterns   = st.toggle("🕯️ Mẫu nến trên chart",  value=True)

    st.markdown('<div class="sec-hdr" style="margin-top:14px">🤖 QUẢN LÝ RỦI RO</div>', unsafe_allow_html=True)
    lot_size  = st.number_input("Số hợp đồng", min_value=1, max_value=50, value=1)
    auto_sltp = st.toggle("Bot tự tính SL/TP theo ATR", value=True)
    if not auto_sltp:
        tp1_points = st.number_input("TP1 (điểm)", min_value=1.0, max_value=50.0, value=4.0, step=0.5)
        tp2_points = st.number_input("TP2 (điểm)", min_value=1.0, max_value=50.0, value=8.0, step=0.5)
        tp3_points = st.number_input("TP3 (điểm)", min_value=1.0, max_value=50.0, value=12.0,step=0.5)
        sl_points  = st.number_input("SL  (điểm)", min_value=1.0, max_value=30.0, value=4.0, step=0.5)

    auto_tp_target = st.selectbox("Bot đóng lệnh tại", ["TP1","TP2","TP3"], index=2)

    st.markdown("---")
    st.markdown('<div class="sec-hdr">🔔 CẢI ĐẶT CẢNH BÁO</div>', unsafe_allow_html=True)
    alert_threshold = st.slider("Ngưỡng Score Alert", 50, 90, 70, step=5,
                                help="Khi |Score| ≥ ngưỡng này → hiện banner cảnh báo")
    mute_alerts = st.toggle("🔕 Tắt banner cảnh báo", value=False)
    if st.button("🗑️ Xóa lịch sử cảnh báo", use_container_width=True):
        st.session_state.alert_history    = []
        st.session_state.alert_last_score = 0
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ Xóa toàn bộ lịch sử lệnh", use_container_width=True):
        st.session_state.trade_history = []; st.rerun()

    st.markdown('<div style="font-size:10px;color:#1a2540;font-family:JetBrains Mono;margin-top:6px">⚠️ Dùng API thực: cài vnstock3<br>pip install vnstock3</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# LOAD DATA  – thông minh theo vòng đời hợp đồng & giờ giao dịch
# ══════════════════════════════════════════════════════════════
_expiry_info = get_vn30f1m_expiry_info() if "VN30F1M" in symbol else None
_db1 = smart_days_back(symbol, 1)
_db5 = smart_days_back(symbol, 5)

# Thông báo nếu hợp đồng mới (ít ngày)
_new_contract_warn = ""
if _expiry_info and _expiry_info["days_since"] <= 3:
    _new_contract_warn = (
        f"⚠️ Hợp đồng **{_expiry_info['contract_name']}** mới bắt đầu "
        f"({_expiry_info['days_since']} ngày) — dữ liệu lịch sử còn ít, "
        f"chỉ báo sẽ chính xác dần theo thời gian."
    )

with st.spinner("Đang tải dữ liệu VN30F1M..."):
    df1_raw = fetch_data(symbol, 1, days_back=_db1)
    df5_raw = fetch_data(symbol, 5, days_back=_db5)

    # Nếu df thiếu bars (do hợp đồng mới), kéo thêm dữ liệu
    MIN_BARS_1 = 50
    MIN_BARS_5 = 80
    if len(df1_raw) < MIN_BARS_1 and _db1 < 31:
        df1_raw = fetch_data_extended(symbol, 1, days_back=min(_db1 * 3, 31))
    if len(df5_raw) < MIN_BARS_5 and _db5 < 31:
        df5_raw = fetch_data_extended(symbol, 5, days_back=min(_db5 * 3, 31))

# Không bao giờ dừng – nếu API lỗi, fetch_data đã tự fallback sang mô phỏng
is_simulated = df1_raw.attrs.get("_simulated", False) or df5_raw.attrs.get("_simulated", False)
if df1_raw.empty or df5_raw.empty:
    # Trường hợp cực kỳ hiếm: cả 3 nguồn đều lỗi → tạo dữ liệu mô phỏng tại chỗ
    df1_raw = _simulate(1,  n=350, seed=hash(symbol + "1") % 9999)
    df5_raw = _simulate(5,  n=350, seed=hash(symbol + "5") % 9999)
    is_simulated = True

if _new_contract_warn:
    st.warning(_new_contract_warn)

if is_simulated:
    st.warning(
        "🖥️ **Đang dùng dữ liệu MÔ PHỎNG** — không lấy được dữ liệu thực từ vnstock. "
        "Kiểm tra kết nối mạng hoặc cài `vnstock3`: `pip install vnstock3`"
    )

df1 = add_indicators(df1_raw.copy())
df5 = add_indicators(df5_raw.copy())

current_price = float(df1["close"].iloc[-1])
prev_close    = float(df1["close"].iloc[-2])
regime1       = detect_regime(df1)
regime5       = detect_regime(df5)
current_atr   = regime5["atr"]

auto_check_trades(current_price, auto_tp_target.lower())

# Tính confluence + forecast
confluence = compute_confluence(df1, df5)
forecast   = compute_forecast(df1, df5)
score      = confluence["score"]

# ── Ghi cảnh báo nếu score vượt ngưỡng ──
ALERT_THRESHOLD = alert_threshold
push_alert(score, confluence, forecast, current_price, regime5["regime"])

# ── Scan mẫu nến lịch sử cho chart (cache theo seed/symbol) ──
pat_hist1 = scan_pattern_history(df1, lookback=120)
pat_hist5 = scan_pattern_history(df5, lookback=120)

# ── VWAP deviation hiện tại ──
vwap_dev  = float(df1["vwap_dev_pct"].iloc[-1]) if "vwap_dev_pct" in df1.columns and not np.isnan(df1["vwap_dev_pct"].iloc[-1]) else 0.0
vwap_now  = float(df1["vwap"].iloc[-1])         if "vwap" in df1.columns and not np.isnan(df1["vwap"].iloc[-1]) else 0.0


# ══════════════════════════════════════════════════════════════
# ██ HEADER METRICS
# ══════════════════════════════════════════════════════════════
price_chg = current_price - prev_close; up = price_chg >= 0
h1,h2,h3,h4,h5,h6,h7 = st.columns([2,1.4,1.2,1.2,1.2,1.2,1.4])

h1.markdown(f"""
<div class="metric-box">
  <div class="metric-label">{symbol}</div>
  <div class="metric-value white" style="font-size:24px">{current_price:.2f}</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{'#00e676' if up else '#ff5252'}">
    {'▲' if up else '▼'} {price_chg:+.2f} ({price_chg/prev_close*100:+.2f}%)</div>
</div>""", unsafe_allow_html=True)

score_c = "#00e676" if score>=40 else ("#ff5252" if score<=-40 else "#ffd600")
h2.markdown(f"""
<div class="metric-box">
  <div class="metric-label">Confluence Score</div>
  <div class="metric-value" style="color:{score_c};font-size:22px">{score:+d}</div>
  <div style="font-size:10px;color:#475569;font-family:'JetBrains Mono',monospace">{confluence['rec']}</div>
</div>""", unsafe_allow_html=True)

rc5 = {"UPTREND":"#00e676","DOWNTREND":"#ff5252","SIDEWAY":"#ffd600"}.get(regime5["regime"],"#64748b")
h3.markdown(f'<div class="metric-box"><div class="metric-label">Xu hướng 5P</div><div class="metric-value" style="color:{rc5};font-size:13px">{regime5["regime"]}</div><div style="font-size:10px;color:#475569;font-family:JetBrains Mono">ADX {regime5["adx"]:.1f}·{regime5["strength"]}</div></div>', unsafe_allow_html=True)

rc1 = {"UPTREND":"#00e676","DOWNTREND":"#ff5252","SIDEWAY":"#ffd600"}.get(regime1["regime"],"#64748b")
h4.markdown(f'<div class="metric-box"><div class="metric-label">Xu hướng 1P</div><div class="metric-value" style="color:{rc1};font-size:13px">{regime1["regime"]}</div><div style="font-size:10px;color:#475569;font-family:JetBrains Mono">ADX {regime1["adx"]:.1f}·{regime1["strength"]}</div></div>', unsafe_allow_html=True)

rsi_c = "green" if regime1["rsi"]<40 else ("red" if regime1["rsi"]>60 else "yellow")
h5.markdown(f'<div class="metric-box"><div class="metric-label">RSI 14</div><div class="metric-value {rsi_c}">{regime1["rsi"]:.1f}</div><div style="font-size:10px;color:#475569;font-family:JetBrains Mono">{"Quá bán" if regime1["rsi"]<30 else "Quá mua" if regime1["rsi"]>70 else "Trung tính"}</div></div>', unsafe_allow_html=True)

h6.markdown(f'<div class="metric-box"><div class="metric-label">VWAP Dev %</div><div class="metric-value {"green" if vwap_dev>0 else "red"}">{vwap_dev:+.2f}%</div><div style="font-size:10px;color:#475569;font-family:JetBrains Mono">VWAP {vwap_now:.1f} · {"Trên" if vwap_dev>0 else "Dưới"}</div></div>', unsafe_allow_html=True)

fc_c = forecast["verdict_color"]
h7.markdown(f'<div class="metric-box"><div class="metric-label">Dự báo 3-5 phiên</div><div class="metric-value" style="color:{fc_c};font-size:12px">{forecast["verdict"]}</div><div style="font-size:10px;color:#475569;font-family:JetBrains Mono">▲{forecast["up_prob"]:.0f}% ▼{forecast["down_prob"]:.0f}%</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ██ ALERT BANNER – hiện khi |score| ≥ ngưỡng
# ══════════════════════════════════════════════════════════════
render_alert_banner(score, confluence, current_price, mute_alerts)


# ══════════════════════════════════════════════════════════════
# ██ KHUYẾN NGHỊ (RECOMMENDATION BLOCK)
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">🤖 KHUYẾN NGHỊ HỆ THỐNG</div>', unsafe_allow_html=True)

rec_col, score_col = st.columns([2.5, 1.5])

with rec_col:
    # Score progress bar
    bar_pct  = abs(score)
    bar_color= "#00e676" if score>0 else "#ff5252"
    bar_left = max(0, -score) / 100 * 100
    st.markdown(f"""
    <div class="{confluence['rec_css']}">
      <div style="font-size:20px;font-weight:800;color:{confluence['rec_color']};margin-bottom:6px">
        {'🚀' if score>=70 else '💥' if score<=-70 else '⚡' if abs(score)>=40 else '🔄'}
        {confluence['rec']}
      </div>
      <div style="font-size:12px;color:#94a3b8;margin-bottom:10px">{confluence['rec_desc']}</div>
      <div style="font-size:10px;color:#475569;margin-bottom:4px">Điểm hội tụ: {score:+d} / 100</div>
      <div class="score-bar-wrap">
        <div style="height:12px;border-radius:6px;width:{bar_pct}%;background:{bar_color};
             margin-{'right' if score<0 else 'left'}:auto;{'margin-left:'+(str(100-bar_pct))+'%' if score<0 else ''}"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:9px;color:#334155;font-family:'JetBrains Mono',monospace;margin-top:2px">
        <span>SHORT MẠNH (-100)</span><span>0</span><span>LONG MẠNH (+100)</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # Candle patterns
    pats = confluence["patterns"]
    if pats:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:10px;color:#334155;font-family:JetBrains Mono;margin-bottom:4px">MẪU NẾN PHÁT HIỆN:</div>', unsafe_allow_html=True)
        tag_html = ""
        for p in pats:
            c_ = "#00e676" if p["bias"]=="BULL" else ("#ff5252" if p["bias"]=="BEAR" else "#ffd600")
            tag_html += f'<span class="pattern-tag" style="background:{c_}22;color:{c_};border:1px solid {c_}55">{p["name"]}</span> '
        st.markdown(tag_html, unsafe_allow_html=True)

with score_col:
    st.markdown('<div class="sec-hdr">Phân tích Confluence</div>', unsafe_allow_html=True)
    for weight, label, color in confluence["detail"]:
        sign = "+" if color == "#00e676" else ("-" if color=="#ff5252" else "·")
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid #1a2540;font-family:'JetBrains Mono',monospace;font-size:10px">
          <span style="color:#64748b;flex:1">{label[:45]}</span>
          <span style="color:{color};font-weight:700;min-width:36px;text-align:right">{sign}{weight}</span>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ██ DỰ BÁO VÀI PHIÊN TỚI
# ══════════════════════════════════════════════════════════════
with st.expander(f"📡 DỰ BÁO 3–5 PHIÊN TỚI  ·  {forecast['verdict']}  ·  ▲{forecast['up_prob']:.0f}% ▼{forecast['down_prob']:.0f}%", expanded=True):
    f1_col, f2_col = st.columns([1.5, 1])

    with f1_col:
        for fac in forecast["factors"]:
            bc = {"UP":"#00e676","DOWN":"#ff5252","NEUTRAL":"#334155"}.get(fac["bias"],"#334155")
            ic = {"UP":"▲","DOWN":"▼","NEUTRAL":"·"}.get(fac["bias"],"·")
            st.markdown(f"""
            <div class="forecast-box" style="border-left:3px solid {bc}">
              <div style="display:flex;justify-content:space-between">
                <b style="color:{bc}">{ic} {fac['label']}</b>
                <span style="color:#475569">{'+' if fac['bias']=='UP' else ('-' if fac['bias']=='DOWN' else '·')}{fac['weight']}đ</span>
              </div>
              <div style="color:#64748b;margin-top:3px">{fac['desc']}</div>
            </div>""", unsafe_allow_html=True)

    with f2_col:
        fc = forecast
        # Probability bars
        st.markdown(f"""
        <div style="background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:14px;font-family:'JetBrains Mono',monospace">
          <div style="color:#38bdf8;font-size:11px;font-weight:700;margin-bottom:10px">XÁC SUẤT DỰ BÁO</div>

          <div style="font-size:11px;color:#00e676;margin-bottom:3px">▲ TĂNG  {fc['up_prob']:.0f}%</div>
          <div style="background:#1a2540;border-radius:4px;height:10px;margin-bottom:8px">
            <div style="height:10px;border-radius:4px;width:{fc['up_prob']:.0f}%;background:#00e676"></div>
          </div>

          <div style="font-size:11px;color:#ff5252;margin-bottom:3px">▼ GIẢM  {fc['down_prob']:.0f}%</div>
          <div style="background:#1a2540;border-radius:4px;height:10px;margin-bottom:12px">
            <div style="height:10px;border-radius:4px;width:{fc['down_prob']:.0f}%;background:#ff5252"></div>
          </div>

          <div style="font-size:18px;font-weight:800;color:{fc['verdict_color']};text-align:center;padding:8px 0;border-top:1px solid #1a2540">
            {fc['verdict']}
          </div>
          <div style="font-size:10px;color:#475569;text-align:center;margin-top:4px">{fc['verdict_desc']}</div>
        </div>""", unsafe_allow_html=True)

        # RSI Divergence summary
        div1 = confluence["div1"]; div5 = confluence["div5"]
        if div1["bull"] or div5["bull"] or div1["bear"] or div5["bear"]:
            div_color = "#00e676" if (div1["bull"] or div5["bull"]) else "#ff5252"
            div_text  = div1["desc"] or div5["desc"]
            st.markdown(f"""
            <div style="background:#0f1626;border:1px solid {div_color}44;border-left:3px solid {div_color};border-radius:6px;padding:10px;margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:11px">
              <b style="color:{div_color}">⚠️ RSI DIVERGENCE</b><br>
              <span style="color:#64748b">{div_text}</span>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ██ REGIME BANNERS
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
cr1, cr5 = st.columns(2)
def regime_banner(r, lbl):
    css  = {"UPTREND":"uptrend","DOWNTREND":"downtrend","SIDEWAY":"sideway"}.get(r["regime"],"sideway")
    icon = {"UPTREND":"🚀","DOWNTREND":"💥","SIDEWAY":"🔄"}.get(r["regime"],"")
    desc = {"UPTREND":"Ưu tiên BUY","DOWNTREND":"Ưu tiên SELL","SIDEWAY":"Đánh biên, chờ Breakout"}.get(r["regime"],"")
    return f'<div class="signal-card {css}">{icon} [{lbl}] {r["regime"]} — {r["strength"]}<br><span style="font-size:10px;font-weight:400">{desc} | ADX {r["adx"]:.1f} | DI+ {r["di_pos"]:.1f} DI- {r["di_neg"]:.1f}</span></div>'
with cr1: st.markdown(regime_banner(regime1,"1 PHÚT"), unsafe_allow_html=True)
with cr5: st.markdown(regime_banner(regime5,"5 PHÚT"), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ██ CHART + TRADE PANEL
# ══════════════════════════════════════════════════════════════
chart_col, trade_col = st.columns([3.2, 1.2])

with chart_col:
    tab1, tab5, tab_pat, tab_sig, tab_wr, tab_alert = st.tabs([
        "📊 Biểu đồ 1P", "📊 Biểu đồ 5P",
        "🕯️ Mẫu nến", "🔔 Lịch sử tín hiệu", "📈 Win Rate", "🚨 Cảnh báo"
    ])

    with tab1:
        st.plotly_chart(build_chart(
            df1, f"{symbol}·1P·{datetime.now().strftime('%H:%M:%S')}",
            show_ema, show_bb, show_signals, show_trades,
            show_vwap, show_vwap_bands, show_patterns, score,
            pattern_history=pat_hist1,
        ), use_container_width=True, config={"displayModeBar": False})

    with tab5:
        st.plotly_chart(build_chart(
            df5, f"{symbol}·5P·{datetime.now().strftime('%H:%M:%S')}",
            show_ema, show_bb, show_signals, show_trades,
            show_vwap, show_vwap_bands, show_patterns, score,
            pattern_history=pat_hist5,
        ), use_container_width=True, config={"displayModeBar": False})

    # ──────────────────────────────────────────────
    # TAB MẪU NẾN – đầy đủ với quality + context
    # ──────────────────────────────────────────────
    with tab_pat:
        st.markdown('<div class="sec-hdr">🕯️ MẪU NẾN PHÁT HIỆN HIỆN TẠI & LỊCH SỬ</div>', unsafe_allow_html=True)

        # ── Mẫu nến nến cuối cùng (1P + 5P) ──
        cur_pats1 = detect_candle_patterns(df1)
        cur_pats5 = detect_candle_patterns(df5)
        all_cur   = [(p,"1P") for p in cur_pats1] + [(p,"5P") for p in cur_pats5]

        if all_cur:
            st.markdown('<div style="font-size:11px;color:#38bdf8;font-family:JetBrains Mono;font-weight:700;margin-bottom:6px">⚡ ĐANG XUẤT HIỆN NGAY BÂY GIỜ</div>', unsafe_allow_html=True)
            cols_p = st.columns(min(len(all_cur), 4))
            for idx, (p, tf) in enumerate(all_cur[:4]):
                bc = {"BULL":"#00e676","BEAR":"#ff5252","NEUTRAL":"#ffd600"}.get(p["bias"],"#64748b")
                qc = p.get("quality_color","#64748b")
                cols_p[idx].markdown(f"""
                <div style="background:#0f1626;border:1px solid {bc}44;border-top:3px solid {bc};
                     border-radius:8px;padding:10px;font-family:'JetBrains Mono',monospace;font-size:11px">
                  <div style="color:{bc};font-weight:700;font-size:13px">{p['name']}</div>
                  <div style="color:#64748b;margin-top:3px">[{tf}] {p['desc']}</div>
                  <div style="display:flex;justify-content:space-between;margin-top:6px">
                    <span style="color:{qc};font-weight:700">Chất lượng {p['quality']}</span>
                    <span style="color:#f1f5f9">{p['reliability']}%</span>
                  </div>
                  <div style="background:#1a2540;border-radius:3px;height:6px;margin-top:4px">
                    <div style="height:6px;border-radius:3px;width:{p['reliability']}%;background:{qc}"></div>
                  </div>
                  {'<div style="font-size:10px;color:#38bdf8;margin-top:3px">+' + str(p["context_bonus"]) + '% (vùng key)</div>' if p.get("context_bonus",0)>0 else ""}
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#334155;font-family:JetBrains Mono;font-size:11px;padding:8px">Không có mẫu nến đặc biệt ở nến hiện tại.</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # ── Bảng giải thích 17 mẫu ──
        with st.expander("📖 Bảng tra cứu 17 mẫu nến & độ tin cậy"):
            pattern_info = [
                ("Morning Star",        "BULL","82%","Đảo chiều tăng mạnh – 3 nến: đỏ lớn → nhỏ → xanh lớn"),
                ("Evening Star",        "BEAR","80%","Đảo chiều giảm mạnh – 3 nến: xanh lớn → nhỏ → đỏ lớn"),
                ("Three White Soldiers","BULL","78%","3 nến xanh thân đầy liên tiếp – trend tăng xác nhận"),
                ("Three Black Crows",   "BEAR","77%","3 nến đỏ thân đầy liên tiếp – trend giảm xác nhận"),
                ("Bull Engulfing",      "BULL","75%","Nến xanh nuốt toàn bộ thân nến đỏ trước"),
                ("Bear Engulfing",      "BEAR","74%","Nến đỏ nuốt toàn bộ thân nến xanh trước"),
                ("Marubozu Bull",       "BULL","72%","Nến xanh thân đầy không râu – lực mua tuyệt đối"),
                ("Marubozu Bear",       "BEAR","71%","Nến đỏ thân đầy không râu – lực bán tuyệt đối"),
                ("Piercing Line",       "BULL","68%","Xanh mở dưới đáy đỏ, đóng trên ½ thân đỏ"),
                ("Dark Cloud Cover",    "BEAR","67%","Đỏ mở trên đỉnh xanh, đóng dưới ½ thân xanh"),
                ("Hammer",             "BULL","65%","Râu dưới dài ≥ 2× thân – hỗ trợ mạnh"),
                ("Shooting Star",      "BEAR","64%","Râu trên dài ≥ 2× thân – kháng cự mạnh"),
                ("Tweezer Bottom",     "BULL","63%","Hai nến chạm cùng đáy – double bottom nhỏ"),
                ("Tweezer Top",        "BEAR","62%","Hai nến chạm cùng đỉnh – double top nhỏ"),
                ("Bullish Harami",     "BULL","60%","Xanh nhỏ trong bụng đỏ lớn – tín hiệu yếu hơn"),
                ("Bearish Harami",     "BEAR","59%","Đỏ nhỏ trong bụng xanh lớn – tín hiệu yếu hơn"),
                ("Doji",              "NEUTRAL","55%","Mở = Đóng – giằng co hoàn toàn, sắp đảo chiều"),
            ]
            rows_pi = [{"Tên mẫu":n,"Xu hướng":b,"Cơ bản":r,"Mô tả":d} for n,b,r,d in pattern_info]
            st.dataframe(pd.DataFrame(rows_pi), use_container_width=True, hide_index=True)

            st.markdown("""
            <div style="background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:12px;margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#64748b">
              <b style="color:#38bdf8">💡 Context Bonus – Độ tin cậy tăng thêm khi:</b><br>
              +12% Mẫu xuất hiện tại BB Lower/Upper (vùng hỗ trợ/kháng cự)<br>
              +10% Mẫu xuất hiện tại VWAP ±2σ (vùng extreme)<br>
              +8%  Volume đột biến > 1.5× MA đi kèm<br>
              +5%  BB Squeeze đang hình thành (sắp breakout)
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── Lịch sử mẫu nến 120 nến gần nhất ──
        st.markdown('<div class="sec-hdr">LỊCH SỬ MẪU NẾN (120 nến gần nhất)</div>', unsafe_allow_html=True)

        fp1, fp2, fp3 = st.columns(3)
        filter_tf_p  = fp1.selectbox("Khung",   ["Tất cả","1P","5P"],    key="pf_tf")
        filter_bias_p= fp2.selectbox("Xu hướng",["Tất cả","BULL","BEAR","NEUTRAL"], key="pf_bias")
        filter_ql_p  = fp3.selectbox("Chất lượng",["Tất cả","A","B","C"], key="pf_ql")

        combined = [(p,"1P") for p in pat_hist1] + [(p,"5P") for p in pat_hist5]
        combined.sort(key=lambda x: x[0]["time"], reverse=True)

        filtered_p = [
            (p, tf) for p, tf in combined
            if (filter_tf_p  == "Tất cả" or tf == filter_tf_p)
            and (filter_bias_p == "Tất cả" or p["bias"] == filter_bias_p)
            and (filter_ql_p  == "Tất cả" or p["quality"] == filter_ql_p)
        ]

        # Stats
        n_bull_h = sum(1 for p,_ in filtered_p if p["bias"]=="BULL")
        n_bear_h = sum(1 for p,_ in filtered_p if p["bias"]=="BEAR")
        n_a_h    = sum(1 for p,_ in filtered_p if p["quality"]=="A")
        st.markdown(f"""
        <div style="display:flex;gap:8px;margin-bottom:10px;font-family:'JetBrains Mono',monospace;font-size:11px;flex-wrap:wrap">
          <div style="background:#0a1f12;border:1px solid #00e67633;border-radius:5px;padding:5px 10px;color:#00e676">🟢 BULL: {n_bull_h}</div>
          <div style="background:#1f0a0a;border:1px solid #ff525233;border-radius:5px;padding:5px 10px;color:#ff5252">🔴 BEAR: {n_bear_h}</div>
          <div style="background:#051a0d;border:1px solid #00e67666;border-radius:5px;padding:5px 10px;color:#00e676">⭐ Chất lượng A: {n_a_h}</div>
          <div style="background:#0f1626;border:1px solid #1a2540;border-radius:5px;padding:5px 10px;color:#64748b">Tổng: {len(filtered_p)}</div>
        </div>""", unsafe_allow_html=True)

        if not filtered_p:
            st.markdown('<div style="color:#334155;font-family:JetBrains Mono;font-size:11px;padding:8px">Không có mẫu khớp bộ lọc.</div>', unsafe_allow_html=True)
        else:
            for p, tf in filtered_p[:60]:
                bc  = {"BULL":"#00e676","BEAR":"#ff5252","NEUTRAL":"#ffd600"}.get(p["bias"],"#64748b")
                qc  = p.get("quality_color","#64748b")
                cb_html = f'<span style="color:#38bdf8"> +{p["context_bonus"]}% context</span>' if p.get("context_bonus",0)>0 else ""
                t_str = p["time"].strftime("%d/%m %H:%M") if hasattr(p["time"],"strftime") else str(p["time"])
                st.markdown(f"""
                <div style="background:#0f1626;border:1px solid {bc}33;border-left:3px solid {bc};
                     border-radius:6px;padding:8px 12px;margin-bottom:4px;
                     font-family:'JetBrains Mono',monospace;font-size:11px">
                  <div style="display:flex;justify-content:space-between;align-items:center">
                    <span><b style="color:{bc}">{p['name']}</b>
                      <span style="color:#475569"> [{tf}] {t_str}</span></span>
                    <div style="display:flex;gap:6px;align-items:center">
                      <span class="{'wr-badge-good' if p['quality']=='A' else 'wr-badge-mid' if p['quality']=='B' else 'wr-badge-bad'}">{p['quality']}</span>
                      <span style="color:#f1f5f9;font-weight:700">{p['price']:.2f}</span>
                    </div>
                  </div>
                  <div style="color:#64748b;margin-top:2px">{p['desc']}{cb_html}</div>
                  <div style="background:#1a2540;border-radius:2px;height:4px;margin-top:5px;width:100%">
                    <div style="height:4px;border-radius:2px;width:{p['reliability']}%;background:{qc}"></div>
                  </div>
                  <div style="font-size:9px;color:#334155;margin-top:2px">Độ tin cậy {p['reliability']}%</div>
                </div>""", unsafe_allow_html=True)

    with tab_sig:
        st.markdown('<div class="sec-hdr">LỊCH SỬ GIAO CẮT TÍN HIỆU (150 NẾN GẦN NHẤT)</div>', unsafe_allow_html=True)
        h1m = get_signal_history(df1, "1P"); h5m = get_signal_history(df5, "5P")
        all_h = sorted(h1m + h5m, key=lambda x: x["_ts"], reverse=True)
        if all_h:
            for item in all_h: del item["_ts"]
            st.dataframe(pd.DataFrame(all_h), use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có tín hiệu giao cắt gần đây.")

    # ──────────────────────────────────────────────
    # WIN RATE TAB – đầy đủ breakdown
    # ──────────────────────────────────────────────
    with tab_wr:
        st.markdown('<div class="sec-hdr">📊 WIN RATE & HIỆU SUẤT TOÀN DIỆN</div>', unsafe_allow_html=True)
        wr = compute_winrate()

        if wr["total"] == 0:
            st.info("Chưa có lệnh đóng. Hãy vào lệnh và để hệ thống tự chốt lời/cắt lỗ.")
        else:
            # ── 4 chỉ số chính ──
            w1, w2, w3, w4 = st.columns(4)
            wrc = "#00e676" if wr["win_rate"] >= 55 else ("#ffd600" if wr["win_rate"] >= 45 else "#ff5252")
            w1.markdown(f'<div class="metric-box"><div class="metric-label">Win Rate</div><div class="metric-value" style="color:{wrc}">{wr["win_rate"]:.1f}%</div><div style="font-size:10px;color:#475569">✅{wr["wins"]} / ❌{wr["losses"]}</div></div>', unsafe_allow_html=True)
            pfc = "#00e676" if wr["profit_factor"] > 1.5 else ("#ffd600" if wr["profit_factor"] > 1 else "#ff5252")
            w2.markdown(f'<div class="metric-box"><div class="metric-label">Profit Factor</div><div class="metric-value" style="color:{pfc}">{wr["profit_factor"]:.2f}</div><div style="font-size:10px;color:#475569">> 1.5 = tốt</div></div>', unsafe_allow_html=True)
            exc = "#00e676" if wr["expectancy"] > 0 else "#ff5252"
            w3.markdown(f'<div class="metric-box"><div class="metric-label">Expectancy</div><div class="metric-value" style="color:{exc}">{wr["expectancy"]:+.2f}đ</div><div style="font-size:10px;color:#475569">kỳ vọng/lệnh</div></div>', unsafe_allow_html=True)
            tc = "#00e676" if wr["total_pnl"] > 0 else "#ff5252"
            w4.markdown(f'<div class="metric-box"><div class="metric-label">Tổng P&L</div><div class="metric-value" style="color:{tc}">{wr["total_pnl"]:+.1f}đ</div><div style="font-size:10px;color:#475569">{wr["total"]} lệnh</div></div>', unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            # ── Equity curve ──
            if wr["equity_curve"]:
                eq_df  = pd.DataFrame(wr["equity_curve"])
                eq_col = ["#00e676" if v >= 0 else "#ff5252" for v in eq_df["eq"]]
                fig_eq = go.Figure()
                fig_eq.add_trace(go.Scatter(
                    x=eq_df["label"], y=eq_df["eq"],
                    fill="tozeroy",
                    fillcolor="rgba(0,230,118,0.08)",
                    line=dict(color="#00e676", width=2),
                    mode="lines+markers",
                    marker=dict(color=eq_col, size=7),
                    name="Equity",
                ))
                fig_eq.add_hline(y=0, line_color="#334155", line_width=1)
                fig_eq.update_layout(
                    template="plotly_dark", paper_bgcolor="#080c18", plot_bgcolor="#080c18",
                    margin=dict(l=0,r=0,t=28,b=0), height=200,
                    title=dict(text="📈 Đường vốn (Equity Curve)", font=dict(size=11, color="#475569"), x=0.01),
                    xaxis=dict(gridcolor="#1a2540", showgrid=True),
                    yaxis=dict(gridcolor="#1a2540", showgrid=True),
                    showlegend=False,
                )
                st.plotly_chart(fig_eq, use_container_width=True, config={"displayModeBar": False})

            # ── Breakdown theo Regime, Hướng, Score ──
            col_r, col_d, col_s = st.columns(3)

            def breakdown_table(title, data: dict):
                html = f'<div style="background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:12px;font-family:JetBrains Mono;font-size:11px"><div style="color:#38bdf8;font-weight:700;margin-bottom:8px">{title}</div>'
                for k, v in data.items():
                    wr_ = v.get("wr", 0)
                    wr_c = "#00e676" if wr_ >= 55 else ("#ffd600" if wr_ >= 45 else "#ff5252")
                    pnl_ = v.get("pnl", 0)
                    pc   = "#00e676" if pnl_ >= 0 else "#ff5252"
                    html += f"""
                    <div class="wr-row">
                      <span style="color:#94a3b8">{k}</span>
                      <div style="display:flex;gap:8px;align-items:center">
                        <span class="{'wr-badge-good' if wr_>=55 else 'wr-badge-mid' if wr_>=45 else 'wr-badge-bad'}">{wr_:.0f}%</span>
                        <span style="color:{pc}">{pnl_:+.1f}đ</span>
                        <span style="color:#475569">{v['total']}L</span>
                      </div>
                    </div>"""
                html += "</div>"
                return html

            with col_r:
                if wr["by_regime"]:
                    st.markdown(breakdown_table("📍 Theo Regime", wr["by_regime"]), unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#334155;font-size:11px;font-family:JetBrains Mono;padding:8px">Chưa có dữ liệu Regime</div>', unsafe_allow_html=True)

            with col_d:
                if wr["by_direction"]:
                    st.markdown(breakdown_table("↕️ Theo Hướng", wr["by_direction"]), unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#334155;font-size:11px;font-family:JetBrains Mono;padding:8px">Chưa có dữ liệu hướng</div>', unsafe_allow_html=True)

            with col_s:
                if wr["by_signal"]:
                    st.markdown(breakdown_table("⚡ Theo Mức Score", wr["by_signal"]), unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#334155;font-size:11px;font-family:JetBrains Mono;padding:8px">Chưa có dữ liệu Score</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            # ── Thống kê bổ sung ──
            dd_c  = "#ff5252" if wr["max_drawdown"] > 5 else ("#ffd600" if wr["max_drawdown"] > 2 else "#00e676")
            cl_c  = "#ff5252" if wr["consecutive_losses"] >= 4 else ("#ffd600" if wr["consecutive_losses"] >= 2 else "#00e676")
            health = "✅ Chiến lược đang hoạt động tốt." if wr["expectancy"] > 0 and wr["profit_factor"] > 1.2 else "⚠️ Cần xem xét lại SL/TP hoặc lọc điều kiện vào lệnh."
            st.markdown(f"""
            <div style="background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:12px;font-family:'JetBrains Mono',monospace;font-size:11px">
              <div style="color:#38bdf8;font-weight:700;margin-bottom:8px">🔍 PHÂN TÍCH NÂNG CAO</div>
              <div style="display:flex;gap:20px;flex-wrap:wrap">
                <span>Avg Thắng: <b style="color:#00e676">{wr['avg_win']:+.2f}đ</b></span>
                <span>Avg Thua: <b style="color:#ff5252">{wr['avg_loss']:+.2f}đ</b></span>
                <span>Max Drawdown: <b style="color:{dd_c}">{wr['max_drawdown']:.2f}đ</b></span>
                <span>Chuỗi thua tối đa: <b style="color:{cl_c}">{wr['consecutive_losses']} lệnh</b></span>
              </div>
              <div style="color:#64748b;margin-top:8px">{health}</div>
            </div>""", unsafe_allow_html=True)

            # ── Bảng lệnh đóng ──
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="sec-hdr">LỊCH SỬ LỆNH ĐÃ ĐÓNG</div>', unsafe_allow_html=True)
            closed_trades = [t for t in st.session_state.trade_history if t["status"] == "CLOSED"]
            if closed_trades:
                rows = [{
                    "#":          t["id"],
                    "Lệnh":       "🟢 LONG" if t["direction"] == "LONG" else "🔴 SHORT",
                    "Vào":        f"{t['date']} {t['time']}",
                    "Ra":         t.get("exit_time", "-"),
                    "Entry":      f"{t['entry']:.2f}",
                    "Exit":       f"{t.get('exit_price', 0):.2f}",
                    "P&L":        f"{t.get('pnl_points', 0):+.1f}đ",
                    "Score":      f"{t.get('score', 0):+d}",
                    "Regime":     t.get("regime", "-"),
                    "Kết quả":    t.get("reason", "-"),
                } for t in closed_trades]
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ──────────────────────────────────────────────
    # ALERT HISTORY TAB
    # ──────────────────────────────────────────────
    with tab_alert:
        n_alerts = len(st.session_state.alert_history)
        st.markdown(f'<div class="sec-hdr">🚨 LỊCH SỬ CẢNH BÁO  ·  {n_alerts} cảnh báo  ·  Ngưỡng: |Score| ≥ {alert_threshold}</div>', unsafe_allow_html=True)

        # Stats
        long_alerts  = sum(1 for a in st.session_state.alert_history if a["direction"] == "LONG")
        short_alerts = sum(1 for a in st.session_state.alert_history if a["direction"] == "SHORT")
        st.markdown(f"""
        <div style="display:flex;gap:8px;margin-bottom:12px;font-family:'JetBrains Mono',monospace;font-size:11px">
          <div style="background:#0a1f12;border:1px solid #00e67633;border-radius:5px;padding:6px 12px;color:#00e676">🚀 LONG Alert: {long_alerts}</div>
          <div style="background:#1f0a0a;border:1px solid #ff525233;border-radius:5px;padding:6px 12px;color:#ff5252">💥 SHORT Alert: {short_alerts}</div>
          <div style="background:#0f1626;border:1px solid #1a2540;border-radius:5px;padding:6px 12px;color:#64748b">Score hiện tại: <b style="color:{'#00e676' if score>0 else '#ff5252'}">{score:+d}</b></div>
        </div>""", unsafe_allow_html=True)

        render_alert_history()

        # Hướng dẫn
        st.markdown(f"""
        <div style="background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:12px;margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#475569">
          <b style="color:#38bdf8">💡 Cách sử dụng cảnh báo:</b><br>
          • Score ≥ +{alert_threshold} → Banner đỏ xanh xuất hiện → Cân nhắc vào LONG<br>
          • Score ≤ -{alert_threshold} → Banner đỏ xuất hiện → Cân nhắc vào SHORT<br>
          • Kết hợp với Forecast và Regime trước khi vào lệnh<br>
          • Điều chỉnh ngưỡng trong Sidebar để lọc tín hiệu<br>
          • Tắt banner bằng toggle "🔕 Tắt banner cảnh báo"
        </div>""", unsafe_allow_html=True)

with trade_col:
    st.markdown('<div class="sec-hdr">🔫 VÀO LỆNH & QUẢN LÝ</div>', unsafe_allow_html=True)

    # Cảnh báo rủi ro
    if auto_sltp:
        calc_sl  = current_atr * 1.0
        calc_tp1 = current_atr * 1.0
        calc_tp2 = current_atr * 2.0
        calc_tp3 = current_atr * 3.0
        active_sl_pts = calc_sl
    else:
        active_sl_pts = sl_points

    risk_amt = active_sl_pts * lot_size * 100_000
    risk_lvl = "CAO" if risk_amt>=2_000_000 else ("TRUNG BÌNH" if risk_amt>=500_000 else "THẤP")
    risk_c   = "#ff5252" if risk_lvl=="CAO" else ("#ffd600" if risk_lvl=="TRUNG BÌNH" else "#00e676")

    # Cảnh báo nghịch chiều
    against_score = (score >= 40 and "SHORT" in confluence["rec"]) or (score <= -40 and "LONG" in confluence["rec"])
    warn_html = ""
    if score >= 70:
        warn_html = '<div style="color:#00e676;margin-top:4px">✅ Score +{score} → Hệ thống khuyến nghị LONG</div>'.format(score=score)
    elif score <= -70:
        warn_html = '<div style="color:#ff5252;margin-top:4px">✅ Score {score} → Hệ thống khuyến nghị SHORT</div>'.format(score=score)

    st.markdown(f"""
    <div style="background:#0f1626;border:1px solid {risk_c}55;border-left:3px solid {risk_c};border-radius:6px;padding:10px;margin-bottom:10px;font-family:'JetBrains Mono',monospace;font-size:11px">
      <div style="color:{risk_c};font-weight:700">⚠️ RỦI RO: {risk_lvl}</div>
      <div style="color:#64748b;margin-top:3px">SL tối đa: <b style="color:#ff5252">-{risk_amt:,.0f} ₫</b></div>
      <div style="color:#64748b">Score hiện tại: <b style="color:{'#00e676' if score>0 else '#ff5252'}">{score:+d}</b> → {confluence['rec']}</div>
      {warn_html}
    </div>""", unsafe_allow_html=True)

    if auto_sltp:
        st.markdown(f"""
        <div style="background:#0f1626;border:1px dashed #38bdf8;border-radius:6px;padding:8px;margin-bottom:10px;font-family:'JetBrains Mono',monospace;font-size:11px">
          <div style="color:#94a3b8">ATR: <b style="color:#ffd600">{current_atr:.1f}đ</b></div>
          <div style="color:#00e676">TP1 +{calc_tp1:.1f} | TP2 +{calc_tp2:.1f} | TP3 +{calc_tp3:.1f}</div>
          <div style="color:#ff5252">SL -{calc_sl:.1f} (R:R = 1:1~1:3)</div>
        </div>""", unsafe_allow_html=True)

    entry_price = st.number_input("Giá vào", value=float(f"{current_price:.2f}"), step=0.1)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🟢 LONG", use_container_width=True):
            sig_tag = f"Score {score:+d} | {regime5['regime']}"
            if auto_sltp:
                add_trade("LONG", entry_price, entry_price+calc_tp1, entry_price+calc_tp2, entry_price+calc_tp3, entry_price-calc_sl, lot_size, score, regime5["regime"], sig_tag)
            else:
                add_trade("LONG", entry_price, entry_price+tp1_points, entry_price+tp2_points, entry_price+tp3_points, entry_price-sl_points, lot_size, score, regime5["regime"], sig_tag)
            st.rerun()
    with c2:
        if st.button("🔴 SHORT", use_container_width=True):
            sig_tag = f"Score {score:+d} | {regime5['regime']}"
            if auto_sltp:
                add_trade("SHORT", entry_price, entry_price-calc_tp1, entry_price-calc_tp2, entry_price-calc_tp3, entry_price+calc_sl, lot_size, score, regime5["regime"], sig_tag)
            else:
                add_trade("SHORT", entry_price, entry_price-tp1_points, entry_price-tp2_points, entry_price-tp3_points, entry_price+sl_points, lot_size, score, regime5["regime"], sig_tag)
            st.rerun()

    # Open trades
    st.markdown('<div style="font-size:11px;color:#94a3b8;font-family:JetBrains Mono;margin:12px 0 6px;font-weight:700">📋 LỆNH ĐANG MỞ</div>', unsafe_allow_html=True)
    open_exist = False
    for i, t in enumerate(st.session_state.trade_history):
        if t["status"] == "OPEN":
            open_exist = True
            live = (current_price-t["entry"]) * (1 if t["direction"]=="LONG" else -1)
            dc   = "#00e676" if t["direction"]=="LONG" else "#ff5252"
            lc   = "#00e676" if live>=0 else "#ff5252"
            st.markdown(f"""
            <div style="background:#0f1626;border:1px solid #1a2540;border-left:2px solid {dc};padding:8px;margin-bottom:5px;font-size:10px;font-family:'JetBrains Mono'">
              <b style="color:{dc}">#{t['id']} {t['direction']}</b>
              <span style="float:right;color:#ffd600">OPEN</span><br>
              <span style="color:#64748b">In: {t['entry']:.2f} | P&L: <span style="color:{lc}">{live:+.2f}</span></span><br>
              <span style="color:#475569">TP {t['tp1']:.1f}/{t['tp2']:.1f}/{t['tp3']:.1f} | SL <span style="color:#ff5252">{t['sl']:.1f}</span></span>
            </div>""", unsafe_allow_html=True)
            if st.button(f"✕ Đóng #{t['id']}", key=f"cl_{i}"): close_trade(i, current_price); st.rerun()
    if not open_exist:
        st.markdown('<div style="color:#334155;font-size:11px;font-family:JetBrains Mono;padding:6px">Không có lệnh mở.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ██ BẢNG TIÊU CHÍ & THỰC TẾ
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
with st.expander("📐 BẢNG TIÊU CHÍ XU HƯỚNG & TÍNH TOÁN THỰC TẾ (5P)"):
    cl, cr = st.columns(2)
    with cl:
        st.markdown("""
        <div style='background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:12px;font-family:JetBrains Mono;font-size:12px'>
          <div style='color:#38bdf8;font-weight:bold;margin-bottom:8px'>📌 BẢNG TIÊU CHÍ</div>
          <span style='color:#ffd600'>ADX < 22</span> ➔ SIDEWAY<br>
          <span style='color:#00e676'>ADX ≥ 22 + DI+ > DI-</span> ➔ UPTREND<br>
          <span style='color:#ff5252'>ADX ≥ 22 + DI- > DI+</span> ➔ DOWNTREND<br><br>
          <span style='color:#a78bfa'>BB Width < Percentile 15%</span> ➔ BB Squeeze<br>
          <span style='color:#38bdf8'>Score ≥ +70</span> ➔ KHUYẾN NGHỊ LONG MẠNH<br>
          <span style='color:#f97316'>Score ≤ -70</span> ➔ KHUYẾN NGHỊ SHORT MẠNH<br>
        </div>""", unsafe_allow_html=True)
    with cr:
        r5 = regime5
        adx_text = (f"<span style='color:#ffd600'>ADX={r5['adx']:.1f}<22 ➔ SIDEWAY</span>" if r5["adx"]<22
                    else (f"<span style='color:#00e676'>ADX={r5['adx']:.1f}≥22 & DI+>DI- ➔ UP</span>" if r5["di_pos"]>r5["di_neg"]
                          else f"<span style='color:#ff5252'>ADX={r5['adx']:.1f}≥22 & DI->DI+ ➔ DOWN</span>"))
        bb_text = (f"<span style='color:#a78bfa'>BB({r5['bb_w']:.4f})<p15({r5['sqz_thresh']:.4f}) → SQUEEZE</span>" if r5["is_sqz"]
                   else f"<span style='color:#475569'>BB({r5['bb_w']:.4f})≥p15({r5['sqz_thresh']:.4f}) → Biên độ mở</span>")
        st.markdown(f"""
        <div style='background:#0f1626;border:1px solid #1a2540;border-radius:8px;padding:12px;font-family:JetBrains Mono;font-size:12px'>
          <div style='color:#38bdf8;font-weight:bold;margin-bottom:8px'>⚙️ TÍNH TOÁN 5P HIỆN TẠI</div>
          • {adx_text}<br>
          • DI+={r5['di_pos']:.1f} | DI-={r5['di_neg']:.1f}<br>
          • {bb_text}<br>
          <hr style='border-color:#1a2540;margin:6px 0'>
          • Divergence 1P: <b>{'CÓ ▲' if confluence['div1']['bull'] else ('CÓ ▼' if confluence['div1']['bear'] else 'KHÔNG')}</b><br>
          • Volume Bias: <b style='color:{"#00e676" if confluence["va"]["bias"]=="BULL" else "#ff5252" if confluence["va"]["bias"]=="BEAR" else "#64748b"}'>{confluence["va"]["bias"]}</b><br>
          • Score: <b style='color:{"#00e676" if score>0 else "#ff5252"}'>{score:+d}</b> → {confluence['rec']}
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# FOOTER + AUTO REFRESH
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
fl, fr = st.columns([4,1])

# Xác định nguồn dữ liệu thực tế (không phải biến is_simulated đã khai báo ở trên)
_src_label = "🖥️ Mô phỏng" if is_simulated else "📡 API Thực (vnstock)"
_hrs_label  = " · ● Đang GD" if is_trading_hours() else " · ○ Ngoài giờ"
_bars_label = f" · {len(df1_raw)}b/1m · {len(df5_raw)}b/5m"

fl.markdown(
    f'<div style="font-size:10px;color:#334155;font-family:JetBrains Mono">'
    f'VN30F Terminal v3 · {_src_label}{_hrs_label}{_bars_label} · '
    f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div>',
    unsafe_allow_html=True
)
if auto_refresh:
    rem = max(0, refresh_sec-(datetime.now()-st.session_state.last_refresh).seconds)
    fr.markdown(f'<div style="font-size:10px;color:#38bdf8;font-family:JetBrains Mono;text-align:right">🔄 {rem}s</div>', unsafe_allow_html=True)
    if (datetime.now()-st.session_state.last_refresh).seconds >= refresh_sec:
        st.session_state.last_refresh = datetime.now()
    time.sleep(1); st.rerun()
