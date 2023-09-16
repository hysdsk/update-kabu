import time
from tqdm import tqdm
from .kabudb import Symbol, SymbolsConnector
from .kabusapi import KabusAPI

def main():
    connector = SymbolsConnector()
    api = KabusAPI()
    targets = connector.find_all()
    desc=f"Update infomation for {len(targets)} symbols"
    bar_format="{l_bar}\033[32m{bar}\033[0m{r_bar}"
    for t in tqdm(targets, desc=desc, bar_format=bar_format):
        symbol = api.get_symbol(t["code"], t["exchange_code"])
        if symbol:
            api.put_unregister(t["code"], t["exchange_code"])
            connector.save_one(Symbol(symbol))
        else:
            with open("errors.txt", mode="a", encoding="utf-8") as f:
                f.write(f"{t['code']}@{t['exchange_code']}\n")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
