from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi.exceptions import HTTPException

def raise_404(text='not found', instead_exception=None):
    """
    Перехватывает исключение NoResultFound SqlAlchemy,
    затем либо вызывает HTTPException с кодом 404 и заданным текстом,
    либо возвращает return_instead_exception


    :param text: Текст исключения по умолчанию
    :param instead_exception:
    """
    def decorator(f):
        async def wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except NoResultFound:
                if instead_exception is not None:
                    return instead_exception

                raise HTTPException(status_code=404, detail=text)
        return wrapper
    return decorator


def raise_400(text='bad request', instead_exception=None):
    """
    Перехватывает исключение IntegrityError SqlAlchemy,
    затем либо вызывает HTTPException с кодом 400 и заданным текстом,
    либо возвращает return_instead_exception
    """
    def decorator(f):
        async def wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except IntegrityError:
                if instead_exception is not None:
                    return instead_exception

                raise HTTPException(status_code=400, detail=text)
        return wrapper
    return decorator
