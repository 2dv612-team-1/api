class NotAuthorized(Exception):
    """Raised if role from JWT doesn't match the expected authorized role"""
    pass
