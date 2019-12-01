from .people import People

class Student:
	def __init__(self, name, number, cred, depart, facu, club=None, lab=None):
		People.__init__(name)
		self.number = number
		self.cred = cred
		self.depart = depart
		self.facu = facu
		self.club = club
		self.lab = lab
