import streamlit as st
import pandas as pd
import plotly.express as px

# ����� ���� CSV ���� (Data1.csv) �� ����� ����� �������
file_path = "C:/Users/ido/Documents/Data1.csv"

# ������ ����� �� ����� �� ���� ������� �����
encodings = ["windows-1255", "ISO-8859-8", "latin1", "utf-8"]
df = None
for enc in encodings:
    try:
        print(f"? ���� ����� �� ����� �� �����: {enc}")
        df = pd.read_csv(file_path, encoding=enc, errors='replace')
        print(f"? ����� ������ ����� �� ������: {enc}")
        break
    except Exception as e:
        print(f"? ����� ������ ����� �� ������ {enc}: {e}")

if df is None:
    st.error("?? �� ���� ����� �� �����. ���� �� ������ �� ��� ����� ���� ���� �-CSV ����.")
    st.stop()

# ���� ���� ������� ���� ����� (������ ����)
df["���� �������"] = pd.to_numeric(df["���� �������"], errors='coerce')


def main():
    st.title("? ������ ��� ��� ������")

    # ���� �� ��� ���� ��� �����
    st.subheader("? ����� �� ��� ����")
    st.dataframe(df)

    # ����� ��� �� ��� ���, ��� ���� ����� �������
    school_name = st.text_input("? ����� ��� �� ����")
    school_symbol = st.text_input("? ����� ��� ��� ����")
    min_students = st.slider("? ���� ������� �������", 0, int(df["���� �������"].max()), 0)

    # ����� ������� ����� ������
    filtered_df = df.copy()
    if school_name:
        filtered_df = filtered_df[filtered_df["�� ����"].str.contains(school_name, na=False, case=False)]
    if school_symbol:
        filtered_df = filtered_df[filtered_df["��� ����"].astype(str).str.contains(school_symbol, na=False, case=False)]
    filtered_df = filtered_df[filtered_df["���� �������"] >= min_students]

    # ���� ������� ��������
    st.write(f"**����� {len(filtered_df)} ��� ��� ����� ������**")
    st.dataframe(filtered_df)

    # ��� ���� ��� ��� ��� ���
    st.subheader("? ���� ��� ��� ��� ���")
    city_counts = filtered_df["���� �������"].value_counts().reset_index()
    city_counts.columns = ["���", "���� ��� ���"]
    fig1 = px.bar(city_counts.head(15), x="���", y="���� ��� ���", text="���� ��� ���",
                  title="���� ��� ��� ����� ��������")
    st.plotly_chart(fig1)

    # ���� ����� �� ��� ��� ��� ���� �������
    st.subheader("? ���� ����� �� ��� ��� ��� ����")
    region_avg = filtered_df.groupby("���� ������� ������")["���� �������"].mean().reset_index()
    region_avg.columns = ["����", "���� ������� �����"]
    fig2 = px.bar(region_avg, x="����", y="���� ������� �����", text="���� ������� �����",
                  title="���� ����� �� ��� ��� ��� ����")
    st.plotly_chart(fig2)


if __name__ == "__main__":
    main()
