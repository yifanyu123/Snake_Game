class User:
	def _init_(self,username="example",snake=Snake()):
		self.name=username
		self.snakelength=snake.length
	def StoreUserData(self,filename)
		DataFile=open(filename,'w')
		DataFile.write(self.name+" "+self.snakelength+'\n')
