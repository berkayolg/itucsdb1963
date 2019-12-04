from .people import People

class Student(People):
	def __init__(self, name, number, cred, depart, facu, club=None, lab=None):
		self.name = name
		self.number = number
		self.cred = cred
		self.depart = depart
		self.facu = facu
		self.club = club
		self.lab = lab
