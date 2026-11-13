import socket
import threading
import time
import uvicorn
import webview

from app.main import app


def get_available_port():
    # Find an available local port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_server(port, timeout=30):
    # Wait until the local server is ready
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.2)

    return False


def main():
    port = get_available_port()

    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    )

    # Start FastAPI in the background
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    # Wait for FastAPI to start
    if not wait_for_server(port):
        server.should_exit = True
        raise RuntimeError("The application server could not be started.")

    # Enable file downloads
    webview.settings["ALLOW_DOWNLOADS"] = True

    # Open the desktop application window
    webview.create_window(
        "Lost and Found Management System",
        f"http://127.0.0.1:{port}/dashboard",
        width=1200,
        height=800,
        min_size=(900, 600),
    )

    try:
        webview.start()
    finally:
        # Stop FastAPI when the window closes
        server.should_exit = True
        server_thread.join(timeout=5)


if __name__ == "__main__":
    main()
