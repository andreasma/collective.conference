from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from collective.conference import _


class IRoom(form.Schema):
    """A conference room.
    """
    
    title = schema.TextLine(
            title=_(u"Name of the Room"),
        )


    description = schema.Text(
            title=_(u"A description of the room and its location"),
        )

    
    picture = NamedBlobImage(
            title=_(u"A picture of the room"),
            description=_(u"Please upload an image"),
            required=False,
        )
    
    form.primary ('details')
    details = RichText(
             title=_(u"A full description of the room, it's location and the way to get there"),
             required=True,                          
        )
    
    capacity = schema.Int(
             title=_(u"Capacity of the room"),
             description=_(u"Please fill in the maximum number of attendees"),
             required=False,
        )

@grok.subscribe(IRoom, IObjectAddedEvent)


class View(grok.View):
    grok.context(IRoom)
    grok.require('zope2.View')
