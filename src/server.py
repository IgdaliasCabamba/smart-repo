from twisted.web.static import File
from klein import run, route

@route('/static/', branch=True)
def static(request):
    return File("./static")

@route('/')
def home(request):
    return 'Working on'

run("localhost", 8080)