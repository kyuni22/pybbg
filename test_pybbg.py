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

if __name__ == '__main__':
    unittest.main()