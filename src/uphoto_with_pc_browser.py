# -*- coding: utf-8 -*-

#
# 완전 자동화 되지않은 버전 - PC 브라우저를 통해 인증
#

import urllib
import urllib2
import webbrowser
import BaseHTTPServer
import urlparse
import sys
import facebook

APP_ID = '562093157232794'
APP_SECRET = 'b1ec7582e8bbe78b6f043e6e5a6ff052'

ENDPOINT = 'graph.facebook.com'
REDIRECT_URI = 'http://192.168.80.27:8000/'
ACCESS_TOKEN = None


def get_url(path, args=None):
    args = args or {}

    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://" + ENDPOINT
    else:
        endpoint = "http://" + ENDPOINT

    return endpoint + path + '?' + urllib.urlencode(args)


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        global ACCESS_TOKEN
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
        code = code[0] if code else None
        print '>> CODE : ' + code

        if code is None:
            self.wfile.write("Sorry, authentication failed.")
            sys.exit(1)

        fb_get_access_token_url = get_url('/oauth/access_token',
              {'client_id': APP_ID, 'redirect_uri':REDIRECT_URI, 'client_secret': APP_SECRET, 'code': code})

        ret = urllib2.urlopen(fb_get_access_token_url).read()
        ACCESS_TOKEN = urlparse.parse_qs(ret)['access_token'][0]
        print '>> ACCESS_TOKEN : ' + ACCESS_TOKEN


if __name__ == '__main__':

    httpd = BaseHTTPServer.HTTPServer(('192.168.80.27', 8000), RequestHandler)

    # Logging you in to facebook
    fb_auth_url = get_url('/oauth/authorize',
              {'client_id': APP_ID, 'redirect_uri': REDIRECT_URI, 'scope': 'publish_actions'})
    print '>> fb_auth_url : ' + fb_auth_url
    webbrowser.open(fb_auth_url)

    while ACCESS_TOKEN is None:
        httpd.handle_request()

    graph = facebook.GraphAPI(ACCESS_TOKEN)
    graph.put_photo(open("tomato.jpg", "rb"), "이쁘다", 'photos')








