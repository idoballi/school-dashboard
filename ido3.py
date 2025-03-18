import streamlit as st
import pandas as pd
import plotly.express as px

# קישור לקובץ ה-CSV ב-GitHub (עדכן את שם המשתמש והמאגר שלך)
GITHUB_CSV_URL = "https://raw.githubusercontent.com/idoballi/school-dashboard/main/Datatest.csv"

# קריאת הנתונים ישירות מ-GitHub
@st.cache_data
def load_data():
    return pd.read_csv(GITHUB_CSV_URL)

df = load_data()

# ניקוי הנתונים
columns_needed = ["שם מוסד", "ישוב לימודים", "מחוז גאוגרפי לחינוך", "מספר תלמידים"]
df = df[columns_needed].dropna()
df["מספר תלמידים"] = pd.to_numeric(df["מספר תלמידים"], errors='coerce')

def main():
    st.title("? דשבורד בתי ספר בישראל")

    # מספר בתי ספר לפי עיר
    st.subheader("? מספר בתי ספר לפי עיר")
    city_counts = df["ישוב לימודים"].value_counts().reset_index()
    city_counts.columns = ["עיר", "מספר בתי ספר"]
    fig1 = px.bar(city_counts.head(15), x="עיר", y="מספר בתי ספר", text="מספר בתי ספר",
                  title="מספר בתי ספר בערים המובילים")
    st.plotly_chart(fig1)

    # גודל ממוצע של בתי ספר לפי מחוז גאוגרפי
    st.subheader("? גודל ממוצע של בתי ספר לפי מחוז")
    region_avg = df.groupby("מחוז גאוגרפי לחינוך")["מספר תלמידים"].mean().reset_index()
    region_avg.columns = ["מחוז", "מספר תלמידים ממוצע"]
    fig2 = px.bar(region_avg, x="מחוז", y="מספר תלמידים ממוצע", text="מספר תלמידים ממוצע",
                  title="גודל ממוצע של בתי ספר לפי מחוז")
    st.plotly_chart(fig2)

    # אפשרות לבחור עיר ולראות פרטים
    st.subheader("? חיפוש בתי ספר בעיר ספציפית")
    selected_city = st.selectbox("בחר עיר", df["ישוב לימודים"].unique())
    filtered_df = df[df["ישוב לימודים"] == selected_city]
    st.write(f"**נמצאו {len(filtered_df)} בתי ספר בעיר {selected_city}**")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()