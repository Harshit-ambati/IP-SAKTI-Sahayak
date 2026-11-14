"""Route modules for IP-SAKTI Sahayak backend."""
from .health import router as health_router
from .classify import router as classify_router
from .answer import router as answer_router
from .sources import router as sources_router
from .referral import router as referral_router

__all__ = [
    "health_router",
    "classify_router",
    "answer_router",
    "sources_router",
    "referral_router",
]
