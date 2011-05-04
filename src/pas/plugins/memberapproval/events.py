from zope.interface import implements
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent

class IUserApprovedEvent(IObjectEvent):
    """ User has been approved """

class IUserDisapprovedEvent(IObjectEvent):
    """ User has been disapproved """

class UserApprovedEvent(ObjectEvent):

    implements(IUserApprovedEvent)
    
    def __init__(self, object, userid):
        self.userid = userid
        ObjectEvent.__init__(self, object)

class UserDisapprovedEvent(ObjectEvent):

    implements(IUserDisapprovedEvent)
    
    def __init__(self, object, userid):
        self.userid = userid
        ObjectEvent.__init__(self, object)
