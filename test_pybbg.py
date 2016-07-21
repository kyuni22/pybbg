import unittest
import pybbg

class TestPybbg(unittest.TestCase):

  def test_bdp(self):
    tester = pybbg.Pybbg()
    tester.service_refData()
    data = tester.bdp(['AMZN US Equity', 'IBM US Equity'], ['PX_LAST', 'PX_BID', 'PX_ASK'])
    print(data) 


if __name__ == '__main__':
    unittest.main()