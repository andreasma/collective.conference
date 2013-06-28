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

from collective.conference.talk import ITalk
from collective.conference.workshop import IWorkshop

class ICallforpaper(form.Schema):
    """A call for paper for a conference. 
    A call for paper can contain incomming talks.
    """
    
    
    title = schema.TextLine(
            title=_(u"Call for paper title"),
        )

    description = schema.Text(
            title=_(u"Call for paper summary"),
        )
    
    
    form.primary('details')
    details = RichText(
            title=_(u"Details"),
            description=_(u"Details about the program"),
            required=True,
        )
        
    cfp_tracks = schema.List(title=_(u"Tracks for the Call for Papers"),
           default=['Development',
                    'Documentation',
                    'Project-Administration'],
           value_type=schema.TextLine()
        )

    


# Views

class View(grok.View):
    grok.context(ICallforpaper)
    grok.require('zope2.View')

    def talks(self):
        """Return a catalog search result of talks to show
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=ITalk.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_order='sortable_title')


# File representation

class CallforpaperFileFactory(grok.Adapter):
    """Custom file factory for programs, which always creates a Track.
    """

    grok.implements(IFileFactory)
    grok.context(ICallforpaper)

    def __call__(self, name, contentType, data):
        talk = createObject('collective.conference.talk')
        notify(ObjectCreatedEvent(talk))
        return talk
