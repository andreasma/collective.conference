from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from zope.schema.interfaces import Bool

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.browser.radio import RadioFieldWidget

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from collective.conference import _

class IAttendee(form.Schema):
    """A conference attendee. Attendees can be added anywhere.
    """
    
    paymentway=SimpleVocabulary(
         [SimpleTerm(value=u'by bank transfer', title=_(u'By Bank transfer')),
          SimpleTerm(value=u'by paypal', title=_(u'Payment by PayPal')),
          SimpleTerm(value=u'by check', title=_(u'By Check'))]
         )
    
    title = schema.TextLine(
            title=_(u"Firstname Lastname"),
        )

  
    street = schema.TextLine(
            title=_(u"Street"),
            description=_(u"This data is mandatory and required for our internal procidures"),
            required=True,
        )
    
    city = schema.TextLine(
            title=_(u"City"),
            description=_(u"This data is mandatory and required for our internal procidures"),
            required=True,
        )
    
    postalcode = schema.TextLine(
                 title=_(u"Postal Code"),
                 description=_(u"This data is mandatory and required for our internal procidures"),
                 required=True,
        )
    
    country = schema.TextLine(
              title=_(u"Country"),
              description=_(u"This data is mandatory and required for our internal procidures"),
              required=True,
        )        

    email = schema.TextLine(
            title=_(u"E-Mail"),
            description=_(u"We need this mandatory data to get in contact with you, if we have any questions"),
            required=True,
        )

    
    organisation = schema.TextLine(
            title=_(u"Organisation"),
            required=False,
        )
    
    form.widget(registrationpayed=RadioFieldWidget)
    registrationpayed = schema.Bool(
            title=_(u"Payment of the Registration Fee"),
            description=_(u"Have you already paid the registration fee?"),
        )

    paymentway = schema.Choice(
            title=_(u"Way of Registration Fee Payment"),
            description=_(u"If you already payed the registration fee, please tell us, which way you used to transfer the money."),
            vocabulary= paymentway,
            required=False,
        )
    
    usedbank = schema.TextLine(
            title = _(u"Used Bank Account"),
            description =_(u"If you transfered the Registration Fee via a bank account, please tell us the name and branch of the bank you used. We need this information to identify your payment more quickly."),
            required=False,
        )
            

@grok.subscribe(IAttendee, IObjectAddedEvent)


class View(grok.View):
    grok.context(IAttendee)
    grok.require('zope2.View')
