from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os.path
from .database import Database

DATABASE_URI = os.path.expanduser("~") + "/.todo-app.json"

db = Database(DATABASE_URI)

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        url_string = self.url(self.path)
        parser_result = urlparse(url_string)
        queries = parse_qs(parser_result.query)
        self.send_response(200)
        self.send_header("Content-Type", "Application/JSON")
        self.end_headers()
        self.path = parser_result.path
        if self.path == "/todos":
            self.wfile.write(bytes(json.dumps(db.all_documents()), encoding="utf-8"))
        elif self.path == "/delete":
            id = queries.get("id")[0]
            db.delete_document_by_id(id)
            db.commit()
            self.wfile.write(bytes(json.dumps({"msg": "ok"}), encoding="utf-8"))
        elif self.path == "/done":
            id = queries.get("id")[0]
            req = db.get_document_by_id(id)
            req["is_done"] = True
            db.data.update({id: req})
            db.commit()
            self.wfile.write(bytes(json.dumps({"msg": "ok"}), encoding="utf-8"))
        elif self.path == "/undone":
            id = queries.get("id")[0]
            req = db.get_document_by_id(id)
            req["is_done"] = False
            db.data.update({id: req})
            db.commit()
            self.wfile.write(bytes(json.dumps({"msg": "ok"}), encoding="utf-8"))
        else:
            self.wfile.write(bytes(json.dumps({"msg": "bad"}), encoding="utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        content_length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(content_length)
        if self.path == "/add":
            source = json.loads(data.decode())
            task = source["task"]
            is_done = source["is_done"]
            id_ = db.add_document({"task": task, "is_done": is_done})
            db.commit()
            self.wfile.write(
                bytes(json.dumps({"msg": "ok", "id": id_}), encoding="utf-8")
            )
        else:
            self.wfile.write(bytes(json.dumps({"msg": "bad"}), encoding="utf-8"))

    def url(self, path):
        return "http://" + self.address_string() + path
