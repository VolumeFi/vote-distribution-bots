import requests
import sys
import pandas as pd

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

def proportional_weight_curve(n_gauges = 5):
    result = query(URL_CURVE)
    df = pd.DataFrame()
    for k in result.json():
        if k['futureWeight'] > 0:
            df.loc[k['name'],'weight'] = k['futureWeight']

    df = df.sort_values('weight',ascending=False).head(n_gauges)
    df['weight'] = df['weight'] / df['weight'].sum()
    return df.to_dict()

def find_best_apr_pool():
    result = query(URL_POOL)
    best_apr = 0
    best_gauge = None
    for k in result.json():
        if k['futureWeight'] > 0 and k['projectedApr'] > best_apr:
            best_apr = k['projectedApr']
            best_gauge = (k['name'], k['address'])
    return best_apr, best_gauge

def proportional_weight_pool(n_gauges = 5):
    result = query(URL_POOL)
    df = pd.DataFrame()
    for k in result.json():
        if k['futureWeight'] > 0:
            df.loc[k['name'],'weight'] = k['futureWeight']

    df = df.sort_values('weight',ascending=False).head(n_gauges)
    df['weight'] = df['weight'] / df['weight'].sum()
    return df.to_dict()

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == 'curve':
        print(find_best_apr_curve())
    elif sys.argv[1] == 'pool':
        print(find_best_apr_pool())
    elif sys.argv[1] == 'curve-proportional-weight':
        print(proportional_weight_curve())
    elif sys.argv[1] == 'pool-proportional-weight':
        print(proportional_weight_pool())