import Utilities

class User(object):

	def __init__(self,name="",age=-1,gender="",conditions=None):
		self.name = name
		self.age = age
		self.gender = gender
		self.conditions = conditions

	def saveUserInfo(self):
		result = self.name + "\n\n"
		result += str(self.age) + "\n\n"
		result += self.gender + "\n\n"
		# all variables split by double linebreak
		for condition in self.conditions:
			# conditions all on same line, split by double comma
			result += condition + ",,"
		result += "\n\n"
		result += "**END USER INFO**"
		Utilities.writeFile("%s.txt"%self.name,result)

	@staticmethod
	def loadUserInfo(filepath):
		fullInfo = Utilities.readFile(filepath)
		lines = fullInfo.split("\n\n")
		name = lines[0]
		age = int(lines[1])
		gender = lines[2]
		conditions = lines[3].split(",,")[:-1]
		newUser = User(name,age,gender,conditions)
		return newUser

	def toString(self):
		result = "NAME: " + self.name + "\n"
		result += "AGE: " + str(self.age) + "\n"
		result += "GENDER: " + self.gender + "\n"
		result += "CONDITIONS: "
		for condition in self.conditions:
			result += condition + ", "
		return result