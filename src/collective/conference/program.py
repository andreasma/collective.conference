import datetime

from zope.interface import invariant, Invalid

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

from collective.conference.track import ITrack




class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")


class IProgram(form.Schema):
    """A conference program. Programs can contain Tracks.
    """

    title = schema.TextLine(
            title=_(u"Program name"),
        )

    description = schema.Text(
            title=_(u"Program summary"),
        )

    start = schema.Datetime(
            title=_(u"Start date"),
            required=False,
        )

    end = schema.Datetime(
            title=_(u"End date"),
            required=False,
        )

    form.primary('details')
    details = RichText(
            title=_(u"Details"),
            description=_(u"Details about the program"),
            required=False,
        )

    form.widget(organizer=AutocompleteFieldWidget)
    organizer = schema.Choice(
            title=_(u"Organiser"),
            vocabulary=u"plone.principalsource.Users",
            required=False,
        )


    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))


@form.default_value(field=IProgram['start'])
def startDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(7)


@form.default_value(field=IProgram['end'])
def endDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(10)

# Indexers


@indexer(IProgram)
def startIndexer(obj):
    if obj.start is None:
        return None
    return DateTime(obj.start.isoformat())
grok.global_adapter(startIndexer, name="start")


@indexer(IProgram)
def endIndexer(obj):
    if obj.end is None:
        return None
    return DateTime(obj.end.isoformat())
grok.global_adapter(endIndexer, name="end")


@indexer(IProgram)
def tracksIndexer(obj):
    return obj.tracks
grok.global_adapter(tracksIndexer, name="Subject")


# Views

class View(grok.View):
    grok.context(IProgram)
    grok.require('zope2.View')

    def tracks(self):
        """Return a catalog search result of tracks to show
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=ITrack.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_order='sortable_title')


# File representation

class ProgramFileFactory(grok.Adapter):
    """Custom file factory for programs, which always creates a Track.
    """

    grok.implements(IFileFactory)
    grok.context(IProgram)

    def __call__(self, name, contentType, data):
        track = createObject('collective.conference.track')
        notify(ObjectCreatedEvent(track))
        return track
