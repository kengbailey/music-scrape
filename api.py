from urllib import request, parse
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TEST_URL = config['API']['TestUrl']
SITE1_POST = config['API']['Site1Post']


def test():
    # try test endpoint of current api
    req = urllib.request.urlopen(TEST_URL)
    print(req.read().decode('utf8'))

def sendJsonToUrl(url, json):
    # send json to urli
    header={'content-type': 'application/json'}
    data = parse.urlencode(json).encode()
    req = request.Request(url=url, data=data, headers=header)
    response = urllib.request.urlopen(req)

if __name__ == "__main__":
    
    # test api 
    test()
