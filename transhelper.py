#!/usr/bin/python2.4

import MySQLdb
import datetime
import wordpresslib
import re

class db(object):
     def __init__(self):
          
          self.host = "tra1121709060314.db.4173543.hostedresource.com"
          self.user = "tra1121709060314"
          self.passwd = "Transporf41l"
          self.db = "tra1121709060314"
          

          conn = MySQLdb.connect(self.host,
                                 self.user,
                                 self.passwd,
                                 self.db)

          self.connection = conn
          self.xmlrpcurl  = 'http://transporfail.com/transwp/xmlrpc.php'
          
#Method
     def closeConn(self):
          try:
               self.connection.close() 
               return 1
          except:
               raise

#select requests          
     def getPost(self, postID):
          c = self.connection.cursor()
          c.execute("select * from wp_posts where id = %i" % (int(postID)))
          row = c.fetchone()
          c.close

          return row

     def getComments(self, postID):
          c = self.connection.cursor()
          c.execute("select * from wp_comments where comment_post_ID =%i" % (int(postID)))
          rows = c.fetchall()
          c.close

          return rows

     def getCommentCount(self, postID):
          c = self.connection.cursor()
          c.execute("select comment_count from wp_posts where id =%i" % (int(postID)))
          row = c.fetchone()
          c.close
          self.comment_count = row[0]

          return self.comment_count

     def checkTweetID(self, tweetID):
          self.tweetID = int(tweetID)
          c = self.connection.cursor()

          c.execute("select id from wp_posts where tweet_id = %i" % (self.tweetID))
          row = c.fetchone()

          if c.rowcount > 0:
               self.postID = int(row[0])
          else:
               self.postID = 0

          c.close()
          
          return self.postID

     def getTransAuthoritiesByState(self, stateID):
          self.stateID = (int(stateID))
          c = self.connection.cursor()
          c.execute("select authority_tag from trans_authority where state_id = %i" % (self.stateID))
          tags = c.fetchall()
          c.close()

          return tags
		     
     def getAllStatesAndAuthorities(self):
	  c = self.connection.cursor()
          c.execute("select * from getAllStateAndAuthorities")
	  
          authorities = c.fetchall()
	  c.close()

	  return authorities 

     def getAllStates(self):
	 c = self.connection.cursor()
	 c.execute("select * from trans_state")
	 
	 states = c.fetchall()
	 c.close()
	 
	 return states
		

#insert requests
     def insertComment(self, postID, commentAuthor, commentContent, commentLoginID=2):
          #scrub the text
          commentContent = re.escape(commentContent)

          self.postID  = int(postID)
          self.author  = "'" + commentAuthor + "'"
          self.content = "'" + commentContent + "'"
          self.LoginID = int(commentLoginID)
          dttm = datetime.datetime.now().isoformat()
          dttm  = "'" + dttm + "'"

          c = self.connection.cursor()

          try:
               c.execute("insert into wp_comments (comment_post_ID, comment_author, comment_content, comment_date, comment_date_gmt, user_id) values (%i, %s, %s, %s, %s, %i)" % (self.postID,
                                                                                                                                                                                  self.author,
                                                                                                                                                                                  self.content,
                                                                                                                                                                                  dttm,
                                                                                                                                                                                  dttm,
                                                                                                                                                                                  self.LoginID))  
               if c.rowcount > 0:
                    totalCount = self.getCommentCount(postID)
                    totalCount = totalCount + 1
                    rID = self.updateCommentCount(postID, totalCount)
                    c.close()
                    if rID == 1:
                         totalCount = self.getCommentCount(postID)

                         return totalCount
                    else:
                         return 0
               else:
                    return 0 
          except:
               raise

#update requests
     def updateCommentCount(self, postID, tCount):
          self.postID = int(postID)
          self.tCount = int(tCount)

          c = self.connection.cursor()
          try:
               c.execute("update wp_posts set comment_count = %i where id = %i" % (self.tCount, self.postID))
               return 1
          except:
               raise

     def updateTweetID(self, postID, twiwpId):
          self.postID = int(postID)
          self.twiwpId = int(twiwpId)
          c = self.connection.cursor()
          try:
               c.execute("update wp_posts set tweet_id = %i where id = %i" % (self.twiwpId, self.postID))
               return 1
          except:
               raise
          
          
          
#Uses wordpresslib to create a new posting
     def newSinglePost(self, id, text, from_user, from_user_id):
          #scrub the text
          text = re.escape(text)
          
          self.twiwpId         = int(id)
          self.twiwpText       = text
          self.twiwpFromUser   = from_user
          self.twiwpFromUserId = int(from_user_id)

          url = self.xmlrpcurl
          #initalize posting using general posting login
          wp = wordpresslib.WordPressClient(url, 'transpost', 'Transp0st')
          #main blog
          wp.selectBlog(0)

          #initilize posting
          post = wordpresslib.WordPressPost()

          post.title = ""
          post.description = self.twiwpFromUser + " said, '" + self.twiwpText + "'"
          self.postID = wp.newPost(post, True)

          upRowCount = self.updateTweetID(self.postID,self.twiwpId)

          if upRowCount > 0:
               return self.postID
          else:
               return -9999
          


                                                                                    
