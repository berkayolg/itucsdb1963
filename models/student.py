from .people import People

class Student(People):
	def __init__(self, id, number, cred, depart, facu, club=None, lab=None):
		self.id = id
		self.number = number
		self.cred = cred
		self.depart = depart
		self.facu = facu
		self.club = club
		self.lab = lab
