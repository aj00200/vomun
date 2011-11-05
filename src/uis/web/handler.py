import libs.events
import libs.globals
import uis.web.content
import libs.encryption.gpg

class Handler(libs.events.Handler):
    '''A demonstration of how event handlers can serve pages on the localhost
    web server. This can be used easily accross the entire project.
    '''
    def web_ui_request(self, path, connection):
        print('R: %s' % path)
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
            parameters = path.split('?')[-1].split('&')
            for parameter in parameters:
                item = parameter.split('=')
                if item[0] == 'key':
                    result = libs.encryption.gpg.import_key(item[1])
                
            connection.send_response(200)
            connection.send_header('Content-type', 'text/html')
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Friend added',
                    pagetitle = 'Friend added',
                    main = 'Your friend has been added.<br />%s' % parameters,
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
        content += uis.web.content.post.format(
                user = 'aj00200',
                body = 'Yeah, we are almost ready!',
                hash = 'lskjdf'
        )
        content += uis.web.content.mention.format(
                user = 'Anonymous1234',
                body = '<a class="tag" href="#!/u/aj00200">@aj00200</a> Ready for the Nov 5th beta?',
                hash = 'lzu89k'
        )
        return content