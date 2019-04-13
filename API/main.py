# -*- encoding: utf-8 -*-
import multiprocessing
import time

import pywinauto
from win32com.client import Dispatch, DispatchWithEvents

from API.enum_list import order_type_dict
from .enum_list import order_status_dict, order_price_type_dict


def auto_enter_password(pwd, delay):
    app = pywinauto.Application()
    time.sleep(delay)
    try:
        app.connect(title_re=u"CybosPlus 주문확인 설정")
        dlg = app.windows_()
        # app.dlg.PrintControlIdentifiers()
        app.dlg.Edit.TypeKeys(pwd)
        app.dlg.Button.Click()


    except:
        pass


class EventDisconnectHandler:
    def OnDisConnect(self):
        print("Disconnecting..")


class CybosPlus(object):
    CpCybos = None
    CpStockCode = None
    CpCodeMgr = None
    CpTdUtil = None
    CpTradeAccPortfolio = None
    CpTradeAccBalanceBuy = None
    CpTradeAccBalanceSell = None
    CpTradeCashOrder = None
    CpTradeCancelOrder = None
    CpTradeOrderStatus = None
    StockChart = None
    MarketEye = None

    @staticmethod
    def initialize(password=None, delay=1):
        CybosPlus.CpCybos = DispatchWithEvents('CpUtil.CpCybos', EventDisconnectHandler)
        CybosPlus.CpStockCode = Dispatch('CpUtil.CpStockCode')
        CybosPlus.CpCodeMgr = Dispatch("CpUtil.CpCodeMgr")
        CybosPlus.CpTdUtil = Dispatch("CpTrade.CpTdUtil")
        CybosPlus.CpTradeAccPortfolio = Dispatch("CpTrade.CpTd6033")
        CybosPlus.CpTradeAccBalanceBuy = Dispatch("CpTrade.CpTdNew5331A")
        CybosPlus.CpTradeAccBalanceSell = Dispatch("CpTrade.CpTdNew5331B")
        CybosPlus.CpTradeCashOrder = Dispatch("CpTrade.CpTd0311")
        CybosPlus.CpTradeChangePrice = Dispatch("CpTrade.CpTd0313")
        CybosPlus.CpTradeCancelOrder = Dispatch("CpTrade.CpTd0314")
        CybosPlus.CpTradeOrderStatus = Dispatch("CpTrade.CpTd5341")
        CybosPlus.StockChart = Dispatch("CpSysDib.StockChart")
        CybosPlus.MarketEye = Dispatch("CpSysDib.MarketEye")
        CybosPlus.trade_init(password, delay)

    @staticmethod
    def is_connected():
        """ Checks the Connection

        :return: int

            1 = Connected
            0 = Disconnected

        """
        return CybosPlus.CpCybos.IsConnect

    @staticmethod
    def get_stock_name(stockcode):
        """ Stock Code --> Stock Name

        :param str stockcode: Stock Code
        :return str: Stock Name

        """
        return CybosPlus.CpStockCode.CodeToName(stockcode)

    @staticmethod
    def get_stock_code(stock_name):
        ''' Stock Name --> Stock Code

        :param str stock_name: Stock Name
        :return str: Stock Code

        '''
        return CybosPlus.CpStockCode.NameToCode(stock_name)

    @staticmethod
    def get_count():
        ''' Gets total number of stock codes available today

        :return int: number of stock codes

        '''
        return CybosPlus.CpStockCode.GetCount()

    @staticmethod
    def trade_init(password=None, delay=1):
        ''' Trade Init Function.

        .. note::

            This function should always be called before doing any trading

        :param str password: password
        :param int delay: delay
        :return int:

            0: success
            -1: error
            1: wrong task key
            2: wrong password
            3: cancelled

        '''
        if password is not None:
            p = multiprocessing.Process(target=auto_enter_password, args=(password, delay))
            p.start()
            result = CybosPlus.CpTdUtil.TradeInit()
            p.join()
            return result

        return CybosPlus.CpTdUtil.TradeInit()

    @staticmethod
    def get_account_number():
        '''  Returns Account Numbers

        :return: list
        '''
        return CybosPlus.CpTdUtil.AccountNumber

    @staticmethod
    def get_goods_list(AccountNumber, Filter):
        ''' It returns whether Account is eligible for trading (Filter)

        .. todo::

            It is not working as intended

        :param str AccountNumber: Account Number
        :param str Filter: Filter
        :return:
        '''
        return CybosPlus.CpTdUtil.GoodsList(AccountNumber, Filter)

    @staticmethod
    def get_account_portfolio(AccountNumber):
        '''Returns account portfolios

        :param str AccountNumber: Account Number
        :return int: Account Balance
        '''
        request_no = 50  # Request no
        CybosPlus.CpTradeAccPortfolio.SetInputValue(0, AccountNumber)
        CybosPlus.CpTradeAccPortfolio.SetInputValue(2, request_no)
        CybosPlus.CpTradeAccPortfolio.BlockRequest()

        pay_balance_amount = CybosPlus.CpTradeAccPortfolio.GetHeaderValue(1)
        sign_balance_amount = CybosPlus.CpTradeAccPortfolio.GetHeaderValue(2)
        evaluation_price = CybosPlus.CpTradeAccPortfolio.GetHeaderValue(3)
        evaluation_diff = CybosPlus.CpTradeAccPortfolio.GetHeaderValue(4)
        no_data = CybosPlus.CpTradeAccPortfolio.GetHeaderValue(7)
        total_return = CybosPlus.CpTradeAccPortfolio.GetHeaderValue(8)
        d2_expect_evaluation = CybosPlus.CpTradeAccPortfolio.GetHeaderValue(9)

        result = {
            "pay_balance_amount": pay_balance_amount,
            "sign_balance_amount": sign_balance_amount,
            "evaluation_price": evaluation_price,
            "evaluation_diff": evaluation_diff,
            "count": no_data,
            "total_return": total_return,
            "d2_expect_evaluation": d2_expect_evaluation,
            "portfolios": [],
        }
        if no_data == 0:
            return -1
        else:
            for i in range(no_data):
                stock_name = CybosPlus.CpTradeAccPortfolio.GetDataValue(0, i)  # stock name
                # pay_amount = CybosPlus.CpTradeAccPorfolio.GetDataValue(3, i) #gyeoljaejangosooryang
                trade_amount = CybosPlus.CpTradeAccPortfolio.GetDataValue(7, i)  # chaegeoljangosooryang
                eval_price = CybosPlus.CpTradeAccPortfolio.GetDataValue(9, i)  # evaluation price
                eval_return = CybosPlus.CpTradeAccPortfolio.GetDataValue(10, i)  # evaluation return
                ROI = CybosPlus.CpTradeAccPortfolio.GetDataValue(11, i)
                stock_code = CybosPlus.CpTradeAccPortfolio.GetDataValue(12, i)  # stock_code
                sell_available = CybosPlus.CpTradeAccPortfolio.GetDataValue(15, i)
                purchase_price = CybosPlus.CpTradeAccPortfolio.GetDataValue(17, i)  # purchase price
                stock = {"stock_name": stock_name, "stock_code": stock_code, "trade_shares": trade_amount,
                         "purchase_price": purchase_price,
                         "evaluation": eval_price, "return": ROI, "sell_available": sell_available,
                         "eval_return": eval_return}
                result['portfolios'].append(stock)
            return result

    @staticmethod
    def get_limit_remain_time():
        '''Returns Limit Remaining Time

        :returns: remaining time (refresh time in seconds)
        '''
        return CybosPlus.CpCybos.LimitRequestRemainTime / 1000.0

    @staticmethod
    def get_limit_remain_count(limit_type):
        '''Get Limit Count

        :param int limit_type: 0: Order Request, 1: Quote Request Limit
        :return int:
        '''
        if limit_type == 0:
            limit_type = 0  # "LT_TRADE_REQUEST"
        elif limit_type == 1:
            limit_type = 1  # "LT_NONTRADE_REQUEST"

        return CybosPlus.CpCybos.GetLimitRemainCount(limit_type)

    @staticmethod
    def get_quote_by_date(stock_code, begin_date, end_date=0):
        """ Get Stock Quote on the given date

        :param str stock_code: stock code
        :param begin_date: YYYYMMDD
        :param end_date: YYYYMMDD
        :return:
        """
        scObject = CybosPlus.StockChart
        scObject.SetInputValue(0, stock_code)
        scObject.SetInputValue(1, ord('1'))  # request by date
        scObject.SetInputValue(2, end_date)  # end_date
        scObject.SetInputValue(3, begin_date)  # begin_date
        scObject.SetInputValue(4, 1000)
        """
        0 - date
        2 - start
        3 - high
        4 - low
        5 - close
        6 - relative to yesterday
        8 - trade_volume
        12 - share available
        13 - market volume
        """
        request_fields = (0, 5, 8, 12, 13)
        scObject.SetInputValue(5, request_fields)
        scObject.SetInputValue(6, ord('D'))  # daily
        scObject.SetInputValue(9, ord('1'))  # adjusted
        scObject.BlockRequest()

        num_of_data_fields = scObject.GetHeaderValue(1)
        field_name_list = scObject.GetHeaderValue(2)
        how_many_data = scObject.GetHeaderValue(3)
        current_price = scObject.GetHeaderValue(7)
        current_status = scObject.GetHeaderValue(17)

        result = dict()
        data = []
        for i in range(how_many_data):
            temp = dict()
            for field_idx, field_name in zip(range(num_of_data_fields), field_name_list):
                val = scObject.GetDataValue(field_idx, i)
                temp[field_name] = val
            data.append(temp)
        result['data'] = data
        result['current_price'] = current_price
        result['current_status'] = order_status_dict[chr(current_status)]
        return result

    @staticmethod
    def get_account_balance(AccountNumber):
        """Get Account Balance

        :param AccountNumber:
        :return:
        """
        object = CybosPlus.CpTradeAccBalanceBuy
        object.SetInputValue(0, AccountNumber)
        object.BlockRequest()
        return object.GetHeaderValue(10)

    @staticmethod
    def get_quote_by_count(stockcode, count=10):
        ''' Returns 10 latest quotes given the stock code.

        :param str stockcode: stock code
        :return DataFrame: Date, Start, Max, Min, Close
        '''
        CybosPlus.StockChart.SetInputValue(0, stockcode)
        CybosPlus.StockChart.SetInputValue(1, ord('2'))  # 1: by date, 2: by number

        CybosPlus.StockChart.SetInputValue(4, count)  # # of Data to Request
        CybosPlus.StockChart.SetInputValue(5, (0, 5, 8, 12, 13, 25))
        # Request Data, 0: date, 1, hhmm, 2: open, 3: high, 4:low, 5: close, 8: volume
        # 12: 상 장 주 식 수, 13: 시가 총액, 25: 주 식 회 전 율
        CybosPlus.StockChart.SetInputValue(6, ord('D'))  # 'D': Daily, W, M, m(inutes), T(ick)
        CybosPlus.StockChart.SetInputValue(9, ord('1'))  # Adj Price
        CybosPlus.StockChart.BlockRequest()

        num_fields = CybosPlus.StockChart.GetHeaderValue(1)
        field_names = CybosPlus.StockChart.GetHeaderValue(2)
        num_data = CybosPlus.StockChart.GetHeaderValue(3)
        current_status = chr(CybosPlus.StockChart.GetHeaderValue(17))

        result = dict()
        data = []
        for i in range(num_data):
            temp = dict()
            for field_name, field in zip(field_names, range(num_fields)):
                val = CybosPlus.StockChart.GetDataValue(field, i)
                temp[field_name] = val
            data.append(temp)
        result['data'] = data
        result['current_status'] = order_status_dict[current_status]
        result['stock_name'] = CybosPlus.get_stock_name(stockcode)
        return result

    @staticmethod
    def buy_order(AccountNumber, StockCode, Amount, Price=0):
        CybosPlus.CpTradeCashOrder.SetInputValue(0, "2")  # 1: Sell, 2: Buy
        CybosPlus.CpTradeCashOrder.SetInputValue(1, AccountNumber)
        CybosPlus.CpTradeCashOrder.SetInputValue(3, StockCode)
        CybosPlus.CpTradeCashOrder.SetInputValue(4, Amount)  # Amount of shares
        if Price == 0:
            CybosPlus.CpTradeCashOrder.SetInputValue(8, "03")  # Market Price
        else:
            CybosPlus.CpTradeCashOrder.SetInputValue(5, Price)
        CybosPlus.CpTradeCashOrder.BlockRequest()

        order_type = order_type_dict(CybosPlus.CpTradeCashOrder.GetHeaderValue(0))
        stock_code = CybosPlus.CpTradeCashOrder.GetHeaderValue(3)
        order_amount = CybosPlus.CpTradeCashOrder.GetHeaderValue(4)
        order_price = CybosPlus.CpTradeCashOrder.GetHeaderValue(5)
        order_id = CybosPlus.CpTradeCashOrder.GetHeaderValue(8)
        stock_name = CybosPlus.CpTradeCashOrder.GetHeaderValue(10)
        order_price_type = order_price_type_dict[CybosPlus.CpTradeCashOrder.GetHeaderValue(13)]

        result = {
            "order_type": order_type,  # buy / sell,
            "stock_code": stock_code,
            "order_amount": order_amount,
            "order_price": order_price,
            "order_id": order_id,  # 주문번호
            "stock_name": stock_name,
            "order_price_type": order_price_type  # 보통, 임의, 시장가,
        }

        return result

    @staticmethod
    def sell_order(AccountNumber, StockCode, Amount, Price=None):
        CybosPlus.CpTradeCashOrder.SetInputValue(0, "1")  # 1: Sell, 2: Buy
        CybosPlus.CpTradeCashOrder.SetInputValue(1, AccountNumber)
        CybosPlus.CpTradeCashOrder.SetInputValue(3, StockCode)
        CybosPlus.CpTradeCashOrder.SetInputValue(4, Amount)  # Amount of shares
        if Price is None:
            CybosPlus.CpTradeCashOrder.SetInputValue(8, "03")  # Market Price
        else:
            CybosPlus.CpTradeCashOrder.SetInputValue(5, Price)

        CybosPlus.CpTradeCashOrder.BlockRequest()

        order_type = order_type_dict(CybosPlus.CpTradeCashOrder.GetHeaderValue(0))
        stock_code = CybosPlus.CpTradeCashOrder.GetHeaderValue(3)
        order_amount = CybosPlus.CpTradeCashOrder.GetHeaderValue(4)
        order_price = CybosPlus.CpTradeCashOrder.GetHeaderValue(5)
        order_id = CybosPlus.CpTradeCashOrder.GetHeaderValue(8)
        stock_name = CybosPlus.CpTradeCashOrder.GetHeaderValue(10)
        order_price_type = order_price_type_dict[CybosPlus.CpTradeCashOrder.GetHeaderValue(13)]

        result = {
            "order_type": order_type,  # buy / sell,
            "stock_code": stock_code,
            "order_amount": order_amount,
            "order_price": order_price,
            "order_id": order_id,  # 주문번호
            "stock_name": stock_name,
            "order_price_type": order_price_type  # 보통, 임의, 시장가,
        }

        return result

    @staticmethod
    def change_order_price(AccountNumber, OrderNumber, StockCode, NewPrice, Amount=0):
        """
        TODO: Implement to change a price of the order.

        :param AccountNumber:
        :param OrderNumber:
        :param StockCode:
        :param NewPrice:
        :param Amount:
        :return:
        """
        pass

    @staticmethod
    def cancel_order(AccountNumber, OrderNumber, StockCode, Amount=0):
        CybosPlus.CpTradeCancelOrder.SetInputValue(1, OrderNumber)
        CybosPlus.CpTradeCancelOrder.SetInputValue(2, AccountNumber)
        CybosPlus.CpTradeCancelOrder.SetInputValue(4, StockCode)
        CybosPlus.CpTradeCancelOrder.SetInputValue(5, Amount)

        CybosPlus.CpTradeCancelOrder.BlockRequest()

        cancel_amount = CybosPlus.CpTradeCancelOrder.GetHeaderValue(5)
        new_order_number = CybosPlus.CpTradeCancelOrder.GetHeaderValue(6)

        return new_order_number, cancel_amount

    @staticmethod
    def get_order_status(AccNo, StockCode="", orderNo=0):
        CybosPlus.CpTradeOrderStatus.SetInputValue(0, AccNo)
        CybosPlus.CpTradeOrderStatus.SetInputValue(2, StockCode)
        CybosPlus.CpTradeOrderStatus.SetInputValue(3, orderNo)
        CybosPlus.CpTradeOrderStatus.SetInputValue(5, 20)  # Request #

        CybosPlus.CpTradeOrderStatus.BlockRequest()

        num_data = CybosPlus.CpTradeOrderStatus.GetHeaderValue(6)
        result = []

        for i in range(num_data):
            order_no = CybosPlus.CpTradeOrderStatus.GetDataValue(1, i)  # order#
            stock_code = CybosPlus.CpTradeOrderStatus.GetDataValue(3, i)
            stock_name = CybosPlus.CpTradeOrderStatus.GetDataValue(4, i)
            info = CybosPlus.CpTradeOrderStatus.GetDataValue(5, i)
            order_amount = CybosPlus.CpTradeOrderStatus.GetDataValue(7, i)

            amount = CybosPlus.CpTradeOrderStatus.GetDataValue(10, i)  # Amount Traded
            buy_or_sell = CybosPlus.CpTradeOrderStatus.GetDataValue(35, i)  # 1: sell 2: buy
            if buy_or_sell == 1:
                buy_or_sell = "Sell"
            else:
                buy_or_sell = "Buy"
            result.append((order_no, stock_code, stock_name, info, order_amount, amount, buy_or_sell))
        return result

    @staticmethod
    def get_market_start_time():
        '''Returns market start time

        :return int:  9 - 09:00 , 15:00 - 03:00pm
        '''
        return CybosPlus.CpCodeMgr.GetMarketStartTime()

    @staticmethod
    def get_market_close_time():
        '''Returns market close time

        :return int:
        '''
        return CybosPlus.CpCodeMgr.GetMarketEndTime()

    @staticmethod
    def get_many_info(stock_list):
        """
        여러 주식에 대한 정보를 입력 받음
        :param stock_list (list):
        :return 정보들:
        """
        object = CybosPlus.MarketEye
        request_fields = (0, 1, 4, 10, 12, 17, 20, 22, 23, 24, 25, 63, 64, 67, 70,
                          83)  # http://cybosplus.github.io/cpsysdib_rtf_1_/marketeye.htm

        object.SetInputValue(0, request_fields)
        object.SetInputValue(1, stock_list)
        object.BlockRequest()

        how_many_fields = object.GetHeaderValue(0)
        field_names = object.GetHeaderValue(1)
        how_many_records = object.GetHeaderValue(2)

        result = []
        for i in range(how_many_records):
            record = dict()
            for f_idx, fieldName in zip(range(how_many_fields), field_names):
                data = object.GetDataValue(f_idx, i)
                record[fieldName] = data
            result.append(record)

        return result


if __name__ == "__main__":
    CybosPlus.initialize(password="0302", delay=0)
    print("Connected: {}".format(CybosPlus.is_connected()))
    account_no = CybosPlus.get_account_number()[0]
