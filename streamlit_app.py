# 📊 Streamlit 소비 트렌드 대시보드
import streamlit as st
import pandas as pd
import numpy as np

# ===== 기본 설정 =====
st.set_page_config(page_title="소비 트렌드 대시보드", layout="wide")

# ===== 더미 데이터 생성 =====
np.random.seed(42)
data = {
    '월': [f'{m}월' for m in range(1, 13)],
    '식음료': np.random.randint(380000, 520000, 12),
    '패션·뷰티': np.random.randint(250000, 400000, 12),
    '여행·레저': np.random.randint(150000, 500000, 12) + np.sin(np.linspace(0, 2*np.pi, 12))*80000,  # 여름 피크
    '교육·문화': np.random.randint(200000, 300000, 12),
    '생활·가전': np.random.randint(180000, 280000, 12)
}

df = pd.DataFrame(data)
df_melt = df.melt(id_vars='월', var_name='업종', value_name='평균소비액')

# ===== CSS 스타일 =====
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    body {
        font-family: "Noto Sans KR", sans-serif;
    }

    /* 사이드바 전체 */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding: 1.2rem 1rem 2rem 1rem;
        border-right: 1px solid #e0e0e0;
    }

    /* 버튼 스타일 */
    div.stButton > button {
        background-color: #4a90e2;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.35rem 0.7rem;
        font-size: 0.9rem;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        background-color: #357ABD;
        transform: scale(1.03);
    }

    /* selectbox 스타일 */
    div[data-baseweb="select"] > div {
        border-radius: 6px;
        border: 1px solid #ccc;
    }

    /* 제목 스타일 */
    .main > div > div > div > div > h1 {
        color: #333333;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# ===== 사이드바 UI =====
st.sidebar.title("🎯 필터 설정")
selected_category = st.sidebar.selectbox("업종 선택", df_melt['업종'].unique())
show_all = st.sidebar.button("전체 업종 보기")

st.sidebar.markdown("---")
st.sidebar.caption("※ 업종을 선택하거나 전체 보기 버튼을 눌러 데이터를 확인하세요.")

# ===== 메인 영역 =====
st.title("📊 2024년 업종별 소비 트렌드 대시보드")

if show_all:
    st.subheader("📈 전체 업종 월별 소비 추이")
    st.line_chart(df.set_index('월'))
else:
    st.subheader(f"📈 {selected_category} 월별 소비 추이")
    filtered = df_melt[df_melt['업종'] == selected_category]
    st.line_chart(filtered.pivot(index='월', columns='업종', values='평균소비액'))

# ===== 요약 통계 =====
st.subheader("📊 업종별 소비 요약 통계")
st.dataframe(df.describe().T.style.format("{:,.0f}").background_gradient(cmap="Blues"))

# ===== 하단 안내 =====
st.markdown("---")
st.caption("💡 데이터는 예시용이며, 실제 소비 트렌드를 기반으로 분석 구조를 확장할 수 있습니다.")
