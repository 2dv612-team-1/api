"""
JWT handler
"""

from exceptions.NoJWT import NoJWT
from exceptions.TamperedToken import TamperedToken
from exceptions.NotAuthorized import NotAuthorized
from utils.string import *
from config import SECRET
import jwt


def extract(request):
    """Extract payload from JWT token

    Arguments:
        request - request object from flask

    Raises:
        NoJWT -- No JWT token was present in request
        TamperedToken -- JWT token was tampered

    Returns:
        payload - extracted from JWT token
    """

    try:
        token = request.form[JWT]
    except Exception:
        raise NoJWT('No JWT present in request')

    try:
        payload = jwt.decode(token, SECRET)
    except Exception:
        raise TamperedToken('Token has been tampered')

    return payload


def authorized_role(payload, role):
    """Check the role of the payload to match the expected

    Arguments:
        payload -- payload extracted from JWT token
        role string -- the expected role
    """

    if payload[ROLE] != role:
        raise NotAuthorized('Forbidden')

def encode(payload):
    """Encodes the payload with the super secret

    Arguments:
        payload -- payload to encode
    Returns:
        encoded -- the encoded payload
    """

    return jwt.encode(payload, SECRET)

def decode(token):
    """Decode token

    Arguments:
        token {jwt token} -- JWT Token to decode

    Returns:
        Decoded JWT
    """

    return jwt.decode(token, SECRET)
