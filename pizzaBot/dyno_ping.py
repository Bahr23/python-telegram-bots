import os
import requests

if __name__ == '__main__':
    print('Pings PING_URL to keep a dyno alive')
    requests.get(os.environ['HEROKU_URL'])
