from abc import ABC, abstractmethod
from typing import List

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
    
    def upload_document(self, doc: Document) -> None:
        # Simulate saving the document to a repository
        print(f"Document {doc.doc_id} successfully saved to repository.")

    def download_document(self, doc_id: str) -> Document:
        # Simulate retrieving a document from storage
        return Document(doc_id, b"retrieved_content")

class SecurityProxy(IDocumentService):
    """Proxy that intercepts requests to enforce security before delegation."""
    
    def __init__(self, real_manager: RealDocumentManager):
        self._real_manager = real_manager
        self._rate_limit_threshold: int = 100  # Example threshold for rate limiting

    def _scan_for_malicious_content(self, payload: bytes) -> bool:
        """Simulates macro/script scanning."""
        # Always returns True for now add real scanning logic as needed
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
        # Directly delegates download to the real manager
        return self._real_manager.download_document(doc_id)