import streamlit as st
import pandas as pd
import plotly.express as px

# ����� ����� �-CSV �-GitHub (���� �� �� ������ ������ ���)
GITHUB_CSV_URL = "https://raw.githubusercontent.com/idoballi/school-dashboard/main/Datatest.csv"

# ����� ������� ������ �-GitHub
@st.cache_data
def load_data():
    return pd.read_csv(GITHUB_CSV_URL)

df = load_data()

# ����� �������
columns_needed = ["�� ����", "���� �������", "���� ������� ������", "���� �������"]
df = df[columns_needed].dropna()
df["���� �������"] = pd.to_numeric(df["���� �������"], errors='coerce')

def main():
    st.title("? ������ ��� ��� ������")

    # ���� ��� ��� ��� ���
    st.subheader("? ���� ��� ��� ��� ���")
    city_counts = df["���� �������"].value_counts().reset_index()
    city_counts.columns = ["���", "���� ��� ���"]
    fig1 = px.bar(city_counts.head(15), x="���", y="���� ��� ���", text="���� ��� ���",
                  title="���� ��� ��� ����� ��������")
    st.plotly_chart(fig1)

    # ���� ����� �� ��� ��� ��� ���� �������
    st.subheader("? ���� ����� �� ��� ��� ��� ����")
    region_avg = df.groupby("���� ������� ������")["���� �������"].mean().reset_index()
    region_avg.columns = ["����", "���� ������� �����"]
    fig2 = px.bar(region_avg, x="����", y="���� ������� �����", text="���� ������� �����",
                  title="���� ����� �� ��� ��� ��� ����")
    st.plotly_chart(fig2)

    # ������ ����� ��� ������ �����
    st.subheader("? ����� ��� ��� ���� �������")
    selected_city = st.selectbox("��� ���", df["���� �������"].unique())
    filtered_df = df[df["���� �������"] == selected_city]
    st.write(f"**����� {len(filtered_df)} ��� ��� ���� {selected_city}**")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()