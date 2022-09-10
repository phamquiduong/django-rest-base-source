import os
import jwt
from core import logger


JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
SECRET_KEY = os.getenv('SECRET_KEY')


def jwt_encode(payload: dict) -> str:
    """ JWT Encode

    Args:
        payload (dict): payload need JWT encode

    Returns:
        (str): JWT token if JWT encode success.
               Else if encode fail return empty string
    """

    logger.info('JWT encode: ' + str(payload))

    try:
        return jwt.encode(
            payload=payload,
            key=SECRET_KEY,
            algorithm=JWT_ALGORITHM
        )
    except Exception as e:
        logger.error(str(e))
        return ''


def jwt_decode(token: str) -> dict:
    """ Decode JWT token

    Args:
        token (str): JWT token need decode

    Returns:
        (dict): If decode success dict have 'payload' key.
                Else if decode fail, dict will have 'errors' key
    """

    logger.info('JWT decode: ' + token)

    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=JWT_ALGORITHM
        )
        return {'payload': payload}
    except jwt.ExpiredSignatureError:
        logger.error('Signature expired')
        return {'errors': 'Signature expired'}
    except jwt.InvalidTokenError:
        logger.error('Invalid token')
        return {'errors': 'Invalid token'}
    except Exception as e:
        logger.error(str(e))
        return {'errors': str(e)}
