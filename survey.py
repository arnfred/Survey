# Main instance of survey

import web
        
urls = (
    '/(.*)', 'survey'
)
app = web.application(urls, globals())

class survey:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
