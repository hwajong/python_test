# -*- coding: utf-8 -*-

# 1. 페이스북(FB) 계정에 앱 등록
# - FB -> 설정 -> 개발자 -> Apps -> Create a New App
# - Display Name : uphoto
# - 카테고리 -> 유틸리티
# --> Create
#
# - Apps -> uphoto -> Settings -> Add Platform -> Website -> Site URL -> http://192.168.80.27:8000 -> Save Change
# - App ID 확인     : Apps -> uphoto
# - App Secret 확인 : Apps -> uphoto
#
# 2. App 접근 허가 설정
# - FB -> 설정 -> 개발자 -> Tools -> Graph API Explorer
# - Application : uphoto
# - get Access Token -> Extended Permission -> publish actions -> Get Access Token -> 확인 -> 확인
#
# 3. 파이선 라이브러리 모듈 설치
# - mechanize 설치 : http://wwwsearch.sourceforge.net/mechanize/
# - facebook sdk 설치 : https://github.com/pythonforfacebook/facebook-sdk
#
# 4. 필요한 정보 수정
# - APP_ID
# - APP_SECRET
# - FB_ID
# - FB_PASS

from urllib2 import URLError

import mechanize
import facebook
import logging

APP_ID = '658559290891111'
APP_SECRET = 'fa9f127e318b32062222054d533d5085'
FB_ID = 'xxxx@gmail.com'
FB_PASS = 'xxxxxxxxx'
REDIRECT_URI = 'http://192.168.80.27:8000/'


# 페이스북으로부터 ACCESS TOKEN 을 얻는다.
#
# 페이스북에 ACCESS TOKEN 을 요청하면 페이스북은 사용자 계정 인증후 요청시 전달한 REDIRECT URL로 ACCESS TOKEN 을 전달해 준다.
# 본 프로그램의 경우 REDIRECT URL 에 해당하는 서버를 뛰어 놓지 않고 mechanize 브라우저의 내부동작을 트레이싱해
# REDIRECT URL 로 전달되는 ACCESS TOKEN 을 켑처하는 방식으로 ACCESS TOKEN 을 얻는다.
def get_access_token():

    # Set logger
    # mechanize 브라우저의 내부동작을 트레이싱하기 위한 로그 설정
    # mechanize 의 내부동작이 br.log 파일에 기록된다.
    logger = logging.getLogger("mechanize")
    logger.addHandler(logging.StreamHandler(open('br.log', 'wb')))
    logger.setLevel(logging.DEBUG)

    br = mechanize.Browser()
    br.set_handle_robots(False)

    # 페이스북 인증요청 API url 설정
    fb_auth_url_prefix = 'https://www.facebook.com/dialog/oauth?scope=publish_actions&response_type=token'
    fb_auth_url = '%s&redirect_uri=%s&client_id=%s&client_secret=%s' % (fb_auth_url_prefix, REDIRECT_URI, APP_ID, APP_SECRET)
    print '>> fb_auth_url : ' + fb_auth_url

    # mechanize 브라우저로 페이스북 인증요청
    br.open(fb_auth_url)

    # for f in br.forms():
    #      print f

    # 페이스북 사용자 계정인증 (email/pass)
    br.form = list(br.forms())[0]
    control = br.form.find_control("email")
    control.value = FB_ID
    control = br.form.find_control("pass")
    control.value = FB_PASS

    try:
        print '>> now submit !!!'
        br.submit()
    except URLError:
        # mechanize 브라우저는 REDIRECT URL 로 접속 하려고 하지만 해당 서버는 없으므로 항상 URLError 가 발생한다 --> 무시.
        pass

    # br.log 를 열어 기록된 ACCESS TOKEN 을 얻어온다.
    f = open('br.log', 'r')
    lines = f.readlines()
    f.close()

    token = None

    # ACCESS TOKEN 파싱
    for line in lines:
        pos = line.find("access_token")
        if pos > 0:
            xx = line.split("access_token=")
            #print xx[1]
            yy = xx[1].split("&")
            #print yy[0]
            token = yy[0]

    print '>> ACCESS_TOKEN : ' + str(token)
    return token


if __name__ == '__main__':

    access_token = get_access_token()

    if access_token is None:
        print ">> Error - can't get ACCESS_TOKEN"
        exit(-1)

    # upload photo
    # GraphAPI 를 이용하여 페이스북으로 사진을 업로드한다.
    graph = facebook.GraphAPI(access_token)
    graph.put_photo(open('tomato.jpg', 'rb'), 'test', 'photos')









