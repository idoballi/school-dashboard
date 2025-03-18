import streamlit as st
import pandas as pd
import plotly.express as px

# קריאת קובץ CSV יחיד (Data1.csv) עם קידוד Windows-1255 בלבד
file_path = r"C:\Users\ido\PycharmProjects\ido\Data1.csv"

try:
    print(f"? טוען את הקובץ: {file_path} עם קידוד: windows-1255")
    df = pd.read_csv(file_path, encoding="windows-1255", errors='replace')  # קריאה עם ניהול שגיאות
except Exception as e:
    print(f"? שגיאה בקריאת הקובץ {file_path}: {e}")
    st.error(f"שגיאה בטעינת הנתונים: {e}")
    st.stop()

# המרת מספר תלמידים לערך מספרי (לסינון נכון)
df["מספר תלמידים"] = pd.to_numeric(df["מספר תלמידים"], errors='coerce')


def main():
    st.title("? דשבורד בתי ספר בישראל")

    # חיפוש לפי שם בית ספר, סמל מוסד וכמות תלמידים
    school_name = st.text_input("? חיפוש לפי שם מוסד")
    school_symbol = st.text_input("? חיפוש לפי סמל מוסד")
    min_students = st.slider("? מספר תלמידים מינימלי", 0, int(df["מספר תלמידים"].max()), 0)

    # סינון הנתונים בהתאם לחיפוש
    filtered_df = df.copy()
    if school_name:
        filtered_df = filtered_df[filtered_df["שם מוסד"].str.contains(school_name, na=False, case=False)]
    if school_symbol:
        filtered_df = filtered_df[filtered_df["סמל מוסד"].astype(str).str.contains(school_symbol, na=False, case=False)]
    filtered_df = filtered_df[filtered_df["מספר תלמידים"] >= min_students]

    # הצגת הנתונים המסוננים
    st.write(f"**נמצאו {len(filtered_df)} בתי ספר בהתאם לחיפוש**")
    st.dataframe(filtered_df)

    # גרף מספר בתי ספר לפי עיר
    st.subheader("? מספר בתי ספר לפי עיר")
    city_counts = filtered_df["ישוב לימודים"].value_counts().reset_index()
    city_counts.columns = ["עיר", "מספר בתי ספר"]
    fig1 = px.bar(city_counts.head(15), x="עיר", y="מספר בתי ספר", text="מספר בתי ספר",
                  title="מספר בתי ספר בערים המובילים")
    st.plotly_chart(fig1)

    # גודל ממוצע של בתי ספר לפי מחוז גאוגרפי
    st.subheader("? גודל ממוצע של בתי ספר לפי מחוז")
    region_avg = filtered_df.groupby("מחוז גאוגרפי לחינוך")["מספר תלמידים"].mean().reset_index()
    region_avg.columns = ["מחוז", "מספר תלמידים ממוצע"]
    fig2 = px.bar(region_avg, x="מחוז", y="מספר תלמידים ממוצע", text="מספר תלמידים ממוצע",
                  title="גודל ממוצע של בתי ספר לפי מחוז")
    st.plotly_chart(fig2)


if __name__ == "__main__":
    main()