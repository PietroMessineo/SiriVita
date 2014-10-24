#!/usr/bin/python
# -*- coding: utf-8 -*-

from plugin import *
import time
import datetime
import re
from fractions import Fraction
from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject
from siriObjects.alarmObjects import *

class Nap(Plugin):

	localizations = {
        'Alarm': {
            "settingAlarm": {
                "it-IT": u"Impostando la sveglia\u2026"
            }, "alarmWasSet": {
                "it-IT": "La tua sveglia e' impostato per le {0}:{1} {2}."
            }, "alarmSetWithLabel": {
                "it-IT": "La tua sveglia {0} {1} e' impostata per {2}:{3} {4}."
            }
        }
    	}

	@register("it-IT", "Svegliami in ([0-5][0-9]|[0-9]) (ora|ore|minuti)")
	def Nap(self, speech, language):
		global time
		currenttime = time.time()
		hour = time.strftime('%H', time.localtime(currenttime))

		if hour >= 12:
			alarmAMPM = 'PM'
		else:
			alarmAMPM = 'AM'
	
		c = re.search("minuti|ora|ore", speech)
		d = c.group() 
		a = re.search('([0-5][0-9]|[0-9])', speech)
		b = a.group()
			
		if d == ("minuti"):
		
			currenttime = time.time()
			alarmHour = time.strftime('%H', time.localtime(currenttime + int(b) * 60))
			alarmMinutes = time.strftime('%M', time.localtime(currenttime + int(b) * 60))
			
		if d == ("ora"):
			
			currenttime = time.time()
			alarmHour = time.strftime('%H', time.localtime(currenttime + int(b) * 60 * 60))
			alarmMinutes = time.strftime('%M', time.localtime(currenttime + int(b) * 60 * 60))
			
		if d ==("ore"):
			
			currenttime = time.time()
			alarmHour = time.strftime('%H', time.localtime(currenttime + int(b) * 60 * 60))
			alarmMinutes = time.strftime('%M', time.localtime(currenttime + int(b) * 60 * 60))
			

		if int(alarmHour) >= 13:
			alarmHour12 = (int(alarmHour) - 12)
		else:
			alarmHour12 = alarmHour

		view = AddViews(self.refId, dialogPhase="Reflection")
        	view.views = [
           	AssistantUtteranceView(
                speakableText=Nap.localizations['Alarm']['settingAlarm'][language],
                dialogIdentifier="Alarm#settingAlarm")]
        	self.sendRequestWithoutAnswer(view)

		#create the alarm
		alarmLabel = None
		alarm = AlarmObject(alarmLabel, int(alarmMinutes), int(alarmHour), None, 1)
		response = self.getResponseForRequest(AlarmCreate(self.refId, alarm))
		
		print(Nap.localizations['Alarm']['alarmWasSet'][language].format(alarmHour12, alarmMinutes, alarmAMPM))
		view = AddViews(self.refId, dialogPhase="Completion")
		
		if alarmLabel == None:
		    view1 = AssistantUtteranceView(speakableText=Nap.localizations['Alarm']['alarmWasSet'][language].format(alarmHour12, alarmMinutes, alarmAMPM), dialogIdentifier="Alarm#alarmWasSet")
		else:
		    view1 = AssistantUtteranceView(speakableText=Nap.localizations['Alarm']['alarmSetWithLabel'][language].format(alarmLabelExists, alarmLabel, alarmHour12, alarmMinutes, alarmAMPM), dialogIdentifier="Alarm#alarmSetWithLabel")
		
		view2 = AlarmSnippet(alarms=[alarm])
		view.views = [view1, view2]
		self.sendRequestWithoutAnswer(view)
		self.complete_request()
					
				
