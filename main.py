import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


# ---------------------------------------------------------
# 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="주식 종목 비교",
    page_icon="📈",
    layout="wide"
)


# ---------------------------------------------------------
# 따뜻한 느낌의 화면 디자인
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #FFF8E8;
        }

        h1, h2, h3 {
            color: #5C421F;
        }

        .description {
            color: #806A4A;
            font-size: 17px;
            line-height: 1.7;
            margin-bottom: 20px;
        }

        .metric-card {
            background-color: #FFFDF5;
            border: 2px solid #F0D58A;
            border-radius: 18px;
            padding: 18px 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(120, 90, 30, 0.08);
        }

        .metric-title {
            color: #8B744F;
            font-size: 15px;
            margin-bottom: 7px;
        }

        .metric-value {
            color: #5C421F;
            font-size: 27px;
            font-weight: bold;
        }

        .hint {
            color: #8B744F;
            font-size: 14px;
            margin-top: 5px;
        }

        .section-title {
            color: #5C421F;
            font-size: 23px;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# 제목과 설명
# ---------------------------------------------------------
st.title("📈 주식 종목 비교")

st.markdown(
    """
    <div class="description">
        최대 2개의 주식 종목을 나란히 비교해 보세요.
        <br>
        원하는 기간을 선택하면 주가 흐름과 주요 가격 정보를 확인할 수 있어요.
        <br>
        예: <b>005930.KS</b> (삼성전자), <b>AAPL</b> (애플)
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# 종목 입력창 2개
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">🔎 비교할 종목</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    ticker1 = st.text_input(
        "첫 번째 종목",
        value="005930.KS",
        placeholder="예: 005930.KS",
        key="ticker1"
    ).strip().upper()

with col2:
    ticker2 = st.text_input(
        "두 번째 종목",
        value="AAPL",
        placeholder="예: AAPL",
        key="ticker2"
    ).strip().upper()

st.markdown(
    '<div class="hint">한국 주식은 보통 .KS, 미국 주식은 AAPL처럼 입력하세요.</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# 기간 선택
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📅 조회 기간</div>',
    unsafe_allow_html=True
)

period_options = {
    "1개월": "1mo",
    "6개월": "6mo",
    "1년": "1y",
    "5년": "5y"
}

selected_period_name = st.radio(
    "기간을 선택하세요",
    options=list(period_options.keys()),
    horizontal=True,
    label_visibility="collapsed"
)

selected_period = period_options[selected_period_name]


# ---------------------------------------------------------
# 입력된 종목을 가져오는 함수
# ---------------------------------------------------------
def get_stock_data(ticker, period):
    """
    yfinance를 이용해서 선택한 기간의 주가 데이터를 가져옵니다.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)

        if data.empty:
            return None

        return data

    except Exception:
        return None


# ---------------------------------------------------------
# 종목 이름을 가져오는 함수
# ---------------------------------------------------------
def get_stock_name(ticker):
    """
    가능하면 yfinance에서 회사 이름을 가져옵니다.
    이름을 가져오지 못하면 종목 코드를 그대로 사용합니다.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        name = info.get("shortName")

        if name:
            return name

    except Exception:
        pass

    return ticker


# ---------------------------------------------------------
# 가격을 보기 좋게 표시하는 함수
# ---------------------------------------------------------
def format_price(price):
    """
    가격을 천 단위 쉼표와 함께 표시합니다.
    """
    return f"{price:,.2f}"


# ---------------------------------------------------------
# 종목 데이터 불러오기
# ---------------------------------------------------------
data1 = None
data2 = None

if ticker1:
    with st.spinner(f"{ticker1} 데이터를 불러오는 중입니다..."):
        data1 = get_stock_data(ticker1, selected_period)

if ticker2:
    with st.spinner(f"{ticker2} 데이터를 불러오는 중입니다..."):
        data2 = get_stock_data(ticker2, selected_period)


# ---------------------------------------------------------
# 데이터를 가져오지 못한 종목이 있으면 안내
# ---------------------------------------------------------
if ticker1 and data1 is None:
    st.warning(
        f"⚠️ '{ticker1}'의 데이터를 찾을 수 없습니다. "
        "종목 코드를 확인해 주세요."
    )

if ticker2 and data2 is None:
    st.warning(
        f"⚠️ '{ticker2}'의 데이터를 찾을 수 없습니다. "
        "종목 코드를 확인해 주세요."
    )


# ---------------------------------------------------------
# 그래프 표시
# ---------------------------------------------------------
if data1 is not None or data2 is not None:

    st.markdown(
        f'<div class="section-title">📊 최근 {selected_period_name} 주가 비교</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure()

    # 첫 번째 종목 그래프
    if data1 is not None:
        fig.add_trace(
            go.Scatter(
                x=data1.index,
                y=data1["Close"],
                mode="lines",
                name=ticker1,
                line=dict(width=3)
            )
        )

    # 두 번째 종목 그래프
    if data2 is not None:
        fig.add_trace(
            go.Scatter(
                x=data2.index,
                y=data2["Close"],
                mode="lines",
                name=ticker2,
                line=dict(width=3)
            )
        )

    fig.update_layout(
        title=f"주가 흐름 · {selected_period_name}",
        xaxis_title="날짜",
        yaxis_title="주가",
        hovermode="x unified",
        height=520,
        plot_bgcolor="#FFFDF5",
        paper_bgcolor="#FFF8E8",
        font=dict(
            color="#5C421F",
            size=14
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # 종목별 현재가와 등락률
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">💰 현재 가격</div>',
        unsafe_allow_html=True
    )

    current_columns = st.columns(2)

    datasets = [
        (ticker1, data1, current_columns[0]),
        (ticker2, data2, current_columns[1])
    ]

    for ticker, data, column in datasets:

        if data is None:
            continue

        current_price = float(data["Close"].iloc[-1])
        start_price = float(data["Close"].iloc[0])

        change_percent = (
            (current_price - start_price) / start_price
        ) * 100

        if change_percent >= 0:
            change_text = f"▲ {change_percent:.2f}%"
        else:
            change_text = f"▼ {abs(change_percent):.2f}%"

        company_name = get_stock_name(ticker)

        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        {company_name} ({ticker})
                    </div>
                    <div class="metric-value">
                        {format_price(current_price)}
                    </div>
                    <div style="margin-top:8px; color:#806A4A;">
                        {selected_period_name} 등락률&nbsp;&nbsp;{change_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # 최고가 · 최저가 · 평균가
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">📌 주요 가격 정보</div>',
        unsafe_allow_html=True
    )

    # 각 종목을 하나의 카드 묶음으로 보여줍니다.
    for ticker, data in [
        (ticker1, data1),
        (ticker2, data2)
    ]:

        if data is None:
            continue

        highest_price = float(data["High"].max())
        lowest_price = float(data["Low"].min())
        average_price = float(data["Close"].mean())

        company_name = get_stock_name(ticker)

        st.markdown(
            f"""
            <div style="
                color:#6B512C;
                font-size:18px;
                font-weight:bold;
                margin:18px 0 10px 3px;
            ">
                {company_name} ({ticker})
            </div>
            """,
            unsafe_allow_html=True
        )

        stat1, stat2, stat3 = st.columns(3)

        with stat1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">🔺 최고가</div>
                    <div class="metric-value">
                        {format_price(highest_price)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with stat2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">🔻 최저가</div>
                    <div class="metric-value">
                        {format_price(lowest_price)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with stat3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">📊 평균가</div>
                    <div class="metric-value">
                        {format_price(average_price)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ---------------------------------------------------------
# 데이터가 하나도 없을 때
# ---------------------------------------------------------
else:
    st.info(
        "💡 종목 코드를 입력하면 주가 비교 그래프가 나타납니다."
    )


# ---------------------------------------------------------
# 하단 안내
# ---------------------------------------------------------
st.markdown(
    """
    <div style="
        text-align:center;
        color:#A28A61;
        font-size:14px;
        margin-top:35px;
        padding-bottom:20px;
    ">
        ※ 주가 데이터는 yfinance를 통해 제공됩니다.<br>
        실제 투자 결정 전에는 추가적인 정보를 확인하세요.
    </div>
    """,
    unsafe_allow_html=True
)
