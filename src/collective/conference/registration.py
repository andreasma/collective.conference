import re

from five import grok
from plone.directives import form
from zope.interface import Interface
from zope.interface import Invalid
from zope import schema
from z3c.form import field, button
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from collective.conference import _

from zope.schema.interfaces import Bool

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.browser.radio import RadioFieldWidget

from zope.component import getMultiAdapter
from Acquisition import aq_inner
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget


class ReCaptcha(object):
    subject = u""
    captcha = u""
    def __init__(self, context):
        self.context = context


checkEmail = re.compile(
     r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match
     
def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True


MESSAGE_TEMPLATE = """\

Registration from %(firstname)s  %(name)s <%(emailAddress)s>

Firstname: %(firstname)s
Name: %(name)s
Street: %(street)s
City: %(city)s
Postalcode: %(postalcode)s
Country: %(country)s
Organisation: %(organisation)s
Position: %(position)s
Conference Fee payed?: %(conferencefeepaid)s
Way of Payment: %(paymentway)s
Used Bank: %(usedbank)s
BIC: %(bankbic)s
IBAN: %(bankiban)s
Country of the Bank: %(bankcountry)s

Privacy Policy: %(privacypolicy)s


%(message)s
"""



class IRegistrationForm(Interface):
    """Define the fields of our form
    """

    name = schema.TextLine(
            title=_(u"Lastname"),
            description=_(u"Please fill in your lastname"),
        )
        
     
    firstname = schema.TextLine(
            title=_(u"Firstname"),
            description=_(u"Please fill in your firstname"),
        )
    
  
    street = schema.TextLine(
            title=_(u"Street"),
            description=_(u"This data is mandatory and required for our internal procedures"),
            required=True,
        )
    
    city = schema.TextLine(
            title=_(u"City"),
            description=_(u"This data is mandatory and required for our internal procedures"),
            required=True,
        )
    
    postalcode = schema.TextLine(
                 title=_(u"Postal Code"),
                 description=_(u"This data is mandatory and required for our internal procedures"),
                 required=True,
        )
    
    country = schema.TextLine(
              title=_(u"Country"),
              description=_(u"This data is mandatory and required for our internal procedures"),
              required=True,
        )        
        

    emailAddress = schema.ASCIILine(
            title=_(u"Your email address"),
            description=_(u"We need this mandatory data to send you the confirmation mail and to get in contact with you, if we have any questions"),
            constraint=validateEmail
        )


    
    organisation = schema.TextLine(
            title=_(u"Organisation"),
            required=False,
        )
    position = schema.TextLine(
            title=_(u"Position in your organisation"),
            required=False,
        )
        
    conferencefeepaid = schema.Choice(
           title=_(u"Did you already pay the conference fee?"),
           values=(u'No', u'Yes'),
           description=_(u"If your answer is yes, please answer also the following question."),
           required=True,
       ) 
    
    
    conferencefeepayexplanation= schema.TextLine(
            title =_(u"Imperative of Registration Fee Payment!"),
            description=_(u"If you have not paid the conference fee yet and you are not an accepted speaker or organizer, please stop here and pay the registration fee first. If you have not paid the registration fee before the registration for the conference closes (except you had not to pay because you are a speaker or an organizer) your registration will be dropped and you will not get access to the conference!!"),
            readonly=True,
            required=False,
        )   

    paymentway=schema.Choice(
           title=_(u"Way of Registration Fee Payment 2"),
           values=(u'Bank', u'PayPal'),
           description=_(u"If you already payed the registration fee, please tell us, which way you used to transfer the money:"),
           required=False,
       )

    bankdataexplanation= schema.TextLine(
            title =_(u"Information about used Bank account"),
            description=_(u"If you paid the conference fee by bank account, please fill in the data into the next fields. Otherwise you could skip this fields."),
            readonly=True,
            required=False,
        )
    
    usedbank = schema.TextLine(
            title = _(u"Used Bank Account"),
            description =_(u"(If you transfered the Registration Fee via a bank account, please tell us the name and branch of the bank you used. We need this information to identify your payment more quickly."),
            required=False,
        )
    bankbic = schema.TextLine(
            title =_(u"BIC of the bank you used for the transfer"),
            required=False,
        )
        
    bankiban = schema.TextLine(
            title=_(u"IBAN of the bank you used for the transfer"),
            required=False,
        )
            
    bankcountry = schema.TextLine(
            title=_(u"Country of the branch of the bank you used for the transfer"),
            required=False,
        )
    
    privacypolicytext = schema.Text(
            title=_(u"Privacy Policy"),
            description=_(u"The data entered during registration is used for the purposes of organizing the conference. Users may be informed via email about the conference, the registration, and technical circumstances. The data is collected as shown in the relative input boxes during the registration. You agree that this data will be processed by The Document Foundation and forwarded to the association Freies Office Deutschland e.V., the German Federal Ministry of Economics and Technology, and - except for the payment related data - the German Federal Ministry of the Interior for the purpose of organizing the conference and for ensuring the safety of the conference, including access control. Revocation, Changes, Corrections, and Updates The user has the right to receive, free of charge, information about his stored personal data. In addition, the user has the right to demand inaccurate data to be corrected, and personal data to be blocked or deleted, as long as there is no legal obligation to retain the data. To do so, write to info@documentfoundation.org. The organizers of the conference reserve the right to revoke the registration of conference participants in this case."),
            readonly=True,
            required=False,
        ) 
        
    privacypolicy = schema.Bool(
            title=_(u"Agree with the above privacy policy"),
            description=_(u"I agree with the terms of the privacy policy."),                         
            required=True,
            
       )

    
    message = schema.Text(
            title=_(u"Additional Message to the Organizers"),
            description=_(u"Please keep to 1,000 characters"),
            max_length=1000,
            required=False,
        )
        
    captcha = schema.TextLine(
            title=_(u"ReCaptcha"),
            description=_(u""),
            required=False
        )
        

class RegistrationForm(form.Form):
      
          
    grok.context(ISiteRoot)
    grok.name('register-for-the-conference')
    grok.require('zope2.View')
    
    fields = field.Fields(IRegistrationForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget
    
    label = _(u"Register for the Conference")
    description = _(u"If you want to ask the organizers of the conference or you want to send an comment please use the form below!")
    
    ignoreContext = True
    
    
    # Hide the editable border and tabs
    def update(self):
        self.request.set('disable_border', True)
        return super(RegistrationForm, self).update()
    
    @button.buttonAndHandler(_(u"Send"))
    def sendMail(self, action):
        """Send the email to the site administrator and redirect to the
        front page, showing a status message to say the message was received.
        """
        
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            captcha = getMultiAdapter((aq_inner(self.context), self.request), name='recaptcha')
            if captcha.verify():
               print 'ReCaptcha validation passed.'
            else:
               print 'The code you entered was wrong, please enter the new one.'
            return
        
        mailhost = getToolByName(self.context, 'MailHost')
        urltool = getToolByName(self.context, 'portal_url')
        
        portal = urltool.getPortalObject()

        # Construct and send a message
        toAddress = portal.getProperty('email_from_address')
        source = "%s <%s>" % (data['name'], data['emailAddress'])
        subject = "%s %s" % (data['firstname'], data['name'])
        message = MESSAGE_TEMPLATE % data

        mailhost.send(message, mto=toAddress, mfrom=str(source), subject=subject, charset='utf8')
        
        # Issue a status message
        confirm = _(u"Thank you! Your registration has been received and we will send you a confirmation mail as soon as posible.")
        IStatusMessage(self.request).add(confirm, type='info')
        
        # Redirect to the portal front page. Return an empty string as the
        # page body - we are redirecting anyway!
        self.request.response.redirect(portal.absolute_url())
        return ''
    
    @button.buttonAndHandler(_(u"Cancel"))
    def cancelForm(self, action):
        
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        
        # Redirect to the portal front page. Return an empty string as the
        # page body - we are redirecting anyway!
        self.request.response.redirect(portal.absolute_url())
        return u''


