import io
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

_PROTOCOL_STDOUT = sys.stdout
sys.stdout = sys.stderr

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "vectordb-plugin"
SERVER_VERSION = "1.0.0"

CONTEXTS = 5
SIMILARITY = 0.7

TOOLS = [
    {
        "name": "vectordb_list_databases",
        "description": (
            "List the vector databases available on this machine. Returns each "
            "database's name, the embedding model it was built with, and its chunk "
            "size. Call this before vectordb_search so you know which database "
            "names are valid."
        ),
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "vectordb_search",
        "description": (
            "Search a vector database for passages relevant to a question and return "
            "the best matching excerpts from the user's own documents. Use this "
            "whenever the user asks about the contents of their documents, files, or "
            "a topic they have stored locally. Returns up to "
            f"{CONTEXTS} excerpts with the source file name and a similarity score."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "database_name": {
                    "type": "string",
                    "description": "Name of the database to search, as reported by vectordb_list_databases.",
                },
                "query": {
                    "type": "string",
                    "description": "What to look for, written as a natural-language question or topic.",
                },
            },
            "required": ["database_name", "query"],
        },
    },
]


def _text_result(text):
    return {"content": [{"type": "text", "text": text}], "isError": False}


def _error_result(text):
    return {"content": [{"type": "text", "text": text}], "isError": True}


def tool_list_databases():
    from core.config import reload_config

    config = reload_config()
    names = config.get_user_databases()
    if not names:
        return _text_result(
            "No vector databases have been created yet. The user needs to create one "
            "in the VectorDB Plugin application before it can be searched."
        )

    lines = []
    for name in names:
        info = config.created_databases[name]
        lines.append(f"- {name} (embedding model: {info.model}, chunk size: {info.chunk_size})")
    return _text_result("Available vector databases:\n" + "\n".join(lines))


def tool_search(arguments):
    database_name = (arguments.get("database_name") or "").strip()
    query = (arguments.get("query") or "").strip()

    if not database_name:
        return _error_result("database_name is required.")
    if not query:
        return _error_result("query is required.")

    from core.config import reload_config

    config = reload_config()
    available = config.get_user_databases()
    if database_name not in available:
        listed = ", ".join(available) if available else "none"
        return _error_result(
            f"No database named '{database_name}'. Available databases: {listed}."
        )

    from db.database_interactions import get_query_db

    db = get_query_db(database_name)
    contexts, metadata_list = db.search(
        query,
        k=CONTEXTS,
        score_threshold=SIMILARITY,
    )

    if not contexts:
        return _text_result(
            f"No passages in '{database_name}' matched that query closely enough."
        )

    blocks = []
    for i, (text, meta) in enumerate(zip(contexts, metadata_list), 1):
        source = meta.get("file_name") or meta.get("file_path") or "unknown source"
        score = meta.get("similarity_score")
        header = f"[{i}] {source}"
        if isinstance(score, (int, float)):
            header += f" (similarity {score:.3f})"
        blocks.append(f"{header}\n{text}")

    return _text_result(
        f"{len(blocks)} passage(s) from '{database_name}':\n\n" + "\n\n".join(blocks)
    )


def dispatch(request):
    method = request.get("method", "")
    request_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        }

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        params = request.get("params") or {}
        name = params.get("name", "")
        arguments = params.get("arguments") or {}
        try:
            if name == "vectordb_list_databases":
                result = tool_list_databases()
            elif name == "vectordb_search":
                result = tool_search(arguments)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {name}"},
                }
        except Exception as e:
            import traceback

            traceback.print_exc(file=sys.stderr)
            result = _error_result(f"{type(e).__name__}: {e}")
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}

    if request_id is None:
        return None

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def send(message):
    _PROTOCOL_STDOUT.write(json.dumps(message) + "\n")
    _PROTOCOL_STDOUT.flush()


def main():
    stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
    print(f"[{SERVER_NAME}] ready, project root {PROJECT_ROOT}", file=sys.stderr)

    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            send({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            })
            continue

        response = dispatch(request)
        if response is not None:
            send(response)


if __name__ == "__main__":
    main()
