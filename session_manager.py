from typing import Dict, Any

class SessionManager:
    """Singleton class to manage and enforce active user sessions."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SessionManager, cls).__new__(cls, *args, **kwargs)
            # Initialize the state only once
            cls._instance.active_sessions: Dict[str, Any] = {}
        return cls._instance

    def establish_session(self, user_id: str) -> None:
        """Creates a new active session for the user."""
        self.active_sessions[user_id] = {"status": "active"}

    def enforce_single_session(self, user_id: str) -> bool:
        """Checks if the user already has an active session."""
        return user_id in self.active_sessions

    def terminate_session(self, user_id: str) -> None:
        """Ends the active session for the specified user."""
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]