"""Only this package handles Google endpoints, identity and token cryptography."""
from .client import GmailConnector, ConnectorError, GmailUnavailable, get_connector

__all__ = ["GmailConnector", "ConnectorError", "GmailUnavailable", "get_connector"]
