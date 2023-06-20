import json
import sys

import requests

URL_CURVE = "https://lockers.stakedao.org/api/strategies/cache/curve"
URL_POOL = "https://lockers.stakedao.org/api/lockers/bribes"


def find_best_apr_curve() -> tuple[float, str]:
    return max(
        (k["apr"], k["name"])
        for k in requests.get(URL_CURVE).json()
        if k["futureWeight"] > 0
    )


def find_best_apr_pool() -> tuple[float, tuple[str, str]]:
    return max(
        (k["projectedApr"], (k["name"], k["address"]))
        for k in requests.get(URL_POOL).json()
    )


if __name__ == "__main__":
    match sys.argv[1:]:
        case [] | ["curve"]:
            apr, gauge = find_best_apr_curve()
        case ["pool"]:
            apr, gauge = find_best_apr_pool()
        case _:
            print("Call as get_vote.py [curve, pool]")
            sys.exit(1)
    json.dump((apr, gauge), sys.stdout)
