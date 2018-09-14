import os

from apistar import App, Route
from apistar.server.wsgi import WSGIEnviron


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to Michae'}
    return {'message': 'Welcome to Michael Home, {}'.format(name)}


def get_ip(environ: WSGIEnviron):
    return {"ip_addr": environ["REMOTE_ADDR"]}


routes = [
    Route('/', method='Get', handler=welcome),
    Route('/ip', method='Get', handler=get_ip)
]

app = App(routes=routes)
if __name__ == '__main__':
    app.serve('0.0.0.0', 5000, debug=True)
