import datetime

from zope.interface import invariant, Invalid

from zope.interface import invariant, Invalid
from DateTime import DateTime
from plone.indexer import indexer
from zope.component import createObject

from five import grok
from zope import schema

from Acquisition import aq_inner, aq_parent, aq_get
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

from zope.security import checkPermission

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.formwidget.autocomplete import AutocompleteFieldWidget

from collective.conference import _

from Products.CMFCore.utils import getToolByName



class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")

#class StartBeforeConferenceProgram(Invalid):
#    __doc__ = _(u"The start of the track could not before the conference program.")


class ITrack(form.Schema):
    """A conference track. Tracks are managed inside Programs.
    """

    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Track title"),
        )

    description = schema.Text(
            title=_(u"Track summary"),
        )

    form.primary('details')
    details = RichText(
            title=_(u"Track details"),
            required=False
        )
    

    start = schema.Datetime(
            title=_(u"Startdate"),
            description =_(u"Start date"),
            required=False,
        )

    end = schema.Datetime(
            title=_(u"Enddate"),
            description =_(u"End date"),
            required=False,
        )
    
    room = schema.TextLine(
            title= _(u"Room"),
        )
    
    
    
    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))
                
    
#    @invariant
#   def validateStartNotBeforeProgram(data):
#        if data.start is not None:
#            startprogram = datetime.date (aq_parent (data.start))
#            if data.start < datetime(startprogram):
#                raise StartBeforeConferenceProgram(_(
#                    u"The start date could not before the begin of the conference program."))
                
class View(dexterity.DisplayForm):
    grok.context(ITrack)
    grok.require('zope2.View')

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
