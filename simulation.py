# Konstanten
# Zeitwerte in Stunden (Tage * 24 rechnen)
PRAEVALENZ = 0.005  # 1% Der Bevölkerung Infiziert. 

# Zeitraum zwischen dem Tag, an die Person dem Virus ausgesetzt war (Exposition) und sich angesteckt hat bis zum Zeitpunkt, an dem der Angesteckte infektiös wird
LATENZZEIT = 2.5 * 24 # https://www.sciencemediacenter.de/alle-angebote/fact-sheet/details/news/verlauf-von-covid-19-und-kritische-abschnitte-der-infektion/

# https://www.sciencemediacenter.de/alle-angebote/fact-sheet/details/news/verlauf-von-covid-19-und-kritische-abschnitte-der-infektion/
# Umfasst den Zeitraum vom Tag der Ansteckung bis zu dem, an dem sich erste Symptome zeigen
INKUBATIONSZEIT_MIN = 4 * 24
#INKUBATIONSZEIT_MAX = 14

# https://www.sciencemediacenter.de/alle-angebote/fact-sheet/details/news/verlauf-von-covid-19-und-kritische-abschnitte-der-infektion/
# Zeitspanne der Infektiosität Umfasst den Zeitraum, in dem ein Infizierter ansteckend ist
#circa 2,5 Tagen vor Symptombeginn
INFEKTIOESITAET = INKUBATIONSZEIT_MIN - (2.5*24)
# WorstCase...


ANTIGEN_FAKE = 0.20 # 20% Faken ihre Selbsttests und nutzen ein kopiertes Bild
ANTIGEN_SPECIFICITY = 0.6 # 60% Specificity TODO: Geraten!!!

PCR_SPECIFICITY = 0.99 # TODO (93% Spezifität checken!!!)
from random import randint
class Human():
	def __init__(self,hour):
		#Würfeln ob Person Infiziert ist
		if(randint(1, 10000)<(PRAEVALENZ*10000)):
			#Wenn Infiziert Status setzen und Infektionsdatum in den vergangenen 14 Tagen würfeln
			self.infected = True
			#Infektionsdatum zwischen jetzt und - 14 Tage
			self.infected_date = randint(-14*24, 0)+hour
			self.virulent = False
		else:
			self.infected = False
			self.virulent = False
		# Go one Hour to the future
	def run(self,hour):
		if(self.infected == True):
			if((self.infected_date + INFEKTIOESITAET) < hour):
				self.virulent = True
	# Simulate A Quicktesting!
	def doAntiGenTest(self,hour):
		threshold = 1-ANTIGEN_FAKE * ANTIGEN_SPECIFICITY
		if(self.infected == True):
			#Würfeln ob Antigentest falsch-negativ ist und nur korrekt wenn gleichzeitig Infektiösität da ist!
			if(randint(0, 10000) <= (threshold*10000) and self.virulent):
				return True
			else:
				return False
		else:
			return False
	def doPCRTest(self,hour):
		threshold = PCR_SPECIFICITY
		if(self.infected == True):
			#Würfeln ob PCR falsch-negativ ist.
			#TODO Zeiraum!!!!
			if(randint(0, 10000) <= (threshold*10000)):
				return True
			else:
				return False
		else:
			return False

class Simulation():
	humans = []
	kicked = 0
	def __init__(self):
		self.hour = 0
	def addHumans(self,count):
		for i in range(0,count):
			self.humans.append(Human(self.hour))
	def runner(self,hours):
		#Run simulation for x hours
		for i in range(0,hours):
			self.hour = self.hour +1
			for human in self.humans:
				human.run(self.hour)
	def antigenTestAll(self):
		for human in self.humans:
			if(human.doAntiGenTest(self.hour)):
				 self.humans.remove(human)
				 self.kicked = self.kicked + 1
	def PCRTestAll(self):
		for human in self.humans:
			if(human.doPCRTest(self.hour)):
				 self.humans.remove(human)
				 self.kicked = self.kicked + 1

	def generateStats(self):
		infected_current = 0
		virulent_current = 0
		for human in self.humans:
			if(human.infected == True):
				infected_current = infected_current+1
			if(human.virulent == True):
				virulent_current = virulent_current+1
		print('Hour:', self.hour)
		print('infected:', infected_current)
		print('virulent:', virulent_current)
		print('kicked:', self.kicked)

simulation = Simulation()
print('***Starting Simulation***')
print('***Hour:',simulation.hour,'***')
simulation.addHumans(35000)
print('Add 35.000 Guests...')
simulation.runner(1)
simulation.generateStats()
print('antigenTestAll')
simulation.antigenTestAll()
simulation.generateStats()
print('10 Hours later')
simulation.runner(10)
print('PCR Test all')
simulation.PCRTestAll()
simulation.generateStats()
print('10 Hours later')
simulation.runner(10)
simulation.generateStats()
print('72 Hours later')
simulation.runner(72)
simulation.generateStats()

#https://www.diamandis.com/blog/false-sense-security