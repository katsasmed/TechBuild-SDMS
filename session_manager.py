import threading
from typing import Dict, Any

class SessionManager:
    """Thread-safe Singleton class to manage active user sessions."""
    _instance = None
    _lock = threading.Lock() # Lock for thread safety

    def __new__(cls, *args, **kwargs):
        # Use the lock to ensure that only one thread 
        # can create the instance at a time.
        with cls._lock:
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
        self.active_sessions.pop(user_id, None)