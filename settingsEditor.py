#Emmett Burns
#06/27/2018
#Settings Updator

# MAINTENANCE ONLY
# file that allows to change settings from the command line so that we can run multiple simualtions in a row in bach files

import sys

class settingsEditor:

	def __init__(self):
		pass

	def editSetting(self, setting, newSetting):
		file = open("settings.txt", "r")
		text = file.read()
		settingWOequals = setting
		setting += "="
		halves = text.split(setting)
		portionToBeChanged = halves[1].split("\n")
		oldSetting = portionToBeChanged[0]
		portionToBeChanged[0] = newSetting
		newSecondHalf = "\n".join(portionToBeChanged)
		newSettingsList = [halves[0], newSecondHalf]
		newSettings = setting.join(newSettingsList)
		file = open("settings.txt", "w")
		file.write(newSettings)
		file.close()
		print("\n\n____________________SETTINGS UPDATE____________________\n\n" +
			settingWOequals + " changed from " + oldSetting + " to " + newSetting + "\n\n")

if __name__ ==  "__main__":
	se = settingsEditor()
	se.editSetting(sys.argv[1], sys.argv[2])
