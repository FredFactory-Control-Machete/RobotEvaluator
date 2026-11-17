import pandas as pd
import numpy as np
import streamlit as st
import VIKOR
from Main import main

st.set_page_config(page_title="Hello Streamlit", page_icon="📊", layout="wide")

st.title("Robot selection with MCDM")
st.header("This robot selection uses VIKOR, MORA, CODA and TOPSIS")

#upload a file with the robots you are planing to choose(integrate a database if possible later on)

# ask for the min ideal and max of each column, for price and asbsolute max

# press button to calcualte, recommendations based on each algorithm.
if st.button("Calculate"):
    df = pd.DataFrame(main())