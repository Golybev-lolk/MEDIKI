import streamlit as st
import pandas as pd
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1mURcpXkUwzhSQsP6SB959gwp5oh-Xw8LkGq1wIhAzYM/edit?usp=sharing"
if "edit?usp=sharing" in GOOGLE_SHEET_URL:
    csv_url = GOOGLE_SHEET_URL.replace("edit?usp=sharing", "gviz/tq?tqx=out:csv")
else:
    csv_url = GOOGLE_SHEET_URL.split("/edit")[0] + "/gviz/tq?tqx=out:csv"
st.set_page_config(page_title="Расчет наценки", layout="centered")
st.title("Медики TF2")
st.write("Двигай штуку на нужный %")
try:
    @st.cache_data(ttl=5)
    def load_data(url):
        return pd.read_csv(url)
    df = load_data(csv_url)
    if "Товар" in df.columns and "Базовая цена (руб)" in df.columns:
        df = df.dropna(subset=["Товар", "Базовая цена (руб)"])
        df["Базовая цена (руб)"] = df["Базовая цена (руб)"].astype(int)
        percent = st.slider("Выберите наценку (%)", min_value=0, max_value=30, value=0, step=1)
        df["Цена с наценкой (руб)"] = (df["Базовая цена (руб)"] * (1 + percent / 100)).round(0).astype(int)
        st.subheader(f"Результаты с наценкой:")
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Базовая цена (руб)": st.column_config.NumberColumn(format="%d"),
                "Цена с наценкой (руб)": st.column_config.NumberColumn(format="%d")
            }
        )
    else:
        st.error("Ошибка: Сладкого съели")

except Exception as e:
    st.error("Не удалось подключиться АДЕКВАТНОСТИ")
