import json
import logging
from colorama import Fore, Style, init

init(autoreset=True)

class SimpleColoredFormatter(logging.Formatter):
    """Custom logging formatter that adds colors based on log level."""
    COLORS = {
        'DEBUG': Fore.WHITE,
        'INFO': Fore.CYAN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, Fore.RESET)
        levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        return f"{levelname} {record.getMessage()}"

logger = logging.getLogger("django")
handler = logging.StreamHandler()
handler.setFormatter(SimpleColoredFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Map specific status codes to messages
STATUS_MESSAGES = {
    200: "Success ✅",
    201: "Created ✅",
    400: "Bad Request ⚠️",
    401: "Unauthorized ⚠️",
    403: "Forbidden ⚠️",
    404: "Not Found ⚠️",
    409: "Conflict ⚠️",
    422: "Unprocessable Entity ⚠️",
    500: "Server Error ❌",
    502: "Bad Gateway ❌",
    503: "Service Unavailable ❌",
}

class APILoggingMiddleware:
    """
    Logs request and response with specific HTTP status messages and colors.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log sending request
        logger.info(f"Sending Request: {request.method} {request.path}")

        # Log request body or query params
        try:
            body = request.body.decode("utf-8")
            try:
                body_json = json.loads(body) if body else {}
            except Exception:
                body_json = body
        except Exception:
            body_json = {}

        pretty_body = json.dumps(body_json, indent=4) if isinstance(body_json, dict) else str(body_json)

        if request.method in ["POST", "PUT", "PATCH"]:
            logger.info(f"Request Body:\n{Fore.CYAN}{pretty_body}{Style.RESET_ALL}")
        else:
            logger.info(f"Query Params:\n{Fore.CYAN}{json.dumps(request.GET.dict(), indent=4)}{Style.RESET_ALL}")

        # Get response
        response = self.get_response(request)
        status = response.status_code
        message = STATUS_MESSAGES.get(status, "Unknown Status")

        # Choose color based on status type
        if 200 <= status < 300:
            color = Fore.GREEN
            log_func = logger.info
        elif 400 <= status < 500:
            color = Fore.YELLOW
            log_func = logger.warning
        elif 500 <= status < 600:
            color = Fore.RED
            log_func = logger.error
        else:
            color = Fore.CYAN
            log_func = logger.info

        log_func(f"Response Status: {color}{status} - {message}{Style.RESET_ALL}")

        return response
