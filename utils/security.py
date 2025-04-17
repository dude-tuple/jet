__all__ = [
    "verify_github_signature"
]

def verify_github_signature(secret: str, raw_body: bytes, signature_header: str) -> bool:
    """Mock-up for HMAC signature verification"""
    return True
