#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
import posixpath
import html
import sys
import io
from http import HTTPStatus
import shutil
from code.node_loop import *
from code.helper import *
import yaml

class ServerCustom(BaseHTTPRequestHandler):
    def do_GET(self):
        yamlnodedir = '/var/lib/puppet/yaml/node'
        outputdir = '/var/lib/puppet-to-rundeck/outdir'
        max_age = 7
        if 'yamlnodedir' in yaml_conf:
               yamlnodedir = yaml_conf['yamlnodedir']
        if 'outputdir' in yaml_conf:
               outputdir = yaml_conf['outputdir']
        if 'maxage' in yaml_conf:
               max_age = yaml_conf['maxage']


        logv('request path: %s' % self.path)
        if not os.path.isdir(outputdir):
            os.mkdir(outputdir)
        os.chdir(outputdir)

        """Serve a GET request."""
        f = self.send_head()
        if f:
            logv('f present OK')
            try:
                node_loop(yamlnodedir,outputdir,max_age,self.path)
                self.copyfile(f, self.wfile)
            finally:
                f.close()
        else:
            logv('f absent PROBLEM')
    
    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        self.send_error(
            HTTPStatus.NOT_IMPLEMENTED,
            "Cannot POST")

    def send_head(self):
        """Common code for GET and HEAD commands.
    
        This sends the response code and MIME headers.
    
        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
    
        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = 'text/yaml'
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

     
    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>'
                    % (urllib.parse.quote(linkname,
                                          errors='surrogatepass'),
                       html.escape(displayname, quote=False)))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path


    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)
    
       
#def runServer(server_class=HTTPServer, handler_class=S, port=8080):
#    httpd = server_class(server_address, handler_class)
def runServer():
    
    config_file = '/etc/puppet-to-rundeck.yaml'
    if os.path.isfile(config_file):
        with open(config_file, 'r') as fconf:
            global yaml_conf
            yaml_conf = yaml.load(fconf)
    else:
        log('%s does not exist' % ( config_file ))
        sys.exit(1)
   
    bind = '127.0.0.1'
    port = 8080
    if yaml_conf['bind']:
        bind = yaml_conf['bind']
    if yaml_conf['port']:
        port = yaml_conf['port']

    server_address = (yaml_conf['bind'], yaml_conf['port'])

    httpd = HTTPServer(server_address, ServerCustom)
    #httpd = HTTPServerCustom(server_address,ServerCustom,yamlnodedir,outputdir)

    print('Starting httpd...')
    httpd.serve_forever()
