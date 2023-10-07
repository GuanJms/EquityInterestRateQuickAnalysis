#


import json
import qrpm_funcs_modified as qf
import numpy as np
from datetime import datetime
import pandas as pd
import os
class InterestRateCurveData:
    def __init__(self):
        self._API_KEY = None
        self._TREASURY_TICKER_LIST=['DGS1MO','DGS3MO','DGS6MO','DGS1','DGS2','DGS3','DGS5','DGS7','DGS10','DGS20','DGS30']
        self._MATURITIES =qf.TenorsFromNames(self._TREASURY_TICKER_LIST)
        self._END_DATE = None
        self._START_DATE = None
        self._DATA = None
        self._DATA_PATH = None
        self.run_config()


    def run_config(self, filename="config.json"):
        with open(filename, "r") as file:
            config = json.load(file)
        try:
            self._API_KEY = config['API_KEY']
        except:
            print("Configuration failed; No API_KEY found")
        pass

    def date_input(self, date1, date2, format = "%Y-%m-%d"):
        # TODO: implement the case where there is data change - rerun bond_data- overlapping etc
        date1 = datetime.strptime(date1, format)
        date2 = datetime.strptime(date2, format)
        if date1 > date2:
            self._START_DATE = date2
            self._END_DATE = date1
        else:
            self._START_DATE = date1
            self._END_DATE = date2

    def bond_data(self):
        self._DATA_PATH = os.path.join("datasets", "treasury")
        self._FILE_PATH = os.path.join(self._DATA_PATH, f"t_{self._START_DATE.strftime('%Y_%m_%d')}_{self._END_DATE.strftime('%Y_%m_%d')}")
        if not os.path.isdir(self._DATA_PATH):
            os.makedirs(self._DATA_PATH)
        if not os.path.isfile(self._FILE_PATH):  # download data if not already there
            dates_dirty, prices_dirty = qf.GetFREDMatrix(self._TREASURY_TICKER_LIST,startdate=self._START_DATE, enddate=self._END_DATE,API_KEY=self._API_KEY)
            nan_list = [any(np.isnan(p)) for p in prices_dirty]
            prices = [prices_dirty[i] for i in range(len(prices_dirty)) if not nan_list[i]]
            dates = [dates_dirty[i] for i in range(len(dates_dirty)) if not nan_list[i]]
            self._DATA = pd.DataFrame(prices, index=dates, columns=self._TREASURY_TICKER_LIST)
            self._DATA.to_csv( self._FILE_PATH)
        else:
            self._DATA = pd.read_csv(self._FILE_PATH, index_col=0, parse_dates=True)
        return self._DATA

