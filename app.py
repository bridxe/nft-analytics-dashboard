import json
import matplotlib.pyplot as plt
import streamlit as st
from time import sleep

from covalentReader import CovalentReader
from quantMetrics import QuantMetrics
from tsForecast import TsForecast

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
        series = st.selectbox("Choose series", ("floor_7d", "avg_volume_1d", "volume_1d", "sold_1d"))
        metric = st.selectbox("Choose metric", ("norm", "estimated_returns", "returns", "max_drawdown", "calmar", "sharpe", "sortino"))
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.title(collection)
        ts = cr.load_data(contracts[collection], series)
        forecast = TsForecast(ts)
        qm = QuantMetrics(ts)
        if metric == "norm":
            # TO-DO: create wrapper function where you pass in the function to run
            # e.g. plot.plot(), forecast.cv_ets(), forecast.predict_ets()
            # maybe conflate forecast.create_ts() INSIDE forecast.cv_ets() and forecast.predict_ets()
            # and pass in arguments e.g.
            # if function == 'quant':
            #   display(plot.plot(), metric)
            # elif function == 'predict':
            #   display(forecast.predict_ets(), metric)
            # 
            # commented out for clarity:
            # plt.plot(ts['ds'], ts['y'], color='red')
            forecast.create_ts('y')
            # forecast.cv_ets(30)
            forecast.predict_ets(100)
        elif metric == "estimated_returns":
            qm.estimated_returns()
            plt.plot(ts['ds'], ts['er'], color='red')
        elif metric == "returns":
            qm.calmar(7)
            plt.plot(ts['ds'], ts['returns'], color='red')
        elif metric == "max_drawdown":
            qm.calmar(7)
            plt.plot(ts['ds'], ts['max_drawdown'], color='red')
        elif metric == "calmar":
            qm.calmar(7)
            plt.plot(ts['ds'], ts['calmar'], color='red')
        elif metric == "sharpe":
            qm.sharpe(7)
            plt.plot(ts['ds'], ts['sharpe'], color='red')
        elif metric == 'sortino':
            qm.sortino(7)
            plt.plot(ts['ds'], ts['sortino'], color='red')
        st.pyplot(plt)


if __name__ == '__main__':
    main()
