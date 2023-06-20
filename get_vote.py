import requests
import sys

URL_CURVE = "https://lockers.stakedao.org/api/strategies/cache/curve"
URL_POOL = "https://lockers.stakedao.org/api/lockers/bribes"

def query(url):
    result = requests.get(url)
    return result

def find_best_apr_curve():
    result = query(URL_CURVE)
    best_apr = 0
    best_gauge = None
    for k in result.json():
        if k['futureWeight'] > 0 and k['apr'] > best_apr:
            best_apr = k['apr']
            best_gauge = k['name']
    return best_apr, best_gauge

def find_best_apr_pool():
    result = query(URL_POOL)
    best_apr = 0
    best_gauge = None
    for k in result.json():
        if k['futureWeight'] > 0 and k['projectedApr'] > best_apr:
            best_apr = k['projectedApr']
            best_gauge = (k['name'], k['address'])
    return best_apr, best_gauge

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == 'curve':
        print(find_best_apr_curve())
    elif sys.argv[1] == 'pool':
        print(find_best_apr_pool())