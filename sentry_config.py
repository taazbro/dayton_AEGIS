import os
import sentry_sdk


def init_sentry():
    """
    Initialize Sentry for AEGIS.
    Reads DSN + environment from .env for cleaner hackathon setup.
    """
    dsn = os.getenv("SENTRY_DSN")
    environment = os.getenv("SENTRY_ENVIRONMENT", "daytona-aegis")

    if not dsn:
        print("[SENTRY] DSN not found. Skipping Sentry initialization.")
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        send_default_pii=True,
        traces_sample_rate=1.0,   # capture all traces (important for hackathon)
    )

    print(f"[SENTRY] Initialized for environment: {environment}")
