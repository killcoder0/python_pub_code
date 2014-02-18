import session


browser = session.Session()
async_browser = session.AsyncSession()

def handle_response(response):
    print async_browser.report()


if __name__ == "__main__":
    for url in ("http://mail.163.com/","http://dev.anzhi.com/","http://www.taobao.com/","http://music.baidu.com","http://mail.sogou.com/"):
        print "Sync GET: ",url
        browser.fetch(url,"GET",{},None)
    browser.report()


    print "login sogou mail :"
    action = "https://account.sogou.com/web/login"
    data = {"username":"game_works_002","password":"abc123","client_id":"1014","xd":"http://mail.sogou.com/jump.htm"}
    resp = browser.send_form(action,"POST",data)
    print resp.body
    browser.report()

    url = "http://mail.sogou.com/bapp/7/main"
    resp = browser.fetch(url,"GET",{},None)
    print resp.body
    print "fetch game_works_002:"
    print resp.body.find("game_works_002")!=-1
    browser.report()
