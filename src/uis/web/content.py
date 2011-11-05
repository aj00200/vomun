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
      <a href="index.htm">Home</a> | 
      <a href="settings.htm">Settings</a> | 
      <a href="profile.htm">Profile</a>

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
    margin: 5px;
    padding: 3px;
    display: block;
    min-height: 3em;
    border-radius: 10px;
    background-color: white;
    background: #cef5ad;
    box-shadow: 1px 1px 3px;
}
.mention {
    background: #f5adc3;
}
.hash {
    color: gray;
    font-family: monospace;
    float: right;
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
    float: left;
    padding-right: 2px;
    margin-right: 3px;
    border-right: 1px solid black;
}
textarea {
    width: 80ex;
}
/* Styles */
#nav a {
    color: orange;
}
'''

post = '''
      <div class="post">
	<div class="postcontent">
	  <div class="postcontrols">R</br />F</div>
	  <span class="user">{user}</span> - {body}
	  <div class="hash">{hash}</div>

	</div>
      </div>
'''
mention = '''
      <div class="post mention">
	<div class="postcontent">
	  <div class="postcontrols">R</br />F</div>
	  <span class="user">{user}</span> - {body}
	  <div class="hash">{hash}</div>

	</div>
      </div>
'''

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
<form action="/post.htm" method="get">
  <textarea id="post" name="post"></textarea>
</form>
'''