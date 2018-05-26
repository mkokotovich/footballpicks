from waitress import serve
from footballpicks.wsgi import application
#serve(application, listen='0.0.0.0:5000', url_scheme='https')
serve(application, unix_socket='/tmp/nginx.socket', url_scheme='https')

