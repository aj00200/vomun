template = '''
<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="global.css" />
    <script type="text/javascript" src="global.js"></script>
  </head>
  <body>
    <div id="header">

      <div id="headblock">
	    <h1>Anon+ The free social network</h1>
      </div>
    </div>
    <div id="nav">
      <a href="/">Home</a> | 
      <a href="friends.html">Friends</a> | 
      <a href="shutdown.html">Shutdown</a>
    </div>
    <div id="content">
      <h2>{pagetitle}</h2>
      {main}
    </div>
    <div id="bottom">
      {sidecontent}
    </div>
  </body>
</html>
'''

friend_page = '''
<h3>Add a friend</h3>
<form action="add_friend.cgi" method="get">
  <p>To add a friend, have them send you their public key and paste the information here:</p>
  <textarea id="key" name="key"></textarea>
  <p>Have your friend give you their IP address.</p>
  <input type="text" id="ip" name="ip" />
  <p>Enter a name so you know who this friend is.</p>
  <input type="text" id="name" name="name" />
  <input type="submit" value="Add This Friend!" />
</form>
<h3>Your public key</h3>
<p>If a friend wants to add you, send them this public key.</p>
<form action="#">
  <textarea rows="5">
{key}
</textarea>
</form>
'''
  

globalcss = '''
html, body {margin: 0px; padding: 0px; text-align: center;}
#header {
    background: black;
    text-align: center;
}
#headblock {
    display: inline-block;
    color: gray;
    width: 80ex;
}
h1 {
    letter-spacing: 3px;
}
h1:hover {
    color: rgb(200,200,200);
}

/* Layout */
#nav {
    position: absolute;
    top: 2px; right: 2px;
    background: rgb(25,25,25);
    border-radius: 5px;
    padding: 2px;
    color: white;
}
#content {
    margin-top: 3px;
    display: inline-block;
    text-align: left;
    width: 80ex;
}

/* Posts */
.post {
    clear: both;
    margin: 5px;
    display: block;
    min-height: 3em;
    border-radius: 10px;
    border-right: 1px solid gray;
    border-left: 10px solid #cef5ad;
    padding: 10px 5px 10px 5px;
}
.mention {
    border-left: 10px solid #f5adc3;
}
.self {
    border-left: 10px solid rgb(86,145,254);
}
.hash {
    color: gray;
    font-family: monospace;
    float: right;
    clear: right;
}
.user {
    font-weight: bold;
}
.tag {
    color: rgb(50,50,50);
    font-style: italic;
    text-decoration: none;
}
.tag:hover {
    text-decoration: underline;
}
.postcontrols {
    float: right;
    padding-left: 2px;
    margin-left: 3px;
    border-left: 1px solid black;
}
textarea {
    display: block;
    width: 100%;
}
input[type="submit"] {
    float: right;
}
/* Styles */
#nav a {
    color: orange;
}
'''

post_controls = '''
<div class="postcontrols"><a href="reply.cgi?{hash}"><img src="data:img/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA+0lEQVR42mNkoBAwUteAVxoOQNIBrw6xGw24DXioBpKsZ/gPlfmPpArEZmF0ZJC5eQC3ARdVGhj+/69H0QzjsDE5MmjdRtGMacBeBYgLsIFf/x0ZPB8SMGCZDG4DQCp/MTgyxD/B44U+CdwGgMC//wcYSl464jagRLiBgZERYgAbYyPDn//2DP+QYwUYFj+Brpj09gB2A2L4gYEIdAE7MLTnfYAoShJ0YPj5fz88VBmBBi/50IDdAGfuBqDmAwzbvqAGliePAzAQ90N5jQx7v+IwAB/QYYeEz5WfKHqIN0CcZT/QdY0Mj34fIM8AXiYHhs//DqALUzkzkQEAX29NEd152/AAAAAASUVORK5CYII=" /></a></br />
        <a href="forward.cgi?{hash}"><img src="data:img/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABq0lEQVR42qWSv0sCYRjH3/curwPDQrAIEkPSMVqimryXJhEaaihaDGptbNY/oL2lhhyChnIKl4IXqq2gqUJEMSQ0EIyKEzvv6b33zvO3Db5w3L3Pj8/zfe55MBry4MZHcLeqpE9k2hkQ3Ksp6WOJ/guYi5YBgU4yCU9bcGDnMw4AoczpBBkI8G9lgd/0OsmeB2yIf/stzl4xhIBmz3ykL8C3/gC2CTSSTy5xyOzGU5w5YpjZmUSav1ggPQEz4RRTgC2TAfklhVSEeiPXDIBj3GVAAGjhapV0AaZJAvgVoyZE1wgSJcVsgWloFGCQ95tN0gbwLB/yFnCrCl5Rp1gQFRPe6tPpx/0+sQHu+QOwg1pUsGTKptMNwCItP8aaAFcgCobfGAW2grEgEQDNbsFsA/HkyvNRewtOb9icglVFECXylUvSMd+aNUbDLBgP/c5ddv9E2bNoA4zKavGOj1GeWuEAbMlWi7e9x+hw+YEHCQ5Sq7zaiySNB809YMm1ykv/RRJG3SCwZE0tta2yKE/GmapQXS0NXmUsygrUq7QzQBhxKrr2Q1Gfg9GQ5w9UupgRdo4gjgAAAABJRU5ErkJggg==" /></a></div>

'''
post = '''
      <div class="post">
	<div class="postcontent">
%s
	  <span class="user">{user}</span> - {body}
	  <div class="hash">{hash}</div>

	</div>
      </div>
''' % post_controls
mention = '''
      <div class="post mention">
	<div class="postcontent">
%s
	  <span class="user">{user}</span> - {body}
	  <div class="hash">{hash}</div>

	</div>
      </div>
''' % post_controls

self_post = '''
      <div class="post self">
	<div class="postcontent">
%s
	  <span class="user">{user}</span> - {body}
	  <div class="hash">{hash}</div>

	</div>
      </div>
''' % post_controls

friends_box = '''
<h3>Friends</h3>
{friends}
'''

key_form = '''
<form action="keys.html" method="POST">
  <input type="submit" value="Generate 2048-bit key" />
</form>
'''

post_box = '''
<form action="/make_post.cgi" method="get">
  <textarea id="post" name="post"></textarea>
  <input type="submit" value="Send" />
</form>
'''