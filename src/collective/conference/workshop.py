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
from collective.conference.track import ITrack

from plone.namedfile.field import NamedBlobFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm




# class StartBeforeEnd(Invalid):
#     __doc__ = _(u"The start or end date is invalid")


class IWorkshop(form.Schema):
    """A conference workshop. Workshops are managed inside tracks of the Program.
    """
        
    length = SimpleVocabulary(
       [SimpleTerm(value=u'30', title=_(u'30 minutes')),
        SimpleTerm(value=u'45', title=_(u'45 minutes')),
        SimpleTerm(value=u'60', title=_(u'60 minutes'))]
        )
    

    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Workshop title"),
        )

    description = schema.Text(
            title=_(u"Workshop summary"),
        )

    form.primary('details')
    details = RichText(
            title=_(u"Workshop details"),
            required=False
        )

    # use an autocomplete selection widget instead of the default content tree
    form.widget(speaker=AutocompleteFieldWidget)
    speaker = RelationChoice(
            title=_(u"Leader of the workshop"),
            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
            required=False,
        )
    form.widget(speaker=AutocompleteFieldWidget)
    speaker2 = RelationChoice(
            title=_(u"Co-Leader of the workshop"),
            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
            required=False,
        )
    form.widget(track=AutocompleteFieldWidget)
    track = RelationChoice(
            title=_(u"Track"),
            source=ObjPathSourceBinder(object_provides=ITrack.__identifier__),
            required=False,
        )
    
        
    
#    start = schema.Datetime(
#            title=_(u"Startdate"),
#            description =_(u"Start date"),
#            required=False,
#        )
#
#    end = schema.Datetime(
#            title=_(u"Enddate"),
#            description =_(u"End date"),
#            required=False,
#        )
    
            
    length= schema.Choice(
            title=_(u"Length"),
            vocabulary=length,
            required=True,
        )
  

    dexterity.write_permission(order='collective.conference.ModifyTrack')        
    order=schema.Int(
           title=_(u"Orderintrack"),               
           description=_(u"Order in the track: write in an Integer from 1 to 12"),
           min=1,
           max=12,
           required=False,
        )
                    
    
    slides = NamedBlobFile(
            title=_(u"Workshop slides / material"),
            description=_(u"Please upload your workshop presentation or material about the content of the workshop."),
            required=False,
        )    
    
    
    creativecommonslicense= schema.Bool(
            title=_(u'label_creative_commons_license', default=u'License is Creative Commons Attribution-Share Alike 3.0 License.'),
                description=_(u'help_creative_commons_license', default=u'You agree that your talk and slides are provided under the Creative Commons Attribution-Share Alike 3.0 License.'),
                default=True
        )
    
    dexterity.read_permission(reviewNotes='cmf.ReviewPortalContent')
    dexterity.write_permission(reviewNotes='cmf.ReviewPortalContent')
    reviewNotes = schema.Text(
            title=u"Review notes",
            required=False,
        )

    
#    @invariant
#    def validateStartEnd(data):
#        if data.start is not None and data.end is not None:
#            if data.start > data.end:
#                raise StartBeforeEnd(_(
#                    u"The start date must be before the end date."))
                



class View(dexterity.DisplayForm):
    grok.context(IWorkshop)
    grok.require('zope2.View')

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
