import time
from .kabudb import Symbol, SymbolsConnector
from .kabusapi import KabusAPI

def main():
    connector = SymbolsConnector()
    api = KabusAPI()

    targets = connector.find_all()
    total = len(targets)
    count = 0
    for t in targets:
        symbol = api.get_symbol(t["code"], t["exchange_code"])
        if symbol:
            api.put_unregister(t["code"], t["exchange_code"])
            connector.save_one(Symbol(symbol))
        else:
            with open("errors.txt", mode="a", encoding="utf-8") as f:
                f.write(f"{t['code']}@{t['exchange_code']}\n")
        # 進捗表示
        print(f"Symbol: {t['code']} ... {(count:=count+1)}/{total}")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
