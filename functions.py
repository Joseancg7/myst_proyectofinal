
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

from datetime import timedelta, datetime
import pandas as pd
import numpy as np


def f_compare_ts(ts_list_o, ts_list_d):
    ts_list_o_dt = [datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%fZ") for i in ts_list_o]
    ts_list_d_dt = [datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%fZ") for i in ts_list_d]
    f_compare_ts = {}
    f_compare_ts['first_o'] = min(ts_list_o_dt).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    f_compare_ts['last_o'] = max(ts_list_o_dt).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    f_compare_ts['qty_o'] = len(ts_list_o_dt)
    f_compare_ts['first_d'] = min(ts_list_d_dt).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    f_compare_ts['last_d'] = max(ts_list_d_dt).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    f_compare_ts['qty_d'] = len(ts_list_d_dt)
    unique_dates = list(dict.fromkeys(ts_list_o_dt + ts_list_d_dt))
    exact_matches = [i for i in unique_dates if (i in (ts_list_o_dt) and i in (ts_list_d_dt))]
    f_compare_ts['exact_match'] = {"qty": len(exact_matches), "values": exact_matches}
    return f_compare_ts


def historical_spread(ob_data):
    k = list(ob_data.keys())
    lowest_asks = []
    highest_bids = []
    spreads = []
    for i in k:
        lowest_asks.append(ob_data[i].ask.min())
        highest_bids.append(ob_data[i].bid.max())
        spreads.append(abs(ob_data[i].ask.min() - ob_data[i].bid.max()))

    df_ts_tob = pd.DataFrame()
    df_ts_tob["timestamp"] = k
    df_ts_tob["bid"] = highest_bids
    df_ts_tob["ask"] = lowest_asks
    df_ts_tob["spread"] = spreads
    return df_ts_tob

def vwap(ob_data):
    k = list(ob_data.keys())
    max_ask = []
    max_bid =[]
    vwap = []
    for i in range(len(ob_data)):
        ob_data[list(ob_data.keys())[i]]['vwap']=(ob_data[list(ob_data.keys())[i]]['bid_size']*ob_data[list(ob_data.keys())[i]]['bid']+
                                                  ob_data[list(ob_data.keys())[i]]['ask_size']*ob_data[list(ob_data.keys())[i]]['ask'])/(ob_data[list(ob_data.keys())[i]]['bid_size']+ob_data[list(ob_data.keys())[i]]['ask_size'])
    for i in range(len(k)):
        max_ask.append(ob_data[list(ob_data.keys())[i]]['ask'].mean())
        max_bid.append(ob_data[list(ob_data.keys())[i]]['bid'].mean())
        vwap.append(ob_data[list(ob_data.keys())[i]]['vwap'].mean())

    df_vwap = pd.DataFrame()
    df_vwap["timestamp"] = k
    df_vwap["bid"] = max_bid
    df_vwap["ask"] = max_ask
    df_vwap["vwap"] = vwap
    return df_vwap

def roll_model(df_ts_tob, gamma_0, gamma_1):
    C = -np.sqrt(gamma_1)
    var_iid = gamma_0 - 2*C*C
    m_0 = df_ts_tob["mid"][0]
    df_ts_tob["bid_roll"] = m_0
    df_ts_tob["ask_roll"] = m_0
    for i in range(len(df_ts_tob)-1):
        u_t = np.random.normal(0,np.sqrt(var_iid))
        df_ts_tob.at[i+1,"bid_roll"] = df_ts_tob.at[i,"mid"] + u_t - C
        df_ts_tob.at[i+1,"ask_roll"] = df_ts_tob.at[i,"mid"] + u_t + C
    return df_ts_tob


def martingala(pdataframe: 'DataFrame with data', column_name: str):
    mtgala = np.zeros(len(pdataframe[column_name]))
    for i in range(len(pdataframe[column_name])-1):
        if pdataframe[column_name][i] == pdataframe[column_name][i+1]:
            mtgala[i+1] = mtgala[i] + 1
        
    mtgala = list(map(lambda x: format(x, '.0f'), mtgala))
    mtgala = list(map(lambda x: int(x), mtgala))
    
    mtgala_r = [mtgala[i] for i in range(len(mtgala)-1) if mtgala[i+1] == 0]
    nonzeros = np.count_nonzero(mtgala_r)
    zeros = len(mtgala_r) - nonzeros
    
    mtgala_pd = pd.DataFrame()
    mtgala_pd['Type'] = ['Zeros', 'Non Zeros']
    mtgala_pd['Zeros vs Non Zeros'] = [zeros, nonzeros]
    
    return mtgala_pd
