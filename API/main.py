#-*- encoding: utf-8 -*-
import pandas as pd
from win32com.client import Dispatch


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

    @staticmethod
    def initialize():
        CybosPlus.CpCybos = Dispatch('CpUtil.CpCybos')
        CybosPlus.CpStockCode = Dispatch('CpUtil.CpStockCode')
        CybosPlus.CpCodeMgr = Dispatch("CpUtil.CpCodeMgr")

        CybosPlus.CpTdUtil = Dispatch("CpTrade.CpTdUtil")
        CybosPlus.CpTradeAccPorfolio = Dispatch("CpTrade.CpTd6033")
        CybosPlus.CpTradeAccBalanceBuy = Dispatch("CpTrade.CpTdNew5331A")
        CybosPlus.CpTradeAccBalanceSell = Dispatch("CpTrade.CpTdNew5331B")

        CybosPlus.CpTradeCashOrder = Dispatch("CpTrade.CpTd0311")
        CybosPlus.CpTradeCancelOrder = Dispatch("CpTrade.CpTd0314")
        CybosPlus.CpTradeOrderStatus = Dispatch("CpTrade.CpTd5341")

        CybosPlus.StockChart = Dispatch("CpSysDib.StockChart")


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
    def trade_init():
        ''' Trade Init Function.

        .. note::

            This function should always be called before doing any trading

        :return int:

            0: success
            -1: error
            1: wrong task key
            2: wrong password
            3: cancelled

        '''
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
        '''Returns account portfolio

        :param str AccountNumber: Account Number
        :return int: Account Balance
        '''
        request_no = 50 # Request no
        CybosPlus.CpTradeAccPorfolio.SetInputValue(0, AccountNumber)
        CybosPlus.CpTradeAccPorfolio.SetInputValue(2, request_no)
        CybosPlus.CpTradeAccPorfolio.BlockRequest()

        no_data = CybosPlus.CpTradeAccPorfolio.GetHeaderValue(7)
        if no_data == 0:
            return -1
        else:
            result = []
            for i in xrange(no_data):
                stock_name = CybosPlus.CpTradeAccPorfolio.GetDataValue(0, i) #stock name
                pay_amount = CybosPlus.CpTradeAccPorfolio.GetDataValue(3, i) #gyeoljaejangosooryang
                trade_amount = CybosPlus.CpTradeAccPorfolio.GetDataValue(7, i) #chaegeoljangosooryang
                eval_price = CybosPlus.CpTradeAccPorfolio.GetDataValue(9, i) #evaluation price
                ROI = CybosPlus.CpTradeAccPorfolio.GetDataValue(11, i)
                sell_available = CybosPlus.CpTradeAccPorfolio.GetDataValue(15, i)
                result.append((stock_name, pay_amount, trade_amount, eval_price, ROI, sell_available))
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
    def get_10_latest_quotes(stockcode):
        ''' Returns 10 latest quotes given the stock code.

        :param str stockcode: stock code
        :return DataFrame: Date, Start, Max, Min, Close
        '''
        CybosPlus.StockChart.SetInputValue(0, stockcode)
        CybosPlus.StockChart.SetInputValue(1, ord('2')) # 1: by date, 2: by number
        CybosPlus.StockChart.SetInputValue(4, 10) # # of Data to Request
        CybosPlus.StockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8)) # Request Data, 0: date, 1, hhmm, 2: hourly, 3: max, 4:min, 5: final, 8: volume
        CybosPlus.StockChart.SetInputValue(6, ord('D')) # 'D': Daily, W, M, m(inutes), T(ick)
        CybosPlus.StockChart.SetInputValue(9, ord('1')) # Adj Price
        CybosPlus.StockChart.BlockRequest()
        num_data = CybosPlus.StockChart.GetHeaderValue(3)
        num_fields = CybosPlus.StockChart.GetHeaderValue(1)

        result = dict()
        for i in xrange(num_data):
            for field in xrange(num_fields):
                val = CybosPlus.StockChart.GetDataValue(field, i)
                if field == 0:
                    if 'Date' not in result.keys():
                        result['Date'] = [val]
                    else:
                        result['Date'].append(val)
                elif field == 1:
                    if 'Start' not in result.keys():
                        result['Start'] = [val]
                    else:
                        result["Start"].append(val)
                elif field == 2:
                    if 'Max' not in result.keys():
                        result['Max'] = [val]
                    else:
                        result['Max'].append(val)
                elif field == 3:
                    if 'Min' not in result.keys():
                        result['Min'] = [val]
                    else:
                        result['Min'].append(val)
                elif field == 4:
                    if 'Close' not in result.keys():
                        result['Close'] = [val]
                    else:
                        result['Close'].append(val)

        result = pd.DataFrame(result, columns=['Date','Start','Min','Max','Close']).sort_values(by=['Date'])
        return result

    @staticmethod
    def buy_order(AccountNumber, StockCode, Amount, Price=None):
        CybosPlus.CpTradeCashOrder.SetInputValue(0, "2") # 1: Sell, 2: Buy
        CybosPlus.CpTradeCashOrder.SetInputValue(1, AccountNumber)
        CybosPlus.CpTradeCashOrder.SetInputValue(3, StockCode)
        CybosPlus.CpTradeCashOrder.SetInputValue(4, Amount) # Amount of shares
        if Price is None:
            CybosPlus.CpTradeCashOrder.SetInputValue(8, "03") # Market Price
        else:
            CybosPlus.CpTradeCashOrder.SetInputValue(5, Price)
        CybosPlus.CpTradeCashOrder.BlockRequest()

        order_type = CybosPlus.CpTradeCashOrder.GetHeaderValue(0)
        order_code = CybosPlus.CpTradeCashOrder.GetHeaderValue(8)

        return order_type, order_code

    @staticmethod
    def sell_order(AccountNumber, StockCode, Amount, Price=None):
        CybosPlus.CpTradeCashOrder.SetInputValue(0, "1") # 1: Sell, 2: Buy
        CybosPlus.CpTradeCashOrder.SetInputValue(1, AccountNumber)
        CybosPlus.CpTradeCashOrder.SetInputValue(3, StockCode)
        CybosPlus.CpTradeCashOrder.SetInputValue(4, Amount) # Amount of shares
        if Price is None:
            CybosPlus.CpTradeCashOrder.SetInputValue(8, "03") # Market Price
        else:
            CybosPlus.CpTradeCashOrder.SetInputValue(5, Price)

        CybosPlus.CpTradeCashOrder.BlockRequest()

        order_type = CybosPlus.CpTradeCashOrder.GetHeaderValue(0)
        order_code = CybosPlus.CpTradeCashOrder.GetHeaderValue(8)

        return order_type, order_code

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
        CybosPlus.CpTradeOrderStatus.SetInputValue(5, 20) # Request #

        CybosPlus.CpTradeOrderStatus.BlockRequest()

        num_data = CybosPlus.CpTradeOrderStatus.GetHeaderValue(6)
        result = []

        for i in xrange(num_data):
            order_no = CybosPlus.CpTradeOrderStatus.GetDataValue(1, i) #order#
            stock_code = CybosPlus.CpTradeOrderStatus.GetDataValue(3, i)
            stock_name = CybosPlus.CpTradeOrderStatus.GetDataValue(4, i)
            info = CybosPlus.CpTradeOrderStatus.GetDataValue(5, i)
            order_amount = CybosPlus.CpTradeOrderStatus.GetDataValue(7, i)

            amount = CybosPlus.CpTradeOrderStatus.GetDataValue(10, i) # Amount Traded
            buy_or_sell = CybosPlus.CpTradeOrderStatus.GetDataValue(35, i) #1: sell 2: buy
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

if __name__ == "__main__":
    CybosPlus.initialize()
    print "Connected: {}".format(CybosPlus.is_connected())
    print CybosPlus.get_stock_name('035420')
    print u"Stock Trade Available: {}".format(CybosPlus.get_count())
    # print CybosPlus.get_stock_code("NAVER")
    print CybosPlus.trade_init()
    AccNo = CybosPlus.get_account_number()[0]
    print CybosPlus.get_account_portfolio(AccNo)

    STOCK_NAME = "NAVER"
    STOCK_CODE = CybosPlus.get_stock_code(STOCK_NAME)
#     toc = time.time()
#     print '''
# STOCK NAME: {}
# STOCK CODE: {}
#     '''.format(STOCK_NAME, STOCK_CODE)
#     print CybosPlus.get_10_latest_quotes(STOCK_CODE)
#     tic = time.time()
    # print "Time elapsed: {:.6f}".format(tic-toc)
    # print CybosPlus.buy_order(AccNo, STOCK_CODE, 10, 850000)
    # print CybosPlus.sell_order(AccNo, STOCK_CODE, 10)
    # print CybosPlus.cancel_order(AccNo, )
    print "Portfolio"
    my_portfolio = CybosPlus.get_account_portfolio(AccNo)
    df = pd.DataFrame(my_portfolio)
    print(df)

    print "Order Status"
    orders = CybosPlus.get_order_status(AccNo)
    df = pd.DataFrame(orders)
    print(df)

    print "Account Balance: KRW {:,}".format(CybosPlus.get_account_balance(AccNo))

    # print CybosPlus.CpCybos.OnDisConnect

