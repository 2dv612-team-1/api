"""
JWT handler
"""

from exceptions.NoJWT import NoJWT
from exceptions.TamperedToken import TamperedToken
from exceptions.IncorrectRole import IncorrectRole
import jwt

SUPER_SECRET = 'super-secret'


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
        token = request.form['jwt']
    except Exception:
        raise NoJWT('No JWT present in request')

    try:
        payload = jwt.decode(token, SUPER_SECRET)
    except Exception:
        raise TamperedToken('Token has been tampered')

    return payload


def authorized_role(payload, role):
    """Check the role of the payload to match the expected

    Arguments:
        payload -- payload extracted from JWT token
        role string -- the expected role
    """

    if payload['role'] != role:
        raise IncorrectRole('You are not a ' + role)

def encode(payload):
    """Encodes the payload with the super secret

    Arguments:
        payload -- payload to encode
    Returns:
        encoded -- the encoded payload
    """

    return jwt.encode(payload, SUPER_SECRET)