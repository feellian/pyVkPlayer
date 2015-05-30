class ApiErr(Exception):
	pass

class MethodErr(ApiErr):
	def __init__(self, errorCode, errorMsg, requestParams):
		self.errorCode = errorCode
		self.errorMsg = errorMsg
		self.requestParams = requestParams

	def __str__(self):
		return repr(self.errorMsg)

