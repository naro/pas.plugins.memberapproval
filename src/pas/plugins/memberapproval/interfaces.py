from zope.interface import Interface
  
class IMemberApprovalPlugin(Interface):
    """interface for MemberapprovalPlugin."""

    def userApproved(user_id):
        """ Returns true if user is approved """

    def approveUser(user_id):
        """ Approve particular user """

    def disapproveUser( user_id):
        """ Disnapprove particular user """

