import SimpleHTTPServer
import SocketServer
import urllib
import json

API_SEARCH_AREA = "/search_area="

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):

    	if API_SEARCH_AREA in self.path: #hack a API endpoint by extending SimpleHTTPServer
    		
    		#Read json data from url
    		area = json.loads(urllib.unquote(self.path[len(API_SEARCH_AREA):]).decode('utf8'))
    		
    		print(area)
    		#print([[area["south"], area["west"]], [area["south"], area["east"]], [area["north"], area["west"]], [area["north"], area["east"]]])

    		self.path = '/area_selector'

        if self.path == '/':
            self.path = '/area_selector'

        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 3000), Handler)

server.serve_forever()