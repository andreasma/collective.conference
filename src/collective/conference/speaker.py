import re
from zope.interface import Invalid

from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from collective.conference import _


checkEmail = re.compile(
     r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match
     
def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True

class ISpeaker(form.Schema):
    """A conference speaker or leader of a workshop. Speaker can be added anywhere.
    """
    
    title = schema.TextLine(
            title=_(u"Your complete name"),
        )
    
    lastname= schema.TextLine(
            title=_(u"Last name"),
        )
    
    firstname = schema.TextLine(
             title=_(u"First name"),
             required=True,
        )
  
    street = schema.TextLine(
            title=_(u"Street"),
            description=_(u"For those requiring visa, please add your full postal address details"),
            required=False,
        )
    
    city = schema.TextLine(
            title=_(u"City"),
            description=_(u"For those requiring visa, please add your full postal address details"),
            required=False,
        )
    
    postalcode = schema.TextLine(
                 title=_(u"Postal Code"),
                 description=_(u"For those requiring visa, please add your full postal address details"),
                 required=False,
        )
    
    country = schema.TextLine(
              title=_(u"Country"),
              description=_(u"For those requiring visa, please add your full postal address details"),
              required=False,
        )        

    email = schema.ASCIILine(
            title=_(u"Your email address"),
            constraint=validateEmail,
            required=True,
        )

    telephonenumber = schema.TextLine(
            title=_(u"Telephone Number"),
            description=_(u"Please fill in your telephone number so that we could get in contact with you by phone if necessary."),
            required=False,
        )
    mobiletelepone = schema.TextLine(
            title=_(u"Mobile Telephone Number"),
            description=_(u"Please fill in your mobile telephone number so that we could get in contact with you during the conference."),
            required=True,
        )
    
    organisation = schema.TextLine(
            title=_(u"Organisation"),
            required=False,
        )

    description = schema.Text(
            title=_(u"A short bio"),
        )
    
    bio = RichText(
            title=_(u"Bio"),
            required=False
        )
    
    picture = NamedBlobImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
        )

@grok.subscribe(ISpeaker, IObjectAddedEvent)
def notifyUser(speaker, event):
    acl_users = getToolByName(speaker, 'acl_users')
    mail_host = getToolByName(speaker, 'MailHost')
    portal_url = getToolByName(speaker, 'portal_url')

    portal = portal_url.getPortalObject()
    sender = portal.getProperty('email_from_address')

    if not sender:
        return

    subject = "Is this you?"
    message = "A speaker /leader of a workshop called %s was added here %s. If this is you, everything is fine." % (speaker.title, speaker.absolute_url(),)

    matching_users = acl_users.searchUsers(fullname=speaker.title)
    for user_info in matching_users:
        email = user_info.get('email', None)
        if email is not None:
            mail_host.secureSend(message, email, sender, subject)

class View(grok.View):
    grok.context(ISpeaker)
    grok.require('zope2.View')
