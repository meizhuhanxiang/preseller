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

reload(sys)
sys.setdefaultencoding('utf-8')


class OpenDSApplication(tornado.web.Application):
    def __init__(self, api_entry, **settings):
        self.logger = utils.logger.api_logger()
        handlers = self.load_handlers(api_entry)
        super(OpenDSApplication, self).__init__(handlers, **settings)

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
    application = OpenDSApplication(handler, **{
        'debug': True if debug_mode else False,
    })
    server = tornado.httpserver.HTTPServer(application)
    server.bind(port)
    server.start(1 if debug_mode else 15)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    from model.config import Configure
    main()
