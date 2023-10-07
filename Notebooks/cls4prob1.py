import qrpm_funcs as qf
import numpy as np
seriesnames=['DGS1MO','DGS3MO','DGS6MO','DGS1','DGS2', \
             'DGS3','DGS5','DGS7','DGS10','DGS20','DGS30']
maturities=qf.TenorsFromNames(seriesnames)
lastday=qf.LastYearEnd()
firstday=qf.LastYearEnd(int(lastday[:4])-1)
dates_dirty,prices_dirty=qf.GetFREDMatrix(seriesnames, \
            startdate=firstday,enddate=lastday)
#remove no-data periods
nan_list=[any(np.isnan(p)) for p in prices_dirty]
prices=[prices_dirty[i] for i in range(len(prices_dirty)) if not nan_list[i]]
dates=[dates_dirty[i] for i in range(len(dates_dirty)) if not nan_list[i]]
