import datetime

from zope.interface import invariant, Invalid


from five import grok
from zope import schema

from Acquisition import aq_inner, aq_parent
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

from zope.security import checkPermission

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.formwidget.autocomplete import AutocompleteFieldWidget

from collective.conference import _

from collective.conference.speaker import ISpeaker

from plone.namedfile.field import NamedBlobFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")


class ITalk(form.Schema):
    """A conference talk. Talks are managed inside tracks of the Program.
    """
    
    length = SimpleVocabulary(
       [SimpleTerm(value=u'30', title=_(u'30 minutes')),
        SimpleTerm(value=u'45', title=_(u'45 minutes')),
        SimpleTerm(value=u'60', title=_(u'60 minutes'))]
        )

    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Talk title"),
        )

    description = schema.Text(
            title=_(u"Talk summary"),
        )

    form.primary('details')
    details = RichText(
            title=_(u"Talk details"),
            required=False
        )

    # use an autocomplete selection widget instead of the default content tree
    form.widget(speaker=AutocompleteFieldWidget)
    speaker = RelationChoice(
            title=_(u"Speaker"),
            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
            required=False,
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
    
        
    length= schema.Choice(
            title=_(u"Length"),
            vocabulary=length,
            required=True,
        )
  
  
    order=schema.Int(
           title=_(u"Orderintrack"),               
           description=_(u"Order in the track: write in an Integer"),
           required=False,
        )
                  
    
    slides = NamedBlobFile(
            title=_(u"Presentation slides"),
            description=_(u"Please upload your presentation"),
            required=False,
        )

    
    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))

class View(dexterity.DisplayForm):
    grok.context(ITalk)
    grok.require('zope2.View')

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
