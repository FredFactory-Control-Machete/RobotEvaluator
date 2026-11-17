import pandas as pd
import streamlit as st
from Main import main

st.set_page_config(page_title="Hello Streamlit", page_icon="📊", layout="wide")

st.title("Robot selection with MCDM")
st.header("This robot selection uses VIKOR, MORA, CODA and TOPSIS")

#upload a file with the robots you are planing to choose(integrate a database if possible later on)
with st.form("upload_form"):
    uploaded_file = st.file_uploader("Upload a file", type=["csv"], accept_multiple_files=False)
    submitted = st.form_submit_button("Load file")

if submitted:
    if uploaded_file is None:
        st.error("Choose a CSV file first.")
    elif isinstance(uploaded_file, list):
        st.error("Please upload only one file.")
    else:
        st.session_state["matrix"] = pd.read_csv(uploaded_file)
        st.dataframe(st.session_state["matrix"])

if "matrix" in st.session_state:
    st.dataframe(st.session_state["matrix"])
# ask for the min ideal and max of each column, for price and asbsolute max

if st.button("Next"):
    if "matrix" not in st.session_state:
        st.error("Upload and submit a CSV first.")
        st.stop()
    st.session_state["show_inputs"] = True #saves a flag

if st.session_state.get("show_inputs", False):#cheacks the flag
    matrix = st.session_state["matrix"].drop(columns="Robot")
    df = pd.DataFrame(columns=["Criterio", "Min", "Ideal", "Max","Weight", "Filter"])
    for i in matrix.columns:
        aplicar_filtro = st.checkbox(
            f"Apply limits for {i}", value=True, key=f"filter_{i}")
        if i != "Costo_USD":

            st.write(f"For {i}, what are the min, ideal and max values?")
            col1, col2, col3, col4 = st.columns(4) #makes three colums same row in the website
            df.loc[len(df)] = [i, col1.number_input("Min", key=f"min_{i}"),
                              col2.number_input("Ideal", key=f"ideal_{i}"),
                              col3.number_input("Max", key=f"max_{i}"),
                              col4.number_input(
                                   "How important is this criterion from 0-1",
                                   min_value=0.0,
                                   max_value=1.0,
                                   step=0.01,
                                   key=f"weight_{i}"),
                                   aplicar_filtro]
            fila = df.iloc[-1] # select the row you ust added(last row basically)
            if not (fila["Min"] <= fila["Ideal"] <= fila["Max"]):#if condition not met, warning
                st.warning(f"For {i}, values must satisfy: Min ≤ Ideal ≤ Max.")
        else:
            st.write(f"What is the most you are willing to pay")
            df.loc[len(df)] = [i, None, None, st.number_input("Max", key=f"max_{i}"),None, aplicar_filtro]
    st.session_state["Values"] = df

# press button to calcualte, recommendations based on each algorithm.
if st.button("Calculate"):
    try:
        st.dataframe(main(st.session_state["matrix"], st.session_state["Values"]))
    except ValueError as error:
        st.warning(str(error))