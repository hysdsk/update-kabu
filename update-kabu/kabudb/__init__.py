from configparser import ConfigParser
from mysql.connector.pooling import MySQLConnectionPool

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
        self.cnxpool = MySQLConnectionPool(
            host=config["database"]["db_host"],
            user=config["database"]["db_user"],
            password=config["database"]["db_pswd"],
            database=config["database"]["db_name"],
            pool_size=5)

    def find(self, sql, params=None):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cnx.close()
        return rows
    
    def save(self, sql, params):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(sql, params)
        cursor.close()
        cnx.commit()
        cnx.close()

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
        sql = """
            UPDATE symbols
            SET
                name = %s,
                exchange_code = %s,
                division_code = %s,
                bis_category_code = %s,
                total_market_value = %s,
                total_stocks = %s,
                fiscal_year_end_basic = %s
            WHERE
                code = %s
        """
        super().save(sql, params=(
            symbol.symbolName,
            symbol.exchange,
            self._e2d(symbol.exchangeName),
            symbol.bisCategory,
            symbol.totalMarketValue,
            symbol.totalStocks,
            symbol.fiscalYearEndBasic,
            symbol.symbolCode
        ))

    def _e2d(self, e):
        return {
            "東証プ":      "01",
            "東証ス":      "02",
            "東証グ":      "03",
            "東証プ外":    "11",
            "東証ス外":    "12",
            "東証グ外":    "13",
            "東証ETF/ETN": "21",
            "東証REIT":    "22",
            "東証監理":    "31",
            "東証整理":    "32",
        }.get(e)
