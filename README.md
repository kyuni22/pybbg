pybbg
=====

python interface to Bloomberg data for Pandas

Prerequisite
=====

[Bloomberg Open API](http://www.openbloomberg.com/open-api/) and python [pandas](http://pandas.pydata.org/)

Install via pip
=====

This package is not yet on pypi manual global install is as follows:

    pip install git+https://github.com/kyuni22/pybbg 

Functions available
=====

New Function beqs

* bdh(tickers, fields, start date, end date, period selection) - similar interface with Bloomberg Excel API's bdh fucntion
	* tickers - one ticker as a string or a list of strings 
	* fields - one field as a string or a list of strings (mnemonics or calcroutes from FLDS screen)
		* if one field is used, the second index on the data frame is removed otherwise a multi-index data frame is used
	* start/end date - end date defaults to today
	* period selection - default to daily
	* overrides - a dictionary, keys map to FLDS fields to overrides, values are the override values
	* other_request_parameters - a dictionary, see `DOCS 2074429 <GO>` page 17 for key/value pairs that are valid here
	* move_dates_to_period_end - boolean - if true forces WEEKLY to the friday of that week, forces MONTHLY to the last calendar day of that month.
* bdp(tickers, fields) - similar to excel bdp
	* tickers - one string or a list of strings
	* fields - one field or a list of fields
	* returns a table where columns are tickers and rows are fields, cell values are values
	* now with overrides
* bds(ticker, field) - similar to excel BDS
	* ticker - one ticker at a time
	* field - one "bulk data" field at a time
	* returns the bulk data table as seen in FLDS as a pandas data frame
* bdib(ticker, field list, start date and time, end date and time, event type, interval) - get intraday bar data and convert to pandas
* beqs(screen name, screen type, group, language)
	* screen name - name of screen in EQS from inside terminal
	* screen type - GLOBAL for bloomberg screens PRIVATE for your custom screens
	* group - name of folder in EQS inside terminal where screen was saved
	* language - desired language of the field names
	* returns a dataframe of the results of the screen (limited to 3,000 rows or 2,999 securities)


Examples
=====
* [bdh and bdib in IPython Notebook](http://nbviewer.ipython.org/github/kyuni22/pybbg/blob/master/BBG_API_test.ipynb?create=1)
* [bdp bds bdh beqs in python unittest](https://github.com/kyuni22/pybbg/blob/master/test_pybbg.py) 
