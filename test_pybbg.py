import unittest
import pybbg
import datetime 

class TestPybbg(unittest.TestCase):
    def test_bdp(self):
        tester = pybbg.Pybbg()
        data = tester.bdp(['AMZN US Equity', 'IBM US Equity'], ['PX_LAST', 'PX_BID', 'PX_ASK'])
        print(data) 

    def test_bds(self):
        tester = pybbg.Pybbg()
        data = tester.bds('EDA Comdty', 'OPT_FUTURES_CHAIN_DATES')
        print(data) 

    def test_bds_col_access(self):
        tester = pybbg.Pybbg()
        data = tester.bds('MSFT US Equity', 'DVD_HIST_ALL')
        print(data['Declared Date'])

    def test_bds_override(self):
        tester = pybbg.Pybbg()
        data = tester.bds('EDA Comdty', 'FUT_CHAIN_LAST_TRADE_DATES', overrides={'INCLUDE_EXPIRED_CONTRACTS': 'Y'})
        print(data) 

    def test_bdh(self):
        tester = pybbg.Pybbg()
        data = tester.bdh(['AMZN US Equity', 'IBM US Equity'], ['PX_LAST', 'PX_BID', 'PX_ASK'], datetime.datetime.today() + datetime.timedelta(days=-10), datetime.datetime.today())
        print(data) 

    def test_bdh_single_field(self):
        tester = pybbg.Pybbg()
        data = tester.bdh(['AMZN US Equity', 'IBM US Equity'], 'PX_LAST', datetime.datetime.today() + datetime.timedelta(days=-10), datetime.datetime.today())
        print(data) 


    def test_bdh_single_field_single_security(self):
        tester = pybbg.Pybbg()
        data = tester.bdh('AMZN US Equity', 'PX_LAST', datetime.datetime.today() + datetime.timedelta(days=-10), datetime.datetime.today())
        print(data) 

    def test_bdp_bad_sec(self):
        tester = pybbg.Pybbg()
        data = tester.bdp('260555 Equity', ['TICKER_AND_EXCH_CODE'])
        print(data)

    def test_bdh_bad_sec(self):
        tester = pybbg.Pybbg()
        data = tester.bdh('260555 Equity', ['PX_LAST','PX_BID','PX_ASK'], datetime.datetime.today() + datetime.timedelta(days=-10), datetime.datetime.today())
        print(data)

if __name__ == '__main__':
    unittest.main()