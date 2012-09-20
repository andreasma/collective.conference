import datetime

from zope.interface import invariant, Invalid


from five import grok
from zope import schema

from Acquisition import aq_inner, aq_parent
from zope.schema.interfaces import IContextSourceBinder

from zope.security import checkPermission

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.formwidget.autocomplete import AutocompleteFieldWidget

from collective.conference import _


from collective.conference.track import ITrack
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


from Products.CMFCore.utils import getToolByName
from zope.app.container.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from collective.conference.track import setdates


class IConferencebreak(form.Schema):

    """A conference break. Breaks (e.g. for lunch) are managed inside tracks of the Program.
    """
    
    
        
    length = SimpleVocabulary(
       [SimpleTerm(value=u'15', title=_(u'15 minutes')),
        SimpleTerm(value=u'30', title=_(u'30 minutes')),
        SimpleTerm(value=u'45', title=_(u'45 minutes')),
        SimpleTerm(value=u'60', title=_(u'60 minutes'))]
        )
    
    
    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Conference break title"),
        )

    description = schema.Text(
            title=_(u"Conference break summary"),
        )

    form.primary('details')
    details = RichText(
            title=_(u"Conference break details"),
            required=True
        )
        
        
    form.widget(track=AutocompleteFieldWidget)
    track = RelationChoice(
            title=_(u"Track"),
            source=ObjPathSourceBinder(object_provides=ITrack.__identifier__),
            required=False,
        )


    dexterity.write_permission(startitem='collective.conference.ModifyTalktime')
    startitem = schema.Datetime(
            title=_(u"Startdate"),
            description =_(u"Start date"),
            required=False,
        )
    

    dexterity.write_permission(enditem='collective.conference.ModifyTalktime')
    enditem = schema.Datetime(
            title=_(u"Enddate"),
            description =_(u"End date"),
            required=False,
        )
    
            
    length= schema.Choice(
            title=_(u"Length"),
            vocabulary=length,
            required=True,
        )
    
    
    
@grok.subscribe(IConferencebreak, IObjectAddedEvent)
def conferencebreakaddedevent(conferencebreak, event):
    setdates(conferencebreak)

@grok.subscribe(IConferencebreak, IObjectModifiedEvent)
def conferencebreakmodifiedevent(conferencebreak, event):
    setdates(conferencebreak)
    


class View(dexterity.DisplayForm):
    grok.context(IConferencebreak)
    grok.require('zope2.View')

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
    