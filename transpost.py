import transhelper as trans
import simplejson as json

class comments(object):
	def getCommentsByPostId(self, id):
		id = int(id)            

                objClient = trans.db()
                commentResults  = objClient.getComments(id)
                objClient.closeConn()
		
                commentsList = list()
                commentsDict = {'results': 'values'}             
		
                for comment in commentResults:
                       twiwpComment = comments()
                       twiwpComment.from_user = comment[2]
                       twiwpComment.text = comment[8]
                       entry = twiwpComment.__dict__

                       commentsList.append(entry)
                       entry = ""

                commentsDict["results"] = commentsList
                commentsJson = json.JSONEncoder().encode(commentsDict)        

                return commentsJson
                







