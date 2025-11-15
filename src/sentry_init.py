"""
Sentry Initialization — Error tracking and monitoring for AEGIS
"""

import os


def init_sentry() -> None:
    """
    Initialize Sentry for AEGIS.
    Reads DSN + environment from environment variables.
    """
    dsn = os.getenv("SENTRY_DSN")
    environment = os.getenv("SENTRY_ENVIRONMENT", "daytona-aegis")

    if not dsn:
        print("[SENTRY] DSN not found. Skipping Sentry initialization.")
        return

    try:
        import sentry_sdk

        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            send_default_pii=True,
            traces_sample_rate=1.0,   # capture all traces (important for hackathon)
        )

        print(f"[SENTRY] ✓ Initialized for environment: {environment}")

    except ImportError:
        print("[SENTRY] ⚠️  sentry-sdk not installed, skipping initialization")
    except Exception as e:
        print(f"[SENTRY] ❌ Initialization failed: {e}")
