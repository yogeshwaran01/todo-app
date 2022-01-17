import argparse
from http.server import HTTPServer
from api.server import Server


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        type=int,
        help="port to run",
        default=8000,
    )
    args = parser.parse_args()
    port = args.port
    hostname = "localhost"
    webServer = HTTPServer((hostname, port), Server)
    print(f"Server started http://{hostname}:{port}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
