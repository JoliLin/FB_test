import requests 
import json
import urllib
import urllib2
import subprocess
import urlparse
import facebook
import sys 

FB_ID = ''
FB_secret = ''

def crawl( url ) :
	return json.load(urllib2.urlopen(url) )

def writeFile( name, content ) :
	f = open( name, 'w' )
	f.write( content )
	f.close()

def init() :
	oauth_args = dict(client_id=FB_ID, client_secret=FB_secret, grant_type='client_credentials')
	oauth_curl_cmd = ['curl', 'https://graph.facebook.com/oauth/access_token?'+urllib.urlencode(oauth_args)]
	oauth_response = subprocess.Popen(oauth_curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

	try :
		oauth_access_token = urlparse.parse_qs( str(oauth_response) )['access_token'][0]
	except KeyError :
		print( 'Unable to grab an access token' )
		exit()
	
	return oauth_access_token


reload(sys)
sys.setdefaultencoding('utf-8')
access_token = init()

g = facebook.GraphAPI(access_token)

#pp(g.get_object( '/lslandnationyouth/'+ 'posts')) 

#print 'ME'
#pp(g.get_object('me'))
#print 'Groups'
#pp(g.get_connections('me', 'groups'))
#pp(g.get_connections( '152361831510746', 'feed'))
post = (g.get_connections( 'lslandnationyouth', 'posts'))
print post.keys()
print post['data'][0].keys()
time = post['data'][24]['created_time'].split('T')[0]
curPage = post
print time

while int(time.split('-')[0]) == 2014 :
	writeFile ( time, json.dumps(curPage, ensure_ascii=False, indent=1) ) 
	nextPage = crawl( curPage['paging']['next'] )
	print curPage['paging']['next']	
	time = nextPage['data'][24]['created_time'].split('T')[0]
	print time
	curPage = nextPage
	print 		
