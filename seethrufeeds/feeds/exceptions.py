class InvalidApiKey(TypeError):
    pass


class SecretKeyDoesNotExist(Exception):
    pass


class InvalidSecretKey(TypeError):
    pass


class AccessTokenDoesNotExist(Exception):
    pass


class InvalidAccessToken(TypeError):
    pass


class InvalidFeedGuid(TypeError):
    pass


class ApiError(Exception):
    pass


class MalformedApiResponse(ApiError):
    pass


class ApiUnexpectedError(ApiError):
    pass


class ApiInvalidGuid(ApiError):
    pass


class ApiKeyUnauthorized(ApiError):
    pass


class ApiKeyInvalidPermissions(ApiError):
    pass


class ApiKeyTimeout(ApiError):
    pass


class ApiInvalidFeedResult(ApiError):
    pass
