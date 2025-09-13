class TwitchAnalyticsException(Exception):
    """Base exception for Twitch Analytics MCP Server"""

    pass


class AuthenticationError(TwitchAnalyticsException):
    """Raised when there are authentication issues with Twitch API"""

    pass


class ServiceUnavailableError(TwitchAnalyticsException):
    """Raised when Twitch API is temporarily unavailable"""

    pass


class ResourceNotFoundError(TwitchAnalyticsException):
    """Raised when requested resources are not found"""

    pass


class RateLimitError(TwitchAnalyticsException):
    """Raised when API rate limits are exceeded"""

    pass


class ConfigurationError(TwitchAnalyticsException):
    """Raised when there are configuration issues"""

    pass
