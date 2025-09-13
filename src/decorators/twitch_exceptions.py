import functools
from ..utils.exceptions import (
    AuthenticationError,
    ServiceUnavailableError,
)
from twitchAPI.type import (
    TwitchAPIException,
    UnauthorizedException,
    InvalidTokenException,
    TwitchBackendException,
    MissingScopeException,
)


def handle_twitch_exceptions(func):
    """Decorator to transform Twitch API exceptions to domain exceptions

    Only handles exception transformation - logging is handled by caller
    """

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            result = await func(self, *args, **kwargs)
            return result

        except (
            InvalidTokenException,
            UnauthorizedException,
            MissingScopeException,
        ) as e:
            raise AuthenticationError(f"Invalid Twitch API credentials: {e}")
        except TwitchBackendException:
            raise ServiceUnavailableError(
                "Twitch API is currently unavailable. Please try again later."
            )
        except TwitchAPIException as e:
            raise ServiceUnavailableError(f"Error communicating with Twitch API: {e}")
        except Exception as e:
            raise ServiceUnavailableError(f"An unexpected error occurred: {e}")

    return wrapper
