import session
import tornado.ioloop


browser = session.Session()
async_browser = session.AsyncSession()

def handle_response(response):
    print async_browser.report()


if __name__ == "__main__":
    print "login sogou mail :"
    action = "https://account.sogou.com/web/login"
    data = {"username":"game_works_002","password":"abc123","client_id":"1014","xd":"http://mail.sogou.com/jump.htm"}
    async_browser.send_form(action,"POST",data,handle_response)
    tornado.ioloop.IOLoop.instance().start()

