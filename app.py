import matplotlib.pyplot as plt
import streamlit as st
from prophetPreprocessor import ProphetPreprocessor

api_key = 'ckey_70a8a6bf18464adc99f3057a1ac'

def main():
    st.sidebar.title("Parameters")
    collection = st.sidebar.selectbox("Choose Collection", ("BAYC", "MAYC"))

    st.title("BridXe Market Intelligence Platform")
    prophetpre = ProphetPreprocessor(api_key)

    mayc = prophetpre.load_data("0x60E4d786628Fea6478F785A6d7e704777c86a7c6", "floor_7d")
    st.dataframe(mayc)


if __name__ == '__main__':
    main()