import uvicorn

from roomslot.bootstrap.app import create_app

INTERNAL_BIND_HOST = "0.0.0.0"  # nosec B104
INTERNAL_BIND_PORT = 8000


def main() -> None:
    uvicorn.run(
        app=create_app(),
        host=INTERNAL_BIND_HOST,
        port=INTERNAL_BIND_PORT,
        log_config=None,
        access_log=False,
    )


if __name__ == "__main__":
    main()
