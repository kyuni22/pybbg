# -*- coding: utf-8 -*-
"""
Edited on 18/01/2017

"""

from __future__ import print_function
import blpapi
from collections import defaultdict
from pandas import DataFrame
from datetime import datetime, date, time
import pandas as pd
import numpy as np
import sys
from pprint import pprint
import logging


class Pybbg():
    def __init__(self, host='localhost', port=8194):
        """
        Starting bloomberg API session
        close with session.close()
        """
        # Fill SessionOptions
        sessionOptions = blpapi.SessionOptions()
        sessionOptions.setServerHost(host)
        sessionOptions.setServerPort(port)

        self.initialized_services = set()

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
        if '//blp/refdata' in self.initialized_services:
            return

        if not self.session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")

        self.session.nextEvent()

        # Obtain previously opened service
        self.refDataService = self.session.getService("//blp/refdata")

        self.session.nextEvent()

        self.initialized_services.add('//blp/refdata')

    def bdh(self, ticker_list, fld_list, start_date, end_date=date.today().strftime('%Y%m%d'), periodselection='DAILY', overrides=None):
        """
        Get ticker_list and field_list
        return pandas multi level columns dataframe
        """
        # Create and fill the request for the historical data
        self.service_refData()

        if isstring(ticker_list):
            ticker_list = [ticker_list]
        if isstring(fld_list):
            fld_list = [fld_list]

        if hasattr(start_date, 'strftime'):
            start_date = start_date.strftime('%Y%m%d')
        if hasattr(end_date, 'strftime'):
            end_date = end_date.strftime('%Y%m%d')

        request = self.refDataService.createRequest("HistoricalDataRequest")
        for t in ticker_list:
            request.getElement("securities").appendValue(t)
        for f in fld_list:
            request.getElement("fields").appendValue(f)
        request.set("periodicityAdjustment", "ACTUAL")
        request.set("periodicitySelection", periodselection)
        request.set("startDate", start_date)
        request.set("endDate", end_date)


        if overrides is not None:
            overrideOuter = request.getElement('overrides')
            for k in overrides:
                override1 = overrideOuter.appendElement()
                override1.setElement('fieldId', k)
                override1.setElement('value', overrides[k])

        # print("Sending Request:", request)
        # Send the request
        self.session.sendRequest(request)
        # defaultdict - later convert to pandas
        data = defaultdict(dict)
        warnings.warn(data)
        # Process received events
        while (True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = self.session.nextEvent(500)
            for msg in ev:
                ticker = msg.getElement('securityData').getElement('security').getValue()
                fieldData = msg.getElement('securityData').getElement('fieldData')
                for i in range(fieldData.numValues()):
                    for j in range(1, fieldData.getValue(i).numElements()):
                        data[(ticker, fld_list[j - 1])][
                            fieldData.getValue(i).getElement(0).getValue()] = fieldData.getValue(i).getElement(
                            j).getValue()

            if ev.eventType() == blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break

        if len(fld_list) == 1:
            data = {k[0]: v for k, v in data.items()}
            data = DataFrame(data)
            data = data[ticker_list]
            data.index = pd.to_datetime(data.index)
            return data

        if len(data) == 0:
            # security error case
            return DataFrame()

        data = DataFrame(data)
        data = data[ticker_list]
        data.columns = pd.MultiIndex.from_tuples(data, names=['ticker', 'field'])
        data.index = pd.to_datetime(data.index)
        return data

    def bdib(self, ticker, fld_list, startDateTime, endDateTime, eventType='TRADE', interval=1):
        """
        Get one ticker (Only one ticker available per call); eventType (TRADE, BID, ASK,..etc); interval (in minutes)
                ; fld_list (Only [open, high, low, close, volumne, numEvents] availalbe)
        return pandas dataframe with return Data
        """
        self.service_refData()
        # Create and fill the request for the historical data
        request = self.refDataService.createRequest("IntradayBarRequest")
        request.set("security", ticker)
        request.set("eventType", eventType)
        request.set("interval", interval)  # bar interval in minutes
        request.set("startDateTime", startDateTime)
        request.set("endDateTime", endDateTime)

        # print "Sending Request:", request
        # Send the request
        self.session.sendRequest(request)
        # defaultdict - later convert to pandas
        data = defaultdict(dict)
        # Process received events
        while (True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = self.session.nextEvent(500)
            for msg in ev:
                barTickData = msg.getElement('barData').getElement('barTickData')
                for i in range(barTickData.numValues()):
                    for j in range(len(fld_list)):
                        data[(fld_list[j])][barTickData.getValue(i).getElement(0).getValue()] = barTickData.getValue(
                            i).getElement(fld_list[j]).getValue()

            if ev.eventType() == blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
        data = DataFrame(data)
        data.index = pd.to_datetime(data.index)
        return data

    def bdp(self, ticker, fld_list, overrides=None):
        # print(ticker, fld_list, overrides)
        self.service_refData()

        request = self.refDataService.createRequest("ReferenceDataRequest")
        if isstring(ticker):
            ticker = [ticker]

        securities = request.getElement("securities")
        for t in ticker:
            securities.appendValue(t)

        if isstring(fld_list):
            fld_list = [fld_list]

        fields = request.getElement("fields")
        for f in fld_list:
            fields.appendValue(f)

        if overrides is not None:
            overrideOuter = request.getElement('overrides')
            for k in overrides:
                override1 = overrideOuter.appendElement()
                override1.setElement('fieldId', k)
                override1.setElement('value', overrides[k])

        self.session.sendRequest(request)
        data = dict()

        while (True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = self.session.nextEvent(500)
            for msg in ev:
                securityData = msg.getElement("securityData")

                for i in range(securityData.numValues()):
                    fieldData = securityData.getValue(i).getElement("fieldData")
                    secId = securityData.getValue(i).getElement("security").getValue()
                    data[secId] = dict()
                    for field in fld_list:
                        if fieldData.hasElement(field):
                            data[secId][field] = fieldData.getElement(field).getValue()
                        else:
                            data[secId][field] = np.NaN

            if ev.eventType() == blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break

        return pd.DataFrame.from_dict(data)

    # def bdp(self, ticker, fld_list):

    #     self.service_refData()

    #     request = self.refDataService.createRequest("ReferenceDataRequest")
    #     if isstring(ticker):
    #         ticker = [ ticker ]

    #     securities = request.getElement("securities")
    #     for t in ticker:
    #         securities.appendValue(t)

    #     if isstring(fld_list):
    #         fld_list = [ fld_list ]

    #     fields = request.getElement("fields")
    #     for f in fld_list:
    #         fields.appendValue(f)


    #     self.session.sendRequest(request)
    #     data = dict()

    #     while(True):
    #         # We provide timeout to give the chance for Ctrl+C handling:
    #         ev = self.session.nextEvent(500)
    #         for msg in ev:
    #             securityData = msg.getElement("securityData")

    #             for i in range(securityData.numValues()):
    #                 fieldData = securityData.getValue(i).getElement("fieldData")
    #                 secId = securityData.getValue(i).getElement("security").getValue()
    #                 data[secId] = dict()
    #                 for field in fld_list:
    #                     if fieldData.hasElement(field):
    #                         data[secId][field] = fieldData.getElement(field).getValue()
    #                     else:
    #                         data[secId][field] = np.NaN



    #         if ev.eventType() == blpapi.Event.RESPONSE:
    #             # Response completly received, so we could exit
    #             break

    #     return pd.DataFrame.from_dict(data)


    def bds(self, security, field, overrides=None):

        self.service_refData()

        request = self.refDataService.createRequest("ReferenceDataRequest")
        assert isstring(security)
        assert isstring(field)

        securities = request.getElement("securities")
        securities.appendValue(security)

        fields = request.getElement("fields")
        fields.appendValue(field)

        if overrides is not None:
            overrideOuter = request.getElement('overrides')
            for k in overrides:
                override1 = overrideOuter.appendElement()
                override1.setElement('fieldId', k)
                override1.setElement('value', overrides[k])

        # print(request)
        self.session.sendRequest(request)
        data = dict()

        while (True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = self.session.nextEvent(500)
            for msg in ev:
                # processMessage(msg)
                securityData = msg.getElement("securityData")
                for i in range(securityData.numValues()):
                    fieldData = securityData.getValue(i).getElement("fieldData").getElement(field)
                    for i, row in enumerate(fieldData.values()):
                        for j in range(row.numElements()):
                            e = row.getElement(j)
                            k = str(e.name())
                            v = e.getValue()
                            if k not in data:
                                data[k] = list()

                            data[k].append(v)

            if ev.eventType() == blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break

        return pd.DataFrame.from_dict(data)

    def stop(self):
        self.session.stop()


def isstring(s):
    # if we use Python 3
    if (sys.version_info[0] == 3):
        return isinstance(s, str)
    # we use Python 2
    return isinstance(s, basestring)


def processMessage(msg):
    SECURITY_DATA = blpapi.Name("securityData")
    SECURITY = blpapi.Name("security")
    FIELD_DATA = blpapi.Name("fieldData")
    FIELD_EXCEPTIONS = blpapi.Name("fieldExceptions")
    FIELD_ID = blpapi.Name("fieldId")
    ERROR_INFO = blpapi.Name("errorInfo")

    securityDataArray = msg.getElement(SECURITY_DATA)
    for securityData in securityDataArray.values():
        print(securityData.getElementAsString(SECURITY))
        fieldData = securityData.getElement(FIELD_DATA)
        for field in fieldData.elements():
            for i, row in enumerate(field.values()):
                for j in range(row.numElements()):
                    e = row.getElement(j)
                    print("Row %d col %d: %s %s" % (i, j, e.name(), e.getValue()))
