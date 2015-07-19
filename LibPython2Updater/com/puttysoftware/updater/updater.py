import urllib
from Tkinter import *
from tkMessageBox import *
import webbrowser

class UpdaterCLI(object):

	# Constructor
	def __init__(self, updateSite, major, minor, bugfix):
		self.updateURL = updateSite
		self.majorVersion = major
		self.minorVersion = minor
		self.bugfixVersion = bugfix

	# Method
	def checkForUpdatesCLI(self):
		self.newVersionMajor = self.majorVersion
		self.newVersionMinor = self.minorVersion
		self.newVersionBugfix = self.bugfixVersion
		try:
			updatereader = urllib.urlopen(self.updateURL)
			self.newVersionMajor = int(updatereader.readline())
			self.newVersionMinor = int(updatereader.readline())
			self.newVersionBugfix = int(updatereader.readline())
			updatereader.close()
		except IOError:
			raise UpdaterError()
		# Compare current version to most recent one
		if self.newVersionMajor > self.majorVersion:
			# Major update available
			return True
		elif self.newVersionMajor == self.majorVersion and self.newVersionMinor > self.minorVersion:
			# Minor update available
			return True
		elif self.newVersionMajor == self.majorVersion and self.newVersionMinor == self.minorVersion and self.newVersionBugfix > self.bugfixVersion:
			# Bug fix update available
			return True
		else:
			# No update
			return False
			
class UpdaterError(Exception):
	pass
	
class Updater(UpdaterCLI):
	
	# Constructor
	def __init__(self, updateSite, blurbSite, newVersionSite, major, minor, bugfix):
		UpdaterCLI.__init__(self, updateSite, major, minor, bugfix)
		self.blurbURL = blurbSite
		self.newVersionURL = newVersionSite
		
	def checkForUpdates(self):
		self.checkForUpdatesInternal(False)
		
	def checkForUpdatesAtStartup(self):
		self.checkForUpdatesInternal(True)
		
	def checkForUpdatesInternal(self, startup):
		update = False
		try:
			update = self.checkForUpdatesCLI()
		except UpdaterError:
			showerror("Updater Error", "An internal error occurred while checking for updates.")
		if update:
			# Read blurb
			blurb = ""
			try:
				line = ""
				blurbreader = urllib.urlopen(self.blurbURL)
				line = blurbreader.readline()
				while line != "":
					blurb = blurb + line + "\n"
					line = blurbreader.readline()
				blurbreader.close()
			except IOError:
				showerror("Updater Error", "An internal error occurred while checking for updates.")
			self.showUpdatesAvailableMessage(blurb)
		else:
			if (not startup):
				self.showNoUpdatesAvailableMessage()
		
	def showNoUpdatesAvailableMessage(self):
		# No updates
		showinfo("No Update Available", "You have the latest version.")
		
	def showUpdatesAvailableMessage(self, blurb):
		oldVersionString = str(self.majorVersion) + "." + str(self.minorVersion) + "." + str(self.bugfixVersion)
		newVersionString = str(self.newVersionMajor) + "." + str(self.newVersionMinor) + "." + str(self.newVersionBugfix)
		result = askyesno("Update Available", "Version " + newVersionString + " is available.\nYou have version " + oldVersionString + ".\n" + blurb + "Do you want to go to the program web site now?")
		if result:
			webbrowser.open(self.newVersionURL)
