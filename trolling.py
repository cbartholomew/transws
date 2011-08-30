#!/usr/bin/python2.4

import web 
import simplejson as json
import urllib2
import transauthority as transauth
import transpost

urls = (
      "/tw.+", "twiwp",
      "/wp.+","wpinteract" 
      )

class twiwp:
    def GET(self):

        #Accepts two parameters:
        #transAuth=mbta
        #sinceID
        
        queryParams = web.input()
        sinceLen = len(queryParams.sinceID)
        
        if sinceLen > 0:
            url="http://search.twitter.com/search.json?q=" + queryParams.transAuth + "&since_id=" + queryParams.sinceID
        else:
            url="http://search.twitter.com/search.json?q=" + queryParams.transAuth + "&rpp=100"  

        #build jSON    
        req = urllib2.Request(url)
        opener = urllib2.build_opener()
        f = opener.open(req)

        #decode json results
        results = json.load(f)

        ds = results['results']
        twiwpsList = list()
        twiwpsDict = {'results': 'values'}

        for result in ds:
            
            transitTwiwp = twiwp()
            transitTwiwp.id = result['id']
            transitTwiwp.id_str = result['id_str']
            transitTwiwp.text = result['text']
            transitTwiwp.from_user = result['from_user']
            transitTwiwp.from_user_id = result['from_user_id']
            transitTwiwp.created_at = result['created_at']
	    transitTwiwp.profile_image_url = result['profile_image_url']

            if not result['from_user'] == 'mbta_alerts': 
                entry = transitTwiwp.__dict__
                twiwpsList.append(entry)
                entry = ""
                twiwpsDict["results"] = twiwpsList

        objJson = json.JSONEncoder().encode(twiwpsDict)
        
	web.header('Content-Type', 'application/json')
        return objJson

class wpinteract:
		
	def GET(self):
	    	#obtain query parameters. based on the action argument, it will figure out how to handle params. 
		queryParams = web.input()
	    
	    	#parameter dictionary, based on action - will process following function 
		paramOptions = {0 : self.states,
				1 : self.authorities, 
				2 : self.comments}
 	    
	    	#this is the webaction parameter. Comes in on "?action="
		webAction = int(queryParams.action)
		webParams = None
	    	
		#oh boy, need to find a better way to handle this - argument handler	
		if webAction == 0:
			#state takes zero parameters
			webParams = None
		
		if webAction == 1:
			#authorities takes zero parameters	
			webParams = None

		if webAction == 2:
			#comments we expect "postID" in the &id= argument
		 	webParams = int(queryParams.id)			
		
		#return the result of the function we handled above.
		return paramOptions[webAction](webParams)
		
	
	def authorities(self, noparams):
		
		jsonData = transauth.authority().getAuthorities()
		web.header('Content-Type', 'application/json')
		return jsonData
	
	def states(self, noparams):
		jsonData = transauth.authority().getStates()
		web.header('Content-Type', 'application/json')
		return jsonData	
	
	def comments(self, id):				
		
		jsonData = transpost.comments().getCommentsByPostId(id)
		web.header('Content-Type','application/json')
		return jsonData

	               
if __name__ == "__main__":
    web.application(urls, globals()).run()
