#!/usr/bin/env python

import sys, time, json
import BaseHTTPServer
HOST_NAME='localhost'
PORT_NUMBER=9000
import rethinkdb as r
con = r.connect('localhost', 28015)

try:
    r.db_create('statistics')
except r.RqlRuntimeError:
    pass


con.use('statistics')

try:
    r.table_create('stats')
except r.RqlRuntimeError:
    pass

class CollectorHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # def do_GET(s):
    #     s.send_response(200)
    #     s.send_header("Content-Type", "text/html")

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = json.loads(self.data_string)
        print r.table('stats').insert(data).run(con)
        return

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), CollectorHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
