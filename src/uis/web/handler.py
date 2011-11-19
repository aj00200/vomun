from urllib import unquote_plus
import hashlib
import time

import libs.events
import libs.globals
import libs.friends
import uis.web.content
import libs.encryption.rsa

class Handler(libs.events.Handler):
    '''A demonstration of how event handlers can serve pages on the localhost
    web server. This can be used easily accross the entire project.
    '''
    def __init__(self):
        self.posts = [
            Post('The Devs',
                 '5d931b7da1ebca177dea980c4c6b9676653f567730fa9831e82542ff04273356',
                 'Welcome to Anon+.\nJust a warning, this system is not completely secure at this time. Messages are not encrypted and you will need to refresh this page to see new messages.'
            )
        ]
        
    def got_message(self, packet):
        contents = packet.message.split(',', 2)
        name = contents[0]
        sha256 = contents[1]
        post = contents[2]
        
        self.posts.insert(0, Post(name, sha256, post))
        
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
            libs.threadmanager.close_sockets()
        elif path.startswith('/make_post.cgi?'):
            parameters = unquote_plus(path.split('?')[-1]).split('&')
            for parameter in parameters:
                item = parameter.split('=')
                if item[0] == 'post':
                    post_contents = item[1] + ' (%s)' % time.ctime()
            for friend in libs.globals.global_vars['friends'].values():
                friend.send_message(','.join((
                        libs.globals.global_vars['config']['username'],
                        hashlib.sha256(post_contents).hexdigest(),
                        post_contents)))
            self.posts.insert(0, Post(
                    libs.globals.global_vars['config']['username'],
                    hashlib.sha256(post_contents).hexdigest(),
                    post_contents))
                        
            connection.send_response(301)
            connection.send_header('Location', 'http://localhost:7777/')
            connection.end_headers()
            connection.wfile.write('Redirecting')
        elif path.startswith('/forward.cgi?'):
            parameters = unquote_plus(path.split('?')[-1])
            post_hash = parameters.split('=')[-1]
            
            for post in self.posts:
                print('Post: %s; FWD: %s' % (post.hash, post_hash))
                if post.hash == post_hash:
                    for friend in libs.globals.global_vars['friends'].values():
                        friend.send_message(','.join((
                                post.name,
                                post.sha256,
                                post.body
                        )))
                    self.posts.insert(0, post)
                    break                 
            
            connection.send_response(301)
            connection.send_header('Location', 'http://localhost:7777/')
            connection.end_headers()
            connection.wfile.write('Redirecting')
        elif path.startswith('/reply.cgi?'):
            connection.send_response(301)
            connection.send_header('Location', 'http://localhost:7777/')
            connection.end_headers()
            connections.wfile.write('Redirecting')
        elif path == '/friends.html':
            connection.send_response(200)
            connection.send_header('Content-type', 'text/html')
            connection.end_headers()
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Friend management',
                    pagetitle = 'Friends',
                    main = uis.web.content.friend_page.format(
                            key = libs.encryption.rsa.export_key(
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
                    result = libs.encryption.rsa.import_key(keydata)
                elif item[0] == 'name':
                    name = item[1]
                elif item[0] == 'ip':
                    ip = item[1]
                    
            # Add the friend object
            libs.friends.add_friend(result, ip = ip,
                                    port = 1337, name = name)
                
            # Notify the user of success
            connection.send_response(200)
            connection.send_header('Content-type', 'text/html')
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Friend added',
                    pagetitle = 'Friend added',
                    main = 'Your friend has been added.<br />' +
                        '<br />Key: %s' % result,
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
            if post.type == 'mention':
                content += uis.web.content.mention.format(
                        user = post.name,
                        body = post.body,
                        hash = post.hash
                )
            elif post.type == 'self':
                content += uis.web.content.self_post.format(
                        user = post.name,
                        body = post.body,
                        hash = post.hash
                )
            else: # normal psot
                content += uis.web.content.post.format(
                        user = post.name,
                        body = post.body,
                        hash = post.hash
                )
        return content
    
class Post(object):
    def __init__(self, name, sha256, post):
        self.name = name
        self.sha256 = sha256
        self.hash = sha256[0:10]
        self.body = post
        
        if name == libs.globals.global_vars['config']['username']:
            self.type = 'self'
        elif '@'+libs.globals.global_vars['config']['username'] in self.body:
            self.type = 'mention'
        else:
            self.type = 'normal'
            
        # Sanity checks
        if not self.check_hash():
            self.body = 'This post failed the hash check.'
        self.sanatize()
            
    def check_hash(self):
        '''Check if the provided hash matches the informationw we were given.
        Return True if it does, otherwise False.
        '''
        return hashlib.sha256(self.body).hexdigest()[0:10] == self.hash
            
    def sanatize(self):
        '''Check the post options to make sure they do not contain anything
        that might act as a security risk or compromise an identity.'''
        self.name = self.name.replace('<', '&lt;')
        self.body = self.body.replace('<', '&lt;')
        self.name = self.name.replace('>', '&gt;')
        self.body = self.body.replace('>', '&gt;')
        self.name = self.name.replace('"', '&quot;')
        self.body = self.body.replace('"', '&quot;')
        
        # Features such as auto-linking and line breaks
        self.body = self.body.replace('\n', '<br />')