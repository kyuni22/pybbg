pybbg
=====

python interface to Bloomberg data for pandas user


Prerequisite
=====

[Bloomberg Open API](http://www.openbloomberg.com/open-api/) and python [pandas](http://pandas.pydata.org/)


Functions available
=====

New Function bdib is available!

* bdh(tickers, field list, start date, end date, periodselection) - similar interface with Bloomberg Excel API's bdh fucntion
* bdib(ticker, field list, start date and time, end date and time, evnet type, interval) - get intraday bar data and convert to pandas


Install via pip
=====

This package is not yet on pypi manual global install is as follows:


    pip install git+https://github.com/kyuni22/pybbg 



Examples in IPython Notebook
=====
* [bdh and bdib](http://nbviewer.ipython.org/github/kyuni22/pybbg/blob/master/BBG_API_test.ipynb?create=1)
