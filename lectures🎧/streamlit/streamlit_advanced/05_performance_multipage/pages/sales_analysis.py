import streamlit as st
import pandas as pd
from utils.database import get_connection

st.header("💰 매출 분석")
st.caption("@st.fragment로 부분 재실행 - 필터 변경 시 해당 영역만 재실행")

conn = get_connection()
st.success(f"✅ DB 연결 (id: {id(conn)})")

# -----------------------------------------------------------------------------
# 매출 데이터 로드
@st.cache_data
def load_invoices():
    return pd.read_sql("""
        SELECT i.InvoiceId, i.InvoiceDate, i.Total,
               c.FirstName || ' ' || c.LastName as Customer,
               c.Country
        FROM invoices i
        JOIN customers c ON i.CustomerId = c.CustomerId
    """, conn)

invoices = load_invoices()

st.divider()

# -----------------------------------------------------------------------------
# Fragment 1: 국가별 필터
@st.fragment
def country_filter():
    st.subheader("🌍 국가별 매출")

    countries = invoices['Country'].unique().tolist()
    selected = st.multiselect("국가 선택", countries, default=countries[:5], key="countries")

    if selected:
        filtered = invoices[invoices['Country'].isin(selected)]
        by_country = filtered.groupby('Country')['Total'].sum().sort_values(ascending=False)
        st.bar_chart(by_country)
        st.caption(f"선택된 국가 총 매출: ${filtered['Total'].sum():,.2f}")

country_filter()

st.divider()

# -----------------------------------------------------------------------------
# Fragment 2: 기간별 분석
@st.fragment
def time_analysis():
    st.subheader("📅 기간별 매출")

    invoices['Date'] = pd.to_datetime(invoices['InvoiceDate'])
    invoices['YearMonth'] = invoices['Date'].dt.to_period('M').astype(str)

    period = st.radio("기간", ["월별", "연도별"], horizontal=True, key="period")

    if period == "월별":
        by_time = invoices.groupby('YearMonth')['Total'].sum()
    else:
        invoices['Year'] = invoices['Date'].dt.year
        by_time = invoices.groupby('Year')['Total'].sum()

    st.line_chart(by_time)

time_analysis()

st.divider()

# -----------------------------------------------------------------------------
# Fragment 3: 고객별 분석
@st.fragment
def customer_analysis():
    st.subheader("👤 Top 고객")

    top_n = st.slider("표시 수", 5, 20, 10, key="top_n")

    top_customers = invoices.groupby('Customer')['Total'].sum().nlargest(top_n)
    st.bar_chart(top_customers)

customer_analysis()
