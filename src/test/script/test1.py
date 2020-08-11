#!/usr/bin/env python3
#
# Created: August 2020
# Author: Aaron Mansheim <aaron.mansheim@gmail.com>

import json
import urllib.request

class LCSClient:
    def __init__(self, values, hostname='localhost', port=80, **kwargs):
        port_part = '' if port == 80 else f':{port}'
        self.url = f'http://{hostname}{port_part}/lcs'
        self.values = values
        self.jsonify_request()

        import http.client
        import urllib.request
        request = urllib.request.Request(self.url, method='POST')
        request.data = bytes(self.request_json, 'utf-8')
        self.request = request 
        self.execute()
        self.parse_response()

    def execute(self):
        # print('<<<{}>>>'.format(self.request.full_url))
        with urllib.request.urlopen(self.request) as response:
            self.response_body = response.read()
        # print('[[[{}]]]'.format(self.response_body ))

    def jsonify_request(self):
        self.request_json = json.dumps(
                { "setOfStrings": [ {"value": v} for v in self.values ] },
                separators=(',', ':'))

    def parse_response(self):
        response_object = json.loads(self.response_body)
        self.lcs = [x['value'] for x in response_object['lcs']]

class MockLCSClient(LCSClient):
    def __init__(self, response_body, **kwargs):
        self.future_response_body = response_body
        super().__init__(**kwargs)

    def execute(self):
        print(self.request_json)
        self.response_body = self.future_response_body
        print(self.response_body)

def test1(lcs_cls, **params):
    x = lcs_cls(values='comcast comcastic broadcaster'.split(' '), **params)
    print(x.lcs)

def test2(lcs_cls, **params):
    x = lcs_cls(values='comcast communicate commutation'.split(' '), **params)
    print(x.lcs)

def test3(lcs_cls, **params):
    x = lcs_cls(values='uabcvmnowabcxpqry vdefwmnoxdefypqrz'.split(' '), **params)
    print(x.lcs)

if __name__ == '__main__':
    import sys
    hostname = 'localhost'
    if 1 < len(sys.argv):
        hostname = sys.argv[0]

    #test1(MockLCSClient, response_body='{"lcs":[{"value":"cast"}]}')
    #test2(MockLCSClient, response_body='{"lcs":[{"value":"com"}]}')
    port = 53792
    test1(LCSClient, hostname=hostname, port=port)
    test2(LCSClient, hostname=hostname, port=port)
    test3(LCSClient, hostname=hostname, port=port)

