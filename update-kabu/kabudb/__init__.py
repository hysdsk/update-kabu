from configparser import ConfigParser
from mysql import connector as mc

class Symbol(object):
    def __init__(self, rawdata):
        self.bisCategory =        rawdata["BisCategory"].strip()
        self.totalMarketValue =   rawdata["TotalMarketValue"]
        self.totalStocks =        rawdata["TotalStocks"]
        self.fiscalYearEndBasic = rawdata["FiscalYearEndBasic"]
        self.kcMarginBuy =        rawdata["KCMarginBuy"]
        self.kcMarginSell =       rawdata["KCMarginSell"]
        self.marginBuy =          rawdata["MarginBuy"]
        self.marginSell =         rawdata["MarginSell"]
        self.displayName =        rawdata["DisplayName"].strip()
        self.exchange =           rawdata["Exchange"]
        self.exchangeName =       rawdata["ExchangeName"].strip()
        self.tradingUnit =        rawdata["TradingUnit"]
        self.priceRangeGroup =    rawdata["PriceRangeGroup"]
        self.upperLimit =         rawdata["UpperLimit"]
        self.lowerLimit =         rawdata["LowerLimit"]
        self.symbolCode =         rawdata["Symbol"].strip()
        self.symbolName =         rawdata["SymbolName"].strip()

class Connector(object):
    def __init__(self):
        config = ConfigParser()
        config.read("config.ini")
        self.host = config["database"]["db_host"]
        self.user = config["database"]["db_user"]
        self.pswd = config["database"]["db_pswd"]
        self.name = config["database"]["db_name"]

    def find(self, sql, params=None):
        with mc.connect(host=self.host, user=self.user, password=self.pswd, database=self.name) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def save(self, sql, params):
        with mc.connect(host=self.host, user=self.user, password=self.pswd, database=self.name) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            cursor.close()
            connection.commit()

class SymbolsConnector(Connector):
    def __init__(self):
        super().__init__()

    def find_all(self):
        sql = """
            SELECT
                code,
                exchange_code
            FROM
                symbols
        """
        rows = super().find(sql)
        return [{
            "code": row[0],
            "exchange_code": row[1]
        } for row in rows]

    def save_one(self, symbol: Symbol):
        # TODO: 区分コードも更新する
        sql = """
            UPDATE symbols
            SET
                name = %s,
                exchange_code = %s,
                bis_category_code = %s,
                total_stocks = %s,
                fiscal_year_end_basic = %s
            WHERE
                code = %s
        """
        super().save(sql, params=(
            symbol.symbolName,
            symbol.exchange,
            symbol.bisCategory,
            symbol.totalStocks,
            symbol.fiscalYearEndBasic,
            symbol.symbolCode
        ))
