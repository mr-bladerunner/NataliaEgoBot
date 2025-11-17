import requests
import pandas as pd
import numpy as np
from io import StringIO
from typing import List, Dict

def fetch_hev_reference_rates() -> List[Dict]:
    url = "https://immo-erben.ch/know-how/der-referenzzinssatz-und-seine-entwicklung/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))
    df = tables[0]
    df.columns = ["Leitzins", "Referenzzinssatz", "Gueltig ab", "Durchschnittszinssatz"]

    for col in ["Leitzins", "Referenzzinssatz", "Durchschnittszinssatz"]:
        df[col] = (
            df[col]
            .replace("-", np.nan)
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    df["Gueltig ab"] = pd.to_datetime(df["Gueltig ab"], format="%d.%m.%Y", errors="coerce")
    df["Jahr"] = df["Gueltig ab"].dt.year.astype(str)

    return df.to_dict(orient="records")

# Для теста отдельного запуска:
if __name__ == "__main__":
    data = fetch_hev_reference_rates()
    print(pd.DataFrame(data))
