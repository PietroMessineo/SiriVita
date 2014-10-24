#!/usr/bin/python
# -*- coding: utf-8 -*-
#Made by Maxx
#Thanks to JimmyKane and his debug level 9 for the siriproxy (<333) and Eichhoernchen for
#making the python siriserver
#Credits to gaVRos for some minor adjustments and testing
#Thanks to Pietro Messineo that had imported in Italian languages this plugin

import re
import logging
import time
import pytz

from datetime import *
from pytz import timezone
from uuid import uuid4
from plugin import *

from siriObjects.baseObjects import *
from siriObjects.uiObjects import *
from siriObjects.systemObjects import *
from siriObjects.emailObjects import *

class checkEmail(Plugin):

	#Command to activate the checking of email...
	@register("it-IT","(.*controlla (.*mail.*)|(.*email.*))")
	@register("en-GB","(.*check.* (.*mail.*)|(.*email.*))")
	def emailSearch(self, speech, language):

		#Let user know siri is searching for your mail GOOD!
		view_initial = AddViews(self.refId, dialogPhase="Reflection")
		view_initial.views = [AssistantUtteranceView(text="Controllo la posta...", speakableText="Controllo la posta...", dialogIdentifier="EmailFindDucs#findingNewEmail")]
		self.sendRequestWithoutAnswer(view_initial)
		
		#Grabs the timeZone given by the client
		tz = timezone(self.connection.assistant.timeZoneId)
		
		#Search object to find the mail GOOD!
		email_search = EmailSearch(self.refId)
		email_search.timeZoneId = self.connection.assistant.timeZoneId
		email_search.startDate = datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=tz)
		email_search.endDate = datetime.now(tz)
		email_return = self.getResponseForRequest(email_search)
		
		if email_return["class"] != "CommandFailed":
			if email_return["properties"]["emailResults"] == []:
				view = AddViews(self.refId, dialogPhase="Summary")
				view.views += [AssistantUtteranceView(text="Non c'Ë alcuna e-mail.", speakableText="Non c'Ë alcuna mail.", dialogIdentifier="EmailFindDucs#foundNoEmail")]
				self.sendRequestWithoutAnswer(view)
			else:
				email_ = email_return["properties"]["emailResults"] 
				#Display the mail! It works :D!
				view = AddViews(self.refId, dialogPhase="Summary")
				view1 = AssistantUtteranceView(text="Ok,questo Ë quello che ho trovato: ", speakableText="Ok,questo Ë quello che ho trovato: ", dialogIdentifier="EmailFindDucs#foundEmail")
				snippet = EmailSnippet()
				snippet.emails = email_
				view2 = snippet
				view.views = [view1, view2]
				self.sendRequestWithoutAnswer(view)
		else:
			view = AddViews(self.refId, dialogPhase="Summary")
			view1 = AssistantUtteranceView(text="Non hai un account di posta ancora configurato.", speakableText="Non hai un account di posta ancora configurato.", dialogIdentifier="EmailCreateDucs#noEmailAccount")
			view2 = AssistantUtteranceView(text="Basta lanciare l'applicazione Mail, che vi guider‡ attraverso il processo di installazione.", speakableText="Basta lanciare l'applicazione Mail, che vi guider‡ attraverso il processo di installazione.", dialogIdentifier="EmailCreateDucs#noEmailAccount")
			view.views = [view1, view2]
			self.sendRequestWithoutAnswer(view)
		self.complete_request()
