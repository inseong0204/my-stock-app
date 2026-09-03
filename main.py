import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


# ---------------------------------------------------------
# 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="주식 주가 조회",
    page_icon="📈",
    layout="wide"
)


# ---------------------------------------------------------
# 따뜻한 느낌의 화면 디자인을 위한 CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        /* 전체 배경 */
        .stApp {
            background-color: #FFF8E8;
        }

        /* 제목 */
        h1, h2, h3 {
            color: #5C421F;
        }

        /* 설명 글씨 */
        .description {
            color: #806A4A;
            font-size: 17px;
            margin-bottom: 20px;
        }

        /* 지표 카드 */
        .metric-card {
            background-color: #FFFDF5;
            border: 2px solid #F0D58A;
            border-radius: 18px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(120, 90, 30, 0.08);
        }

        .metric-title {
            color: #8B744F;
            font-size: 16px;
            margin-bottom: 8px;
        }

        .metric-value {
            color: #5C421F;
            font-size: 30px;
            font-weight: bold;
        }

        /* 안내 메시지 */
        .hint {
            color: #8B744F;
            font-size: 14px;
            margin-top: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# 제목과 간단한 설명
# ---------------------------------------------------------
st.title("📈 주식 주가 조회")

st.markdown(
    """
    <div class="description">
        주식 종목 코드를 입력하면 최근 1년간의 주가 흐름을 확인할 수 있어요.
        <br>
        예: <b>005930.KS</b> (삼성전자), <b>AAPL</b> (애플)
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# 종목 코드 입력창
# ---------------------------------------------------------
ticker = st.text_input(
    "🔎 종목 코드",
    value="005930.KS",
    placeholder="예: 005930.KS 또는 AAPL"
).strip().upper()

st.markdown(
    '<div class="hint">한국 주식은 보통 .KS, 미국 주식은 AAPL처럼 입력하세요.</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# 사용자가 종목 코드를 입력했을 때 실행
# ---------------------------------------------------------
if ticker:

    # yfinance를 이용해 최근 1년간의 주가 데이터를 가져옵니다.
    with st.spinner("주가 데이터를 불러오는 중입니다..."):
        try:
            stock = yf.Ticker(ticker)

            # 최근 1년 데이터를 다운로드합니다.
            data = stock.history(period="1y")

        except Exception as e:
            st.error("주가 데이터를 가져오는 중 문제가 발생했습니다.")
            st.stop()


    # 데이터를 가져오지 못한 경우
    if data.empty:
        st.error(
            f"'{ticker}' 종목의 데이터를 찾을 수 없습니다. "
            "종목 코드를 다시 확인해 주세요."
        )
        st.stop()


    # -----------------------------------------------------
    # 현재가와 1년 등락률 계산
    # -----------------------------------------------------

    # 가장 최근 거래일의 종가
    current_price = float(data["Close"].iloc[-1])

    # 1년 전 데이터의 첫 번째 종가
    start_price = float(data["Close"].iloc[0])

    # 1년 등락률 계산
    change_percent = ((current_price - start_price) / start_price) * 100


    # -----------------------------------------------------
    # 지표 카드 표시
    # -----------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">현재가</div>
                <div class="metric-value">
                    {current_price:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # 상승/하락에 따라 표시할 기호를 바꿉니다.
        if change_percent >= 0:
            change_text = f"▲ {change_percent:.2f}%"
        else:
            change_text = f"▼ {abs(change_percent):.2f}%"

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">최근 1년 등락률</div>
                <div class="metric-value">
                    {change_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # -----------------------------------------------------
    # Plotly 꺾은선 그래프
    # -----------------------------------------------------
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="종가",
            line=dict(width=3)
        )
    )

    # 그래프 제목과 축 이름을 설정합니다.
    fig.update_layout(
        title=f"{ticker} 최근 1년 주가",
        xaxis_title="날짜",
        yaxis_title="주가",
        hovermode="x unified",
        height=500,
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
        )
    )

    # 그래프를 화면에 표시합니다.
    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------------------------
    # 간단한 안내 문구
    # -----------------------------------------------------
    st.info(
        "💡 위 그래프는 yfinance에서 제공하는 최근 1년간의 종가 데이터를 "
        "바탕으로 표시합니다. 실제 투자 결정 전에는 추가적인 정보를 확인하세요."
    )
