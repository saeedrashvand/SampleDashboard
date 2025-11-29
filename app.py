import streamlit as st
import pandas as pd
import plotly.express as px

# تنظیمات اولیه صفحه (عنوان و آیکون)
st.set_page_config(page_title="داشبورد فروش", page_icon="📊", layout="wide")

# استایل برای راست‌چین کردن متن‌ها (چون فارسی است)
st.markdown("""
<style>
    .main {
        direction: rtl;
        font-family: 'Tahoma', sans-serif;
    }
    h1, h2, h3 {
        text-align: right;
    }
    .stSelectbox, .stMetric {
        direction: rtl; 
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# --- داده‌های نمونه ---
data = {
    "محصول": ["گوشی موبایل", "لپ‌تاپ", "هدفون", "ساعت هوشمند", "تبلت", 
               "گوشی موبایل", "لپ‌تاپ", "هدفون", "ساعت هوشمند", "تبلت"],
    "تعداد فروش": [120, 85, 200, 150, 90, 130, 95, 210, 160, 100],
    "شهر": ["تهران", "تهران", "تهران", "تهران", "تهران", 
            "اصفهان", "اصفهان", "اصفهان", "اصفهان", "اصفهان"],
    "درامد (میلیون)": [2400, 4250, 600, 750, 1800, 2600, 4750, 630, 800, 2000]
}
df = pd.DataFrame(data)

# --- هدر و عنوان ---
st.title(" نمونه داشبورد(www.nhsk.ir)📊 داشبورد تحلیل فروش آنلاین")
st.markdown(" www.nhsk.ir این داشبورد جهت ارائه نمونه کار به کارفرما طراحی شده است.")
st.markdown("---")

# --- سایدبار (نوار کناری) برای فیلتر ---
st.sidebar.header("فیلترها")
selected_city = st.sidebar.selectbox(
    "انتخاب شهر:",
    options=df["شهر"].unique()
)

# فیلتر کردن داده‌ها
filtered_df = df[df["شهر"] == selected_city]

# --- نمایش متریک‌های کلیدی (KPI) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("تعداد کل فروش", f"{filtered_df['تعداد فروش'].sum()} عدد")
with col2:
    st.metric("مجموع درآمد", f"{filtered_df['درامد (میلیون)'].sum():,} میلیون")
with col3:
    st.metric("بهترین محصول", filtered_df.loc[filtered_df['تعداد فروش'].idxmax()]['محصول'])

st.markdown("---")

# --- نمودارها ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader(f"تعداد فروش در {selected_city}")
    fig_bar = px.bar(filtered_df, x='محصول', y='تعداد فروش', 
                     text='تعداد فروش', color='محصول')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader(f"سهم درآمد محصولات")
    fig_pie = px.pie(filtered_df, values='درامد (میلیون)', names='محصول', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- نمایش جدول داده‌ها ---
with st.expander("مشاهده داده‌های خام"):
    st.dataframe(filtered_df, use_container_width=True)
