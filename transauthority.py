import transhelper as trans
import simplejson as json

class authority(object):
	def getAuthorities(self):
                objClient = trans.db()
		authorities = objClient.getAllStatesAndAuthorities()
                                             
		objClient.closeConn()
		
	       	authorityList  = list()
                authorityDict  = {'authorities' : 'values'}
	
                for authrow in authorities:
                        objAuthority = authority()
                        objAuthority.authid     = authrow[0]
                        objAuthority.authdesc   = authrow[1]
                        objAuthority.authtag    = authrow[2]
                        objAuthority.stateid    = authrow[3]
                        objAuthority.stateabbrv = authrow[4]

			entry = objAuthority.__dict__
			
			authorityList.append(entry)
                        entry = ""

                authorityDict["authorities"] = authorityList
                authorityJson = json.JSONEncoder().encode(authorityDict)

                return authorityJson

	def getStates(self):
		objClient = trans.db()
		states = objClient.getAllStates()
		
		objClient.closeConn()
		
		stateList  = list()
                stateDict  = {'states' : 'values'}

                for staterow in states:
                        objState = authority()
                        objState.stateid      = staterow[0]
                        objState.stateabbrv   = staterow[1]

                        entry = objState.__dict__

                        stateList.append(entry)
                        entry = ""

                stateDict["states"] = stateList
                stateJson = json.JSONEncoder().encode(stateDict)

                return stateJson


