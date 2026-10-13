import io
import json
import os
import re
import sys
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

_PROTOCOL_STDOUT = sys.stdout
sys.stdout = sys.stderr

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "vectordb-plugin"
SERVER_VERSION = "1.1.0"

SEARCH_TIMEOUT = 150
IDLE_RELEASE_SECONDS = 600
REPEAT_WINDOW_SECONDS = 180
MAX_PASSAGES = 20

_request_lock = threading.Lock()
_search_service = None
_last_search = 0.0
_recent_searches = {}


def build_tools():
    from core.downloads import language_guidance, vector_models
    from core.settings import MAX_CHUNK_SIZE, MIN_CHUNK_SIZE, build_chunking, current_settings

    guidance = " ".join(language_guidance())
    default_passages = current_settings()["contexts"]
    default_chunk_size, default_overlap = build_chunking()
    return [
        {
            "name": "vectordb_list_databases",
            "description": (
                "List the vector databases on this computer: each database's name, the embedding model it was "
                "built with and whether that model suits English or multilingual text, and how many files it "
                "holds. It also shows a database that is still being created. Call this before vectordb_search "
                "so you use a valid database name. Takes no parameters."
            ),
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "vectordb_search",
            "description": (
                "Search one of the user's vector databases and return the passages from their own files that "
                "best match a question, each labeled with its source file name. Use it whenever the user asks "
                "about the contents of their documents. Parameters: database_name (required) is a name from "
                "vectordb_list_databases; query (required) is the question or topic in plain words; passages "
                f"(optional) is how many passages to return, from 1 to {MAX_PASSAGES}. Only include passages when "
                "the user asks for a specific number of passages, results or excerpts; otherwise leave it out and "
                f"{default_passages} are returned. Base your answer on the returned passages and name the files you "
                "used. If they don't answer the question, search once more with different words, or tell the user "
                "the documents don't seem to cover it. Repeating the exact same search returns no new passages."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "database_name": {
                        "type": "string",
                        "description": "Name of the database to search, as listed by vectordb_list_databases.",
                    },
                    "query": {
                        "type": "string",
                        "description": "The question or topic to look for, in plain words.",
                    },
                    "passages": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": MAX_PASSAGES,
                        "description": f"How many passages to return. Only set it when the user asks for a specific "
                                       f"number; otherwise leave it out and {default_passages} are returned.",
                    },
                },
                "required": ["database_name", "query"],
            },
        },
        {
            "name": "vectordb_create_database",
            "description": (
                "Create a new vector database from files and folders on this computer so they can be searched "
                "with vectordb_search. Only do this when the user asks. It runs in the background and returns "
                "right away; large folders can take a long time, so check vectordb_build_status and tell the "
                "user how it is going. Parameters: database_name (required) is a new name of at least 3 "
                "characters using only lowercase letters, numbers, hyphens and underscores. paths (required) is "
                "a list of full paths to files or folders, for example [\"C:\\\\Users\\\\Name\\\\Documents\\\\Cases\"]; "
                "folders include all their subfolders. embedding_model (optional) should match the language of "
                f"the documents. {guidance} If it is left out, the model used last time is used. chunk_size "
                f"(optional) is how many characters go in each chunk, from {MIN_CHUNK_SIZE} to {MAX_CHUNK_SIZE}; "
                "only include it when the user asks for a particular chunk size, otherwise leave it out and the "
                f"default of {default_chunk_size} is used. Neighboring chunks always overlap by half the chunk size. "
                "ocr_scanned_pdfs (optional, true or false) first makes scanned PDFs that have no text "
                "searchable, saving a searchable copy named NAME_OCR.pdf next to each one; ask the user before "
                "using it. clear_waiting_files (optional, true or false) removes files left waiting from an "
                "earlier session; only use it after the user agrees."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "database_name": {
                        "type": "string",
                        "description": "New database name: at least 3 lowercase letters, numbers, hyphens or underscores.",
                    },
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Full paths to the files or folders to add. Folders include their subfolders.",
                    },
                    "embedding_model": {
                        "type": "string",
                        "enum": [m["name"] for m in vector_models()],
                        "description": f"Embedding model that suits the documents' language. {guidance}",
                    },
                    "chunk_size": {
                        "type": "integer",
                        "minimum": MIN_CHUNK_SIZE,
                        "maximum": MAX_CHUNK_SIZE,
                        "description": f"Characters in each chunk. Only set it when the user asks for a particular "
                                       f"chunk size; otherwise leave it out and {default_chunk_size} is used. "
                                       f"Neighboring chunks overlap by half of it ({default_overlap} by default).",
                    },
                    "ocr_scanned_pdfs": {
                        "type": "boolean",
                        "description": "Make scanned PDFs searchable first by saving NAME_OCR.pdf copies next to them.",
                    },
                    "clear_waiting_files": {
                        "type": "boolean",
                        "description": "Remove files left waiting from an earlier session before adding these.",
                    },
                },
                "required": ["database_name", "paths"],
            },
        },
        {
            "name": "vectordb_build_status",
            "description": (
                "Report the progress of a database that is being created, or the result of the last one: the "
                "current step, how far along it is, and any files that could not be added. Parameter: "
                "database_name (optional); leave it out to get the database being created now or the most "
                "recent one."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "database_name": {"type": "string", "description": "Name of the database to report on."},
                },
                "required": [],
            },
        },
        {
            "name": "vectordb_cancel_build",
            "description": (
                "Stop creating a database that is still being built and remove its partial files. Only use "
                "this when the user asks to stop. Parameter: database_name (required)."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "database_name": {"type": "string", "description": "Name of the database to stop creating."},
                },
                "required": ["database_name"],
            },
        },
    ]


def _text_result(text):
    return {"content": [{"type": "text", "text": text}], "isError": False}


def _error_result(text):
    return {"content": [{"type": "text", "text": text}], "isError": True}


def _count(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        number = float(str(value).strip())
    except ValueError:
        return None
    return int(number) if number >= 1 else None


def _flag(value):
    if isinstance(value, str):
        return value.strip().lower() in ("true", "yes", "1", "on")
    return bool(value)


def search_service():
    global _search_service
    if _search_service is None:
        from db.search_process import SearchService

        _search_service = SearchService(timeout=SEARCH_TIMEOUT)
    return _search_service


def release_search():
    if _search_service is not None:
        _search_service.release()


def _idle_release_loop():
    while True:
        time.sleep(30)
        if _search_service is None or _search_service.database is None:
            continue
        if time.monotonic() - _last_search < IDLE_RELEASE_SECONDS:
            continue
        if not _request_lock.acquire(blocking=False):
            continue
        try:
            release_search()
            print(f"[{SERVER_NAME}] released the idle search process", file=sys.stderr)
        except Exception as e:
            print(f"[{SERVER_NAME}] could not release the search process: {e}", file=sys.stderr)
        finally:
            _request_lock.release()


def tool_list_databases():
    from core.build_jobs import describe_status, running_job
    from core.constants import WIKI_DATABASE
    from core.databases import database_files, list_databases
    from core.downloads import model_language, vector_model_for_path

    lines = []
    for name, info in sorted(list_databases().items()):
        model = vector_model_for_path(info.get("model"))
        if model:
            model_text = f"{model['name']} ({model_language(model)})"
        else:
            model_text = Path(info["model"]).name if info.get("model") else "unknown model"
        files = database_files(name)
        count = f"{len({f for f, _ in files})} file(s)" if files is not None else "its files are missing"
        about = " (the KoboldCpp wiki, KoboldCpp's own documentation)" if name == WIKI_DATABASE else ""
        lines.append(f"- {name}{about}: {model_text}, {count}")
    running = running_job()
    text = ("Databases:\n" + "\n".join(lines)) if lines else "There are no vector databases yet."
    if running is not None:
        text += "\n\nStill being created: " + describe_status(running)
    return _text_result(text)


def tool_search(arguments):
    global _last_search
    database_name = (arguments.get("database_name") or "").strip()
    query = (arguments.get("query") or "").strip()
    if not database_name:
        return _error_result("database_name is required.")
    if not query:
        return _error_result("query is required.")

    from core.build_jobs import job_is_running, read_status
    from core.databases import list_databases, missing_model_problem
    from core.settings import current_settings

    available = sorted(list_databases())
    if database_name not in available:
        status = read_status(database_name)
        if status is not None and job_is_running(status):
            return _error_result(f"'{database_name}' is still being created. Check vectordb_build_status.")
        listed = ", ".join(available) if available else "none"
        return _error_result(f"No database named '{database_name}'. Available databases: {listed}.")
    problem = missing_model_problem(database_name)
    if problem:
        return _error_result(problem)

    settings = current_settings()
    requested = _count(arguments.get("passages"))
    passages = min(requested, MAX_PASSAGES) if requested else settings["contexts"]
    options = {"k": passages, "score_threshold": settings["similarity"], "search_term": "", "document_types": ""}
    key = (database_name, query, passages, settings["similarity"])
    now = time.monotonic()
    for old_key, stamp in list(_recent_searches.items()):
        if now - stamp > REPEAT_WINDOW_SECONDS:
            del _recent_searches[old_key]
    if key in _recent_searches:
        return _text_result(
            f"You already searched '{database_name}' for exactly \"{query}\" moments ago, so this would return the "
            "same passages again. Answer from the passages you already have, or search with different words. If "
            "those passages are no longer in the conversation, search again with slightly different wording."
        )
    _last_search = time.monotonic()
    contexts, metadata_list = search_service().search(database_name, query, options)
    _last_search = time.monotonic()
    _recent_searches[key] = _last_search
    if not contexts:
        return _text_result(f"No passages in '{database_name}' matched that query closely enough. "
                            "Try rephrasing it or searching for more specific words.")
    blocks = []
    for index, (text, meta) in enumerate(zip(contexts, metadata_list), 1):
        source = meta.get("file_name") or meta.get("file_path") or "unknown source"
        cleaned = re.sub(r"\n\s*\n\s*\n*", "\n\n", re.sub(r"\n[ \t]+\n", "\n\n", text).strip())
        blocks.append(f"[{index}] {source}\n{cleaned}")
    limit_note = ""
    if requested and requested > MAX_PASSAGES:
        limit_note = f"(A search returns at most {MAX_PASSAGES} passages, so {MAX_PASSAGES} are shown instead of {requested}.)\n\n"
    return _text_result(limit_note + f"{len(blocks)} passage(s) from '{database_name}':\n\n" + "\n\n".join(blocks))


def tool_create_database(arguments):
    from core.build_jobs import start_build_job

    paths = arguments.get("paths")
    if paths is None and arguments.get("path"):
        paths = [arguments["path"]]
    chunk_size = arguments.get("chunk_size")
    release_search()
    plan = start_build_job(
        arguments.get("database_name") or "",
        paths,
        embedding_model=(arguments.get("embedding_model") or "").strip() or None,
        ocr_scanned_pdfs=_flag(arguments.get("ocr_scanned_pdfs")),
        clear_waiting_files=_flag(arguments.get("clear_waiting_files")),
        chunk_size=None if chunk_size in (None, "") else chunk_size,
    )
    model = plan["model"]
    text = f"Started creating '{plan['name']}' from {plan['files']} file(s) with {model['name']}"
    if plan["download"]:
        text += f", which will be downloaded first (about {model['size_mb']} MB)"
    text += (f", using {plan['chunk_size']}-character chunks that overlap by {plan['chunk_overlap']}. "
             "It runs in the background; check its progress with vectordb_build_status.")
    if plan["unsupported"]:
        text += f" {plan['unsupported']} file(s) of types this program can't read will be skipped."
    return _text_result(text)


def tool_build_status(arguments):
    from core.build_jobs import status_report

    return _text_result(status_report((arguments.get("database_name") or "").strip() or None))


def tool_cancel_build(arguments):
    from core.build_jobs import request_cancel

    database_name = (arguments.get("database_name") or "").strip()
    if not database_name:
        return _error_result("database_name is required.")
    return _text_result(request_cancel(database_name))


TOOL_HANDLERS = {
    "vectordb_list_databases": lambda arguments: tool_list_databases(),
    "vectordb_search": tool_search,
    "vectordb_create_database": tool_create_database,
    "vectordb_build_status": tool_build_status,
    "vectordb_cancel_build": tool_cancel_build,
}

TOOLS = []


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
        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Unknown tool: {name}"},
            }
        try:
            result = handler(arguments)
        except (ValueError, RuntimeError, FileNotFoundError) as e:
            result = _error_result(str(e))
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
    global TOOLS
    from core.environment import prepare_process

    prepare_process()
    from core.wiki import install_wiki

    install_wiki()
    TOOLS = build_tools()
    threading.Thread(target=_idle_release_loop, daemon=True).start()
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

        with _request_lock:
            response = dispatch(request)
        if response is not None:
            send(response)
    release_search()


if __name__ == "__main__":
    main()
