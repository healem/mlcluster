import json
import os
from pathlib import Path
from polygon import RESTClient


def main():
    key = os.environ.get("POLYGON_KEY")
    res_file = "/tmp/results"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        resp = client.stocks_equities_aggregates("AAPL", 1, "minute", "2019-01-01", "2019-02-01")
        res = Path(res_file)
        with res.open("w") as r:
            r.write(json.dumps(resp))


if __name__ == '__main__':
    main()
