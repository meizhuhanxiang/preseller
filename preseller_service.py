#!/usr/bin/python
# coding: utf-8
import os
import sys
import glob
import handler

import tornado.web
import tornado.ioloop
import tornado.httpserver
import utils.config
import utils.logger
from optparse import OptionParser
from utils import session

reload(sys)
sys.setdefaultencoding('utf-8')


class HandlersApplication(tornado.web.Application):
    def __init__(self, api_entry, **settings):
        self.logger = utils.logger.api_logger()
        handlers = self.load_handlers(api_entry)
        super(HandlersApplication, self).__init__(handlers, **settings)
        self.session_manager = session.SessionManager(settings["session_secret"], settings["store_options"],
                                                      settings["session_timeout"])
    def load_handlers(self, m):
        handlers = []
        if hasattr(m, "__all__"):
            for sub_module in m.__all__:
                for handler_file in glob.glob('%s/%s/*_handler.*' % (m.__name__, sub_module)):
                    handler_name, ext = os.path.splitext(os.path.basename(handler_file))
                    handler_split = handler_name.split("_")
                    module = "%s.%s.%s" % (m.__name__, sub_module, handler_name)
                    attr = "%sHandler" % handler_split[0].capitalize()
                    __import__(module)
                    handlers.append((r"/api/%s/%s" % (sub_module, handler_split[0]), "%s.%s" % (module, attr)))
                    sys.stderr.write("routing uri %s to handler %s\n" % (
                        "/%s/%s" % (sub_module, handler_split[0]), "%s.%s" % (module, attr)))
        return handlers

    def log_request(self, handler):
        if handler.get_status() == 0:
            self.logger.info(handler.get_log_info())
        else:
            self.logger.error(handler.get_log_info())


def main():
    parser = OptionParser(usage="usage:%prog [options] filepath")
    parser.add_option("-p", "--port",
                      action="store", type="string", default="", dest="port")
    (options, args) = parser.parse_args()
    port = options.port
    if not port:
        port = utils.config.get("global", "port")
    debug_mode = int(utils.config.get('global', 'debug'))

    sys.stderr.write("listen server on port %s ...\n" % port)
    settings = dict(
        debug=True if debug_mode else False,
        cookie_secret="e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
        session_secret="3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
        session_timeout=600,
        store_options={
            'redis_host': '127.0.0.1',
            'redis_port': 6379,
            'redis_pass': '',
        }
    )
    application = HandlersApplication(handler, **settings)
    server = tornado.httpserver.HTTPServer(application)
    server.bind(port)
    server.start(1 if debug_mode else 15)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    #from model.config import Configure
    main()
