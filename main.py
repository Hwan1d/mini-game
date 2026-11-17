import http.server
import os
import socketserver
import sys
import threading
import webbrowser

PORT = 8000
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))


class QuietSimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """요청 로그로 터미널 화면이 지저분해지지 않도록 로그를 숨기는 핸들러"""
    def log_message(self, format, *args):
        pass


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def start_web_server():
    os.chdir(SERVER_DIR)
    handler = QuietSimpleHTTPRequestHandler

    try:
        httpd = ReusableTCPServer(("", PORT), handler)
    except OSError:
        print(f"\n⚠️ 포트 {PORT}번이 이미 사용 중입니다. 기존 프로세스를 확인해주세요.\n")
        return

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    url = f"http://localhost:{PORT}"
    print(f"\n🚀 로컬 웹 서버가 시작되었습니다! ({url})")
    print("🌐 기본 브라우저를 실행합니다...")
    webbrowser.open(url)

    print("\n" + "=" * 50)
    print(f"서버 실행 중... (주소: {url})")
    print("종료하려면 0번을 누르세요.")
    print("=" * 50)

    while True:
        try:
            choice = input("입력: ").strip()
            if choice == '0':
                print("\n서버를 종료하는 중...")
                httpd.shutdown()
                httpd.server_close()
                print("로컬 웹 서버가 안전하게 종료되었습니다. 안녕히 가세요! 👋")
                sys.exit(0)
            else:
                print("종료하려면 0번을 누르세요.")
        except (KeyboardInterrupt, EOFError):
            print("\n서버를 종료하는 중...")
            httpd.shutdown()
            httpd.server_close()
            print("로컬 웹 서버가 종료되었습니다. 안녕히 가세요! 👋")
            sys.exit(0)


def main():
    while True:
        print("=" * 45)
        print("   🎮 Hwan1d 미니게임 에이전트 🎮")
        print("=" * 45)
        print("1. 2048 웹 미니게임 실행 (로컬 서버 + 브라우저)")
        print("0. 종료")
        print("-" * 45)

        try:
            choice = input("선택하세요 (0-1): ").strip()
            if choice == '1':
                start_web_server()
            elif choice == '0':
                print("\nHwan1d 미니게임 에이전트를 종료합니다. 감사합니다! 👋")
                sys.exit(0)
            else:
                print("\n⚠️ 올바른 번호를 선택해주세요. (0 또는 1)\n")
        except (KeyboardInterrupt, EOFError):
            print("\n프로그램을 종료합니다. 👋")
            sys.exit(0)


if __name__ == "__main__":
    main()
