import streamlit as st
import pandas as pd
import plotly.express as px

# קריאת קובץ CSV יחיד (Data1.csv) עם זיהוי קידוד אוטומטי
file_path = "C:/Users/ido/Documents/Data1.csv"

# ניסיון לקרוא את הקובץ עם מספר קידודים שונים
encodings = ["windows-1255", "ISO-8859-8", "latin1", "utf-8"]
df = None
for enc in encodings:
    try:
        print(f"? מנסה לטעון את הקובץ עם קידוד: {enc}")
        df = pd.read_csv(file_path, encoding=enc, errors='replace')
        print(f"? הצלחה בטעינת הקובץ עם הקידוד: {enc}")
        break
    except Exception as e:
        print(f"? שגיאה בקריאת הקובץ עם הקידוד {enc}: {e}")

if df is None:
    st.error("?? לא ניתן לטעון את הקובץ. בדוק את הקידוד או נסה לשמור אותו מחדש ב-CSV תקין.")
    st.stop()

# המרת מספר תלמידים לערך מספרי (לסינון נכון)
df["מספר תלמידים"] = pd.to_numeric(df["מספר תלמידים"], errors='coerce')


def main():
    st.title("? דשבורד בתי ספר בישראל")

    # הצגת כל בתי הספר ללא סינון
    st.subheader("? רשימת כל בתי הספר")
    st.dataframe(df)

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
