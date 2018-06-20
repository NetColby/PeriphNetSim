#Attenuated Communication Model
#Created by Emmett Burns
#06/20/2018

from CommunicationModel import CommunicationModel
import random

class Attenuated(CommunicationModel):

	def __init__(self, c=1, a=1, v=1):
		CommunicationModel.__init__(self)
		self.constant = c
		self.alpha = a
		self.valueForCompare = v
		self.communicationRange = 100

	def attemptCommunication(self, distance):
		f = (self.constant/(distance**self.alpha))
		return f < self.valueForCompare

if __name__ == "__main__" :
	at = Attenuated(1, 1, 1)
	print(at.attemptConnect(1))