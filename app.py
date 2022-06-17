import json
import matplotlib.pyplot as plt
import streamlit as st
from time import sleep
from covalentReader import CovalentReader

api_key = 'ckey_70a8a6bf18464adc99f3057a1ac'

def main():
    cr = CovalentReader(api_key)

    @st.cache(persist=True)
    def load_data():
        with open('contracts.json', 'r') as f:
            contracts = json.load(f)

        keys = [c for c in contracts.keys()]

        return contracts, keys

    contracts, keys = load_data()
    st.sidebar.title("Parameters")
    with st.sidebar.form("parameters"):
        collection = st.selectbox("Choose Collection", keys)
        metric = st.selectbox("Choose metric", ("floor_7d", "avg_volume_1d", "volume_1d", "sold_1d"))
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.title(collection)
        ts = cr.load_data(contracts[collection], metric)
        plt.plot(ts['ds'], ts['y'], color='red')
        st.pyplot(plt)


if __name__ == '__main__':
    main()
    