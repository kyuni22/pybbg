# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 13:47:12 2014

@author: kian
"""

import blpapi
from collections import defaultdict
from pandas import DataFrame
from datetime import datetime, date, time
import pandas as pd

class Pybbg():
    def __init__(self, host='localhost', port=8194):
        """
        Starting bloomberg API session
        close with session.close()
        """
        # Fill SessionOptions
        sessionOptions = blpapi.SessionOptions()
        sessionOptions.setServerHost('localhost')
        sessionOptions.setServerPort(8194)
    
        # Create a Session
        self.session = blpapi.Session(sessionOptions)
    
        # Start a Session
        if not self.session.start():
            print("Failed to start session.")
        
        self.session.nextEvent()
        
    def service_refData(self):
        """
        init service for refData
        """
        # Open service to get historical data from
        if not self.session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")
        
        self.session.nextEvent()
        
        # Obtain previously opened service
        self.refDataService = self.session.getService("//blp/refdata")
        
        self.session.nextEvent() 
    
    def bdh(self, ticker_list, fld_list, start_date, end_date=date.today().strftime('%Y%m%d'), periodselection = 'DAILY'):
        """
        Get ticker_list and field_list
        return pandas multi level columns dataframe
        """
        # Create and fill the request for the historical data
        request = self.refDataService.createRequest("HistoricalDataRequest")
        for t in ticker_list:
            request.getElement("securities").appendValue(t)       
        for f in fld_list :
            request.getElement("fields").appendValue(f)
        request.set("periodicityAdjustment", "ACTUAL")
        request.set("periodicitySelection", periodselection)
        request.set("startDate", start_date)
        request.set("endDate", end_date)
        
        #print("Sending Request:", request)
        # Send the request
        self.session.sendRequest(request)
        # defaultdict - later convert to pandas
        data = defaultdict(dict)
        # Process received events
        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = self.session.nextEvent(500)
            for msg in ev:
                ticker = msg.getElement('securityData').getElement('security').getValue()
                fieldData = msg.getElement('securityData').getElement('fieldData')
                for i in range(fieldData.numValues()) :
                    for j in range(1,fieldData.getValue(i).numElements()) :
                        data[(ticker, fld_list[j-1])][fieldData.getValue(i).getElement(0).getValue()] = fieldData.getValue(i).getElement(j).getValue()
        
            if ev.eventType() == blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
        data = DataFrame(data)
        data.columns = pd.MultiIndex.from_tuples(data, names=['ticker', 'field'])
        data.index = pd.to_datetime(data.index)
        return data

    def bdib(self, ticker, fld_list, startDateTime, endDateTime, eventType='TRADE', interval = 1):
        """
        Get one ticker (Only one ticker available per call); eventType (TRADE, BID, ASK,..etc); interval (in minutes)
                ; fld_list (Only [open, high, low, close, volumne, numEvents] availalbe)
        return pandas dataframe with return Data
        """
        # Create and fill the request for the historical data
        request = self.refDataService.createRequest("IntradayBarRequest")
        request.set("security", ticker)
        request.set("eventType", eventType)
        request.set("interval", interval)  # bar interval in minutes        
        request.set("startDateTime", startDateTime)
        request.set("endDateTime", endDateTime)
        
        #print "Sending Request:", request
        # Send the request
        self.session.sendRequest(request)
        # defaultdict - later convert to pandas
        data = defaultdict(dict)
        # Process received events
        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = self.session.nextEvent(500)
            for msg in ev:
                barTickData = msg.getElement('barData').getElement('barTickData')
                for i in range(barTickData.numValues()) :
                    for j in range(len(fld_list)) :
                        data[(fld_list[j])][barTickData.getValue(i).getElement(0).getValue()] = barTickData.getValue(i).getElement(fld_list[j]).getValue()
        
            if ev.eventType() == blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
        data = DataFrame(data)
        data.index = pd.to_datetime(data.index)
        return data
        
    def stop(self):
        self.session.stop()