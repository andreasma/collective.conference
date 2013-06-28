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
from zope.schema.interfaces import Bool
from Products.CMFCore.utils import getToolByName
from zope.app.container.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


from collective import dexteritytextindexer

from Acquisition import aq_inner, aq_parent, aq_get



#from collective.conference.track import setdates


# class StartBeforeEnd(Invalid):
#   __doc__ = _(u"The start or end date is invalid")


@grok.provider(schema.interfaces.IContextSourceBinder)
def vocabCfPTracks(context):
    # For add forms

    # For other forms edited or displayed
    from collective.conference.callforpaper import ICallforpaper
    if context is not None and not ICallforpaper.providedBy(context):
        #context = aq_parent(aq_inner(context))
        context = context.__parent__

    track_list = []
    if context is not None and context.cfp_tracks:
        track_list = context.cfp_tracks

    terms = []
    for value in track_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)



class ITalk(form.Schema):
    """A conference talk. Talks are managed inside tracks of the Program.
    """
    
    length = SimpleVocabulary(
       [SimpleTerm(value=u'15', title=_(u'15 minutes')),
        SimpleTerm(value=u'30', title=_(u'30 minutes')),
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
            required=True
        )

    # use an autocomplete selection widget instead of the default content tree
    form.widget(speaker=AutocompleteFieldWidget)
    speaker = RelationChoice(
            title=_(u"Presenter"),
            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
            required=False,
        )
    form.widget(speaker=AutocompleteFieldWidget)
    speaker2 = RelationChoice(
            title=_(u"Co-Presenter"),
            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
            required=False,
        )
 
    form.widget(speaker=AutocompleteFieldWidget)
    speaker3 = RelationChoice(
            title=_(u"Co-Presenter"),
            source=ObjPathSourceBinder(object_provides=ISpeaker.__identifier__),
            required=False,
        )
 

    dexteritytextindexer.searchable('call_for_paper_tracks')
    call_for_paper_tracks = schema.List(
        title=_(u"Choose the track for your talk"),
        value_type=schema.Choice(source=vocabCfPTracks),
        required=True,
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
    dexterity.write_permission(order='collective.conference.ModifyTrack')  
    order=schema.Int(
           title=_(u"Orderintrack"),               
           description=_(u"Order in the track: write in an Integer from 1 to 12"),
           min=1,
           max=12,
           required=False,
        )
                  
    
    slides = NamedBlobFile(
            title=_(u"Presentation slides in ODT-File-Format"),
            description=_(u"Please upload your presentation shortly after you have given your talk."),
            required=False,
        )
    
    slides2 = NamedBlobFile(
            title=_(u"Presentation slides in PDF-File-Format or PDF-Hybrid-File-Format"),
            description=_(u"Please upload your presentation shortly after you have given your talk."),
            required=False,
        )

    slides3 = schema.URI(
            title=_(u"Link to the presentation slides in ODT-File-Format"),
            required=False,
        )
    slides4 = schema.URI(
        title=_(u"Link to the presentation slides in PDF-File-Format or PDF-Hybrid-File-Format"),
        required=False,
       )

    files = NamedBlobFile(
            title=_(u"Additional Files of your presentation."),
            description=_(u"Please upload the additional files of your presentation (in archive format) shortly after you have given your talk."),
            required=False,
        )

    files2 = schema.URI(
            title=_(u"Link to additional Files of your presentation in archive file format (e.g. zip-file-format."),
            required=False,
        )

    video = schema.URI(
            title=_(u"Link to the Video of the talk"),
            required=False,
        )
    creativecommonslicense= schema.Bool(
            title=_(u'label_creative_commons_license', default=u'License is Creative Commons Attribution-Share Alike 3.0 License.'),
                description=_(u'help_creative_commons_license', default=u'You agree that your talk and slides are provided under the Creative Commons Attribution-Share Alike 3.0 License.'),
                default=True
        )
    
    messagetocommittee = schema.Text (
            title=_(u'Messages to the Program Committee'),
            description=_(u'You can give some information to the committee here, e.g. about days you are (not) available to give the talk'),
            required=False,                     
        )
    
    dexterity.read_permission(reviewNotes='cmf.ReviewPortalContent')
    dexterity.write_permission(reviewNotes='cmf.ReviewPortalContent')
    reviewNotes = schema.Text(
            title=u"Review notes",
            required=False,
        )


    
#@grok.subscribe(ITalk, IObjectAddedEvent)
#def talkaddedevent(talk, event):
#    setdates(talk)

#@grok.subscribe(ITalk, IObjectModifiedEvent)
#def talkmodifiedevent(talk, event):
#    setdates(talk)
    

#    @invariant
#    def validateStartEnd(data):
#        if data.start is not None and data.end is not None:
#            if data.start > data.end:
#                raise StartBeforeEnd(_(
#                    u"The start date must be before the end date."))

class View(dexterity.DisplayForm):
    grok.context(ITalk)
    grok.require('zope2.View')

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
