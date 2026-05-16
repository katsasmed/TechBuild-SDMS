from abc import ABC, abstractmethod
from typing import Dict

class Document:
    def __init__(self, doc_id: str, payload: bytes):
        self.doc_id = doc_id
        self.payload = payload

class IDocumentService(ABC):
    """Common interface for both the Proxy and the Real Manager."""
    
    @abstractmethod
    def upload_document(self, doc: Document) -> None:
        pass

    @abstractmethod
    def download_document(self, doc_id: str) -> Document:
        pass

class RealDocumentManager(IDocumentService):
    """The core business logic that handles actual document storage."""
    
    def __init__(self):
        # In-memory dictionary to act as our "database"
        self._storage: Dict[str, bytes] = {}
    
    def upload_document(self, doc: Document) -> None:
        self._storage[doc.doc_id] = doc.payload
        print(f"[Storage] Document '{doc.doc_id}' successfully saved.")

    def download_document(self, doc_id: str) -> Document:
        if doc_id not in self._storage:
            raise FileNotFoundError(f"Document '{doc_id}' not found.")
        return Document(doc_id, self._storage[doc_id])

class SecurityProxy(IDocumentService):
    """Proxy that intercepts requests to enforce security before delegation."""
    
    def __init__(self, real_manager: RealDocumentManager):
        self._real_manager = real_manager

    def _scan_for_malicious_content(self, payload: bytes) -> bool:
        """Simulates macro/script scanning. Rejects files containing 'malware'."""
        bad_signature = b"malware"
        if bad_signature in payload.lower():
            return False
        return True

    def upload_document(self, doc: Document) -> None:
        """Intercepts upload to scan content before delegating to Real Manager."""
        is_safe = self._scan_for_malicious_content(doc.payload)
        
        # Only upload if the document passes the security scan
        if is_safe:
            self._real_manager.upload_document(doc)
        else:
            raise PermissionError("Upload blocked: Malicious content detected.")

    def download_document(self, doc_id: str) -> Document:
        return self._real_manager.download_document(doc_id)