import urllib.request
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TEST_URL = config['API']['TestUrl']
SITE1_POST = config['API']['Site1Post']


def test():
    # try test endpoint of current api
    req = urllib.request.urlopen(TEST_URL)
    print(req.read().decode('utf8'))

if __name__ == "__main__":
    
    # test api 
    test()
