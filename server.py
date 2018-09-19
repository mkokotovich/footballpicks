from waitress import serve
from footballpicks.wsgi import application


serve(application, unix_socket='/tmp/nginx.socket', url_scheme='https')
