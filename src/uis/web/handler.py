from urllib import unquote_plus

import libs.events
import libs.globals
import libs.friends
import uis.web.content
import libs.encryption.gpg

class Handler(libs.events.Handler):
    '''A demonstration of how event handlers can serve pages on the localhost
    web server. This can be used easily accross the entire project.
    '''
    def __init__(self):
        self.posts = [
            Post('aj00200', 'shuffilinhashinsmashin', 'Post contents')
        ]
        
    def got_message(self, packet):
        contents = packet.message.split(',')
        name = contents[0]
        sha256 = contents[1]
        post = contents[2]
        
        self.posts.append(Post(name, sha256, post))
        
    def web_ui_request(self, path, connection):
        if path == '/':
            connection.send_response(200)
            connection.send_header('Content-type',	'text/html')
            connection.end_headers()
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Anon+ News Feed',
                    pagetitle = 'Anon+ News Feed',
                    main = uis.web.content.post_box + self.__generate_news_feed(),
                    sidecontent = self.__friends2html()
            ))
        elif path == '/global.css':
            connection.send_response(200)
            connection.send_header('Content-type',	'text/css')
            connection.end_headers()
            connection.wfile.write(uis.web.content.globalcss)
        elif path == '/settings.html':
            connection.send_response(200)
            connection.send_header('Content-type',	'text/html')
            connection.end_headers()
            connection.wfile.write('Connections page')
        elif path == '/shutdown.html':
            connection.send_response(200)
            connection.send_header('Content-type',	'text/html')
            connection.end_headers()
            print('Got shutdown request from web server')
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Shutting down',
                    pagetitle = 'Shutdown',
                    main = 'We are quitting now. Threads are being killed.',
                    sidecontent = 'Goodbye :)'
            ))
            libs.globals.global_vars['running'] = False
            libs.threadmanager.killall()
        elif path == '/friends.html':
            connection.send_response(200)
            connection.send_header('Content-type', 'text/html')
            connection.end_headers()
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Friend management',
                    pagetitle = 'Friends',
                    main = uis.web.content.friend_page.format(
                            key = libs.encryption.gpg.export_key(
                                libs.globals.global_vars['config']['nodekey']
                            )
                        ),
                    sidecontent = self.__friends2html()
            ))
        elif path.startswith('/add_friend.cgi?'):
            parameters = unquote_plus(path.split('?')[-1]).split('&')
            keydata = ''
            name = ''
            ip = ''
            
            # Parse parameters
            for parameter in parameters:
                item = parameter.split('=')
                if item[0] == 'key':
                    keydata = item[1].replace('\\r', '').replace('\\n', '\n')
                    result = libs.encryption.gpg.import_key(keydata)
                elif item[0] == 'name':
                    name = item[1]
                elif item[0] == 'ip':
                    ip = item[1]
                    
            # Add the friend object
            libs.friends.add_friend(result.fingerprints[0], ip = ip,
                                    port = 1337, name = name)
                
            # Notify the user of success
            connection.send_response(200)
            connection.send_header('Content-type', 'text/html')
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Friend added',
                    pagetitle = 'Friend added',
                    main = 'Your friend has been added.<br />' +
                        '<br />Key: %s' % result.fingerprints[0],
                    sidecontent = self.__friends2html()
            ))
        elif path == '/keys.html':
            connection.send_response(200)
            connection.send_header('Content-type', 'text/html')
            connection.end_headers()
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Key management',
                    pagetitle = 'Key management',
                    main = uis.web.content.key_form,
                    sidecontent = self.__friends2html()
            ))
            
    def __friends2html(self):
        '''Convert our friends list into some nice HTML'''
        return uis.web.content.friends_box.format(
                friends = 'Our friend detector tells me you have no friends!'
        )
        
    def __generate_news_feed(self):
        '''Return the post elements in HTML'''
        content = ''
        for post in self.posts:
            content += uis.web.content.post.format(
                    user = post.name,
                    body = post.body,
                    hash = post.hash
            )
        return content
    
class Post(object):
    def __init__(self, name, sha256, post):
        self.name = name
        self.hash = sha256[0:10]
        self.body = post
        