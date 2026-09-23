"""Optional local tracing configuration for Foundry Toolkit."""

import os


def configure_local_observability() -> None:
    """Enable local OpenTelemetry export when explicitly requested."""
    if os.getenv("ENABLE_LOCAL_TRACING", "false").lower() != "true":
        return

    from agent_framework.observability import configure_otel_providers

    capture_content = os.getenv("OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "false").lower() == "true"
    configure_otel_providers(
        vs_code_extension_port=4317,
        enable_sensitive_data=capture_content,
    )
