import streamlit as st
import pandas as pd

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1mURcpXkUwzhSQsP6SB959gwp5oh-Xw8LkGq1wIhAzYM/edit?usp=sharing"
if "edit?usp=sharing" in GOOGLE_SHEET_URL:
    csv_url = GOOGLE_SHEET_URL.replace("edit?usp=sharing", "gviz/tq?tqx=out:csv")
else:
    csv_url = GOOGLE_SHEET_URL.split("/edit")[0] + "/gviz/tq?tqx=out:csv"
st.set_page_config(page_title="Расчет наценки", layout="centered")
st.title("Медики-шмедики")
st.write("Выбери медицину , её колличество и наценку на неё")

try:
    @st.cache_data(ttl=5)
    def load_data(url):
        return pd.read_csv(url)

    df_base = load_data(csv_url)
    
    if "Товар" in df_base.columns and "Базовая цена (руб)" in df_base.columns:
        df_base = df_base.dropna(subset=["Медицина", "Базовая цена (руб)"])
        df_base["Базовая цена (руб)"] = df_base["Базовая цена (руб)"].astype(int)
        
        percent = st.slider("Выбери на сколько ты ограбишь сталкеров в % (Наценка)", min_value=0, max_value=30, value=0, step=1)

        df_base["Цена с наценкой (руб)"] = (df_base["Базовая цена (руб)"] * (1 + percent / 100)).round(0).astype(int)
        
        df_base.insert(0, "Выбрать", False)
        df_base["Количество (шт)"] = 1

        st.subheader("Медицина")
        st.caption("Ебани галочку слева от медицины и справа выставь колличество:")

        edited_df = st.data_editor(
            df_base,
            use_container_width=True,
            hide_index=True,
            disabled=["Товар", "Базовая цена (руб)", "Цена с наценкой (руб)"],
            column_config={
                "Выбрать": st.column_config.CheckboxColumn("Выбрать", default=False),
                "Количество (шт)": st.column_config.NumberColumn("Количество", min_value=1, max_value=1000, step=1, default=1),
                "Базовая цена (руб)": st.column_config.NumberColumn(format="%d"),
                "Цена с наценкой (руб)": st.column_config.NumberColumn(format="%d")
            }
        )

        selected_rows = edited_df[edited_df["Выбрать"] == True]

        st.markdown("---") 

        if not selected_rows.empty:
            selected_rows["Всего (руб)"] = selected_rows["Цена с наценкой (руб)"] * selected_rows["Количество (шт)"]
            total_sum = selected_rows["Всего (руб)"].sum()

            st.success(f"### Итого по денякам: {total_sum:,} руб.".replace(",", " "))
            
            # Показываем мини-чек (что именно выбрано)
            st.write("*Выбранные позиции:*")
            st.dataframe(
                selected_rows[["Товар", "Количество (шт)", "Цена с наценкой (руб)", "Всего (руб)"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Цена с наценкой (руб)": st.column_config.NumberColumn(format="%d"),
                    "Всего (руб)": st.column_config.NumberColumn(format="%d")
                }
            )
        else:
            st.info("Стоимость появляется только после выбора хотя бы одной позиции")

    else:
        st.error("Ошибка: СЛАДКОГО СЪЕЛИ")

except Exception as e:
    st.error("Не удалалось найти мозг")
