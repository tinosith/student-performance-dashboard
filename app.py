import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df = df.dropna().copy()
    df["attendance_rate"] = df["attendance_rate"].clip(0, 1)
    df["final_grade"] = df["final_grade"].clip(0, 100)
    df["study_hours"] = df["study_hours"].clip(lower=0)
    return df

df = load_data()
st.title("🎓 Student Performance Dashboard")

with st.sidebar:
    st.header("Filters")
    attendance_min, attendance_max = st.slider("Attendance range", 0.0, 1.0, (0.6, 1.0), 0.01)
    study_min, study_max = st.slider("Study hours range", 0.0, float(df["study_hours"].max()), (0.0, float(df["study_hours"].max())), 0.5)
    parts = sorted(df["participation"].unique().tolist())
    participation_sel = st.multiselect("Participation (0-5)", parts, default=parts)

mask = (
    (df["attendance_rate"].between(attendance_min, attendance_max)) &
    (df["study_hours"].between(study_min, study_max)) &
    (df["participation"].isin(participation_sel))
)
dff = df.loc[mask]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Students", len(dff))
col2.metric("Avg Grade", f"{dff['final_grade'].mean():.1f}")
col3.metric("Avg Attendance", f"{dff['attendance_rate'].mean():.2f}")
col4.metric("Avg Study Hours", f"{dff['study_hours'].mean():.1f}")

st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Final Grade Distribution")
    fig1 = plt.figure()
    dff["final_grade"].plot.hist(bins=15)
    plt.xlabel("Final Grade")
    plt.ylabel("Count")
    st.pyplot(fig1)

with c2:
    st.subheader("Attendance vs Final Grade")
    fig2 = plt.figure()
    plt.scatter(dff["attendance_rate"], dff["final_grade"], alpha=0.7)
    x = dff["attendance_rate"].values
    if len(x) > 1:
        coef = np.polyfit(x, dff["final_grade"].values, 1)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = coef[0] * x_line + coef[1]
        plt.plot(x_line, y_line)
    plt.xlabel("Attendance Rate")
    plt.ylabel("Final Grade")
    st.pyplot(fig2)

st.subheader("Data Preview")
st.dataframe(dff.head(50))