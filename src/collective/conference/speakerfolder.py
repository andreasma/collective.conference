from five import grok
from zope import schema

from zope.component import createObject
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.filerepresentation.interfaces import IFileFactory

from DateTime import DateTime
from plone.indexer import indexer

from plone.directives import form
from plone.app.textfield import RichText

from plone.formwidget.autocomplete import AutocompleteFieldWidget
from z3c.form.browser.textlines import TextLinesFieldWidget

from collective.conference import _

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from plone.directives import form, dexterity
from zope.security import checkPermission

from collective.conference.speaker import ISpeaker

class ISpeakerfolder(form.Schema):
    """A speaker folder. The speaker of the conference are created in the folder.
    """


    title = schema.TextLine(
            title=_(u"Name of the speaker folder"),
        )

    description = schema.Text(
            title=_(u"speakerfolder description"),
        )
    
class View(dexterity.DisplayForm):
    grok.context(ISpeakerfolder)
    grok.require('zope2.View')

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)   