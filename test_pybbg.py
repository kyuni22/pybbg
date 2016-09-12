import unittest
import pybbg
import datetime 
import pybbg.pybbg_k

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

    def test_default_session_pool(self):
        with pybbg.acquire_session() as session: # access the session pool, this acquires a session from the pool and blocks
            assert session is not None
            assert not pybbg.pybbg_k._SESSION_POOL._session_pool.full()

        assert pybbg.pybbg_k._SESSION_POOL._session_pool.full()

    def test_custom_session_pool(self):
        pool = pybbg.SessionPool(8)
        with pool.acquire_session() as session:
            assert session is not None
            assert not pool._session_pool.full()

        assert pool._session_pool.full()


if __name__ == '__main__':
    unittest.main()