import argparse
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

ORIGINAL_CWD = Path.cwd()
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from core.constants import MAX_CHUNK_SIZE, MIN_CHUNK_SIZE

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff"}
DOCUMENT_TYPES = ("document", "image", "audio")
BUILD_SETTINGS = {"embedding-model", "vision-model", "chunk-size", "create-device", "half", "pipeline"}

EXAMPLES = """examples:
  python cli.py models
  python cli.py create my-notes C:\\Notes --model yuan
  python cli.py search my-notes "When is the filing deadline?"
  python cli.py databases

Run "python cli.py COMMAND --help" for the options of a command."""


def out(text=""):
    print(text, flush=True)


def warn(text):
    print(text, file=sys.stderr, flush=True)


def fail(message, code=1):
    warn(f"Error: {message}")
    return code


def emit_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False), flush=True)


def display_width(text):
    return sum(2 if unicodedata.east_asian_width(char) in ("W", "F") else 1 for char in text)


def table(headers, rows):
    rows = [[str(cell) for cell in row] for row in rows]
    widths = [max(display_width(row[i]) for row in [headers] + rows) for i in range(len(headers))]

    def line(cells):
        return "  ".join(cell + " " * (width - display_width(cell)) for cell, width in zip(cells, widths)).rstrip()

    return "\n".join([line(headers)] + [line(row) for row in rows])


def user_path(text):
    path = Path(text).expanduser()
    return path if path.is_absolute() else ORIGINAL_CWD / path


def format_seconds(seconds):
    if seconds < 60:
        return f"{seconds:.1f} s"
    minutes, seconds = divmod(int(round(seconds)), 60)
    if minutes < 60:
        return f"{minutes} min {seconds} s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours} h {minutes} min"


def score(value):
    return value if isinstance(value, (int, float)) else None


def clean_passage(text):
    text = re.sub(r"\n[ \t]+\n", "\n\n", text)
    return re.sub(r"\n\s*\n\s*\n*", "\n\n", text.strip())


def int_between(low, high):
    def parse(text):
        try:
            value = int(text)
        except ValueError:
            raise argparse.ArgumentTypeError("must be a whole number") from None
        if not low <= value <= high:
            raise argparse.ArgumentTypeError(f"must be between {low} and {high}")
        return value
    return parse


def fraction(text):
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a number from 0 to 1") from None
    if not 0.0 <= value <= 1.0:
        raise argparse.ArgumentTypeError("must be a number from 0 to 1")
    return value


def configure_output():
    if sys.platform == "win32":
        import ctypes

        kernel32 = ctypes.windll.kernel32
        for handle_id in (-11, -12):
            handle = kernel32.GetStdHandle(handle_id)
            mode = ctypes.c_uint()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    for stream in (sys.stdout, sys.stderr):
        try:
            if stream.isatty():
                stream.reconfigure(errors="replace")
            else:
                stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def download_model(model):
    from core.downloads import ModelDownloader

    out(f"Downloading {model['name']} (about {model['size_mb']} MB)...")
    ModelDownloader(model, "vector").download()
    out(f"{model['name']} is ready.")


def stage_paths(paths, recursive):
    from core.staging import collect_files, stage_files

    selection = collect_files([user_path(p) for p in paths])
    files = selection.top_level + (selection.nested if recursive else [])
    made, errors = stage_files(files) if files else (0, [])
    already = len(files) - made - len(errors)
    out(f"Added {made} file(s)." + (f" {already} were already in the list." if already else ""))
    if selection.unsupported:
        out(f"Skipped {len(selection.unsupported)} file(s) of a type this program can't read.")
    if selection.nested and not recursive:
        out(f"{len(selection.nested)} more file(s) are in subfolders; add --recursive to include them.")
    for path in selection.missing:
        warn(f"Not found: {path}")
    for error in errors:
        warn(error)
    return not selection.missing and not errors


class BuildPrinter:
    def __init__(self, verbose):
        from core.build_progress import BuildProgress

        self.verbose = verbose
        self.progress = BuildProgress()
        self.stage = None
        self.documents = None
        self.chunks = None
        self.last_batch_report = 0.0

    def __call__(self, line):
        from core.build_progress import STAGE_LABELS

        self.progress.feed(line)
        if self.verbose:
            out(line)
            return
        progress = self.progress
        if progress.stage != self.stage and progress.stage in STAGE_LABELS:
            self.stage = progress.stage
            out(f"{STAGE_LABELS[progress.stage]}...")
        if progress.documents and progress.documents != self.documents:
            self.documents = progress.documents
            out(f"  {progress.documents} document(s) read")
        if progress.chunks is not None and progress.chunks != self.chunks:
            self.chunks = progress.chunks
            out(f"  {progress.chunks} chunk(s)")
        if progress.stage == "embed" and progress.batches and progress.batch and progress.batch < progress.batches:
            now = time.monotonic()
            if now - self.last_batch_report >= 5:
                self.last_batch_report = now
                out(f"  {progress.batch}/{progress.batches} batches")


def cmd_models(args):
    from core.downloads import (
        is_vector_model_downloaded, language_guidance, model_language, models_by_language, vector_model_for_path,
    )
    from core.settings import read_config

    english, multilingual = models_by_language()
    models = english + multilingual
    current = vector_model_for_path(read_config().get("EMBEDDING_MODEL_NAME"))
    selected = current["name"] if current else None
    if args.json:
        emit_json([{
            "name": m["name"],
            "best_for": model_language(m).lower(),
            "repo_id": m["repo_id"],
            "size_mb": m["size_mb"],
            "dimensions": m["dimensions"],
            "max_sequence": m["max_sequence"],
            "english_retrieval": score(m.get("english_retrieval")),
            "multilingual_retrieval": score(m.get("multilingual_retrieval")),
            "legal_retrieval": score(m.get("rteb_legal")),
            "downloaded": is_vector_model_downloaded(m),
            "selected": m["name"] == selected,
        } for m in models])
        return 0
    rows = [[("* " if m["name"] == selected else "  ") + m["name"], model_language(m).capitalize(),
             f"{m['size_mb']} MB", m["dimensions"], "yes" if is_vector_model_downloaded(m) else "no"] for m in models]
    out(table(["  MODEL", "BEST FOR", "SIZE", "DIMENSIONS", "DOWNLOADED"], rows))
    out()
    for line in language_guidance():
        out(line)
    if selected:
        out(f"\n* New databases use {selected}.")
    return 0


def cmd_download(args):
    from core.downloads import is_vector_model_downloaded, resolve_vector_model

    model = resolve_vector_model(args.model)
    if is_vector_model_downloaded(model) and not args.force:
        out(f"{model['name']} is already downloaded.")
        return 0
    download_model(model)
    return 0


def cmd_add(args):
    from core.locks import exclusive

    with exclusive("adding files"):
        ok = stage_paths(args.paths, args.recursive)
    return 0 if ok else 1


def cmd_staged(args):
    from core.staging import DOCS_DIR, staged_files

    names = staged_files()
    if args.json:
        emit_json([{"name": name, "source": str((DOCS_DIR / name).resolve())} for name in names])
        return 0
    if not names:
        out("No files are waiting to be added.")
        return 0
    for name in names:
        out(name)
    out(f"\n{len(names)} file(s) will go into the next database.")
    return 0


def cmd_unstage(args):
    from core.locks import exclusive
    from core.staging import clear_staged_files, remove_staged_file, staged_files

    if not args.all and not args.names:
        return fail("Name the files to remove, or use --all.")
    with exclusive("removing files from the list"):
        if args.all:
            out(f"Removed {clear_staged_files()} file(s) from the list.")
            return 0
        staged = set(staged_files())
        missing = [name for name in args.names if name not in staged]
        failed = [name for name in args.names if name in staged and not remove_staged_file(name)]
    out(f"Removed {len(args.names) - len(missing) - len(failed)} file(s) from the list.")
    for name in missing:
        warn(f"Not in the list: {name}")
    for name in failed:
        warn(f"Could not remove: {name}")
    return 1 if missing or failed else 0


def cmd_create(args):
    from core.databases import DatabaseBuild, check_preconditions_for_db_creation, database_name_problem
    from core.downloads import (
        is_vector_model_downloaded, language_guidance, model_directory, resolve_vector_model, vector_model_for_path,
    )
    from core.initialize import prepare
    from core.locks import exclusive
    from core.settings import build_chunking, change_setting, current_settings, read_config, set_embedding_model
    from core.staging import staged_files

    problem = database_name_problem(args.name)
    if problem:
        return fail(problem)
    with exclusive(f"creating the database '{args.name}'"):
        prepare()
        if args.model:
            model = resolve_vector_model(args.model)
        else:
            model = vector_model_for_path(read_config().get("EMBEDDING_MODEL_NAME"))
            if model is None:
                for line in language_guidance():
                    warn(line)
                return fail("Choose an embedding model with --model.")
        if not is_vector_model_downloaded(model):
            download_model(model)
        set_embedding_model(model_directory(model))
        if args.device is not None:
            change_setting("create-device", args.device)
        if args.half is not None:
            change_setting("half", "on" if args.half else "off")
        if args.vision_model is not None:
            change_setting("vision-model", args.vision_model)
        if args.paths and not stage_paths(args.paths, args.recursive):
            return 1
        count = len(staged_files())
        if not count:
            return fail("No files are waiting to be added. Pass files or folders to create, "
                        "or add them first with 'python cli.py add'.")
        ok, message, pdfs = check_preconditions_for_db_creation(PROJECT_ROOT, args.name, skip_ocr=args.skip_ocr_check)
        if not ok:
            if pdfs:
                warn("These PDFs have no text layer:")
                for pdf in pdfs:
                    warn(f"  {Path(pdf).name}")
                return fail("Run 'python cli.py ocr --staged' to make them searchable, or add --skip-ocr-check "
                            "to create the database without their text.")
            return fail(message)
        settings = current_settings()
        chunk_size, chunk_overlap = build_chunking(args.chunk_size)
        out(f"Creating '{args.name}' from {count} file(s) with {model['name']} "
            f"(chunk size {chunk_size}, overlap {chunk_overlap}, {settings['create-device']})...")
        printer = BuildPrinter(args.verbose)
        started = time.monotonic()
        result = DatabaseBuild(args.name, chunk_size=args.chunk_size).run(printer)
        elapsed = time.monotonic() - started
    if result.success:
        chunks = printer.progress.chunks
        out(f"Created '{args.name}' from {count} file(s) in {format_seconds(elapsed)}"
            + (f" ({chunks} chunk(s))." if chunks is not None else "."))
        if result.not_added:
            out(f"{len(result.not_added)} file(s) were not fully added:")
            for entry in result.not_added:
                out(f"  {entry}")
        return 0
    if result.cancelled:
        warn(result.message)
        return 130
    if not args.verbose:
        warn("Last lines of the build log:")
        for line in printer.progress.log[-15:]:
            warn(f"  {line}")
    return fail(result.message)


def cmd_databases(args):
    from core.databases import database_files, list_databases
    from core.downloads import vector_model_for_path

    entries = []
    for name, info in sorted(list_databases().items()):
        files = database_files(name)
        model = vector_model_for_path(info.get("model"))
        entries.append({
            "name": name,
            "model": model["name"] if model else (Path(info["model"]).name if info.get("model") else None),
            "chunk_size": info.get("chunk_size"),
            "chunk_overlap": info.get("chunk_overlap"),
            "files": len({f for f, _ in files}) if files is not None else None,
        })
    if args.json:
        emit_json(entries)
        return 0
    if not entries:
        out("There are no databases yet. Create one with: python cli.py create NAME FOLDER --model MODEL")
        return 0
    out(table(["DATABASE", "MODEL", "CHUNK SIZE", "OVERLAP", "FILES"],
              [[e["name"], e["model"] or "?", e["chunk_size"], e["chunk_overlap"],
                "missing" if e["files"] is None else e["files"]] for e in entries]))
    return 0


def cmd_files(args):
    from core.databases import database_files, list_databases

    if args.database not in list_databases():
        return fail(f"There is no database called '{args.database}'.")
    files = database_files(args.database)
    if files is None:
        return fail(f"The files of '{args.database}' are missing from the Vector_DB folder.")
    files = sorted(set(files), key=lambda item: (str(item[0]).lower(), str(item[1])))
    if args.json:
        emit_json([{"file_name": name, "file_path": path} for name, path in files])
        return 0
    out(table(["FILE", "PATH"], files))
    out(f"\n{len(files)} file(s) in '{args.database}'.")
    return 0


def cmd_search(args):
    from core.databases import list_databases, missing_model_problem, search_database
    from core.initialize import prepare
    from core.settings import current_settings

    prepare()
    if args.database not in list_databases():
        return fail(f"There is no database called '{args.database}'.")
    problem = missing_model_problem(args.database)
    if problem:
        return fail(problem)
    results = search_database(args.database, args.query, contexts=args.contexts, similarity=args.similarity,
                              contains=args.contains or "", document_type=args.type or "")
    if args.json:
        emit_json(results)
        return 0
    if not results:
        threshold = args.similarity if args.similarity is not None else current_settings()["similarity"]
        out(f"No passages scored at least {threshold}. Try a lower --similarity or different wording.")
        return 0
    for index, result in enumerate(results, 1):
        found = f" (score {result['score']:.3f})" if isinstance(result["score"], (int, float)) else ""
        out(f"[{index}] {result['file_name']}{found}")
        out(clean_passage(result["text"]))
        out()
    return 0


def cmd_delete(args):
    from core.constants import WIKI_DATABASE
    from core.databases import VECTOR_DB_DIR, delete_database, list_databases
    from core.locks import exclusive

    name = args.database
    if name not in list_databases() and not (VECTOR_DB_DIR / name).is_dir():
        return fail(f"There is no database called '{name}'.")
    if not args.yes:
        if not sys.stdin.isatty():
            return fail("Add --yes to confirm deleting a database.")
        answer = input(f"Delete the database '{name}'? This cannot be undone. [y/N] ")
        if answer.strip().lower() not in ("y", "yes"):
            out("Nothing was deleted.")
            return 0
    with exclusive(f"deleting the database '{name}'"):
        deleted = delete_database(name)
    if not deleted:
        return fail(f"Some files of '{name}' could not be deleted. If KoboldCpp is running with this program's "
                    "MCP server, close KoboldCpp and delete the database again.")
    out(f"Deleted the database '{name}'.")
    if name == WIKI_DATABASE:
        out("It came with this program and won't be put back. To get it again, run: python cli.py wiki update")
    return 0


def report_ocr(path, output, error, events, seconds):
    from core.ocr_tools import summarize_ocr_events

    if output is None:
        warn(f"  OCR failed for {path.name}: {error}")
        return
    warnings, infos = summarize_ocr_events(events)
    out(f"  Saved {output} ({format_seconds(seconds)})")
    for item in warnings:
        out(f"  Warning: {item}")
    for item in infos:
        out(f"  {item}")


def ocr_pdf(path):
    from core.ocr_tools import OCR_ENGINES, ocr_output_path, run_ocr

    out(f"Reading text from {path.name}...")
    started = time.monotonic()
    ok, error, events = run_ocr(path, OCR_ENGINES["RapidOCR"])
    output = ocr_output_path(path)
    if not ok or not output.exists():
        output, error = None, error or "no output was written"
    report_ocr(path, output, error, events, time.monotonic() - started)
    return output


def cmd_ocr(args):
    from core.databases import find_pdfs_needing_ocr

    if args.staged == bool(args.paths):
        return fail("Name PDF files or folders, or use --staged, but not both.")
    if args.staged:
        from core.locks import exclusive
        from core.ocr_tools import ocr_staged_pdfs

        timer = {}

        def on_start(index, total, source):
            out(f"Reading text from {source.name} ({index} of {total})...")
            timer["started"] = time.monotonic()

        def on_result(index, total, source, output, error, events):
            report_ocr(source, output, error, events, time.monotonic() - timer["started"])
            if output is not None:
                out(f"  The list now has {output.name} instead of {source.name}.")

        with exclusive("making the staged PDFs searchable"):
            total, converted = ocr_staged_pdfs(on_start=on_start, on_result=on_result)
        if not total:
            out("None of the staged PDFs need OCR.")
        return 1 if converted < total else 0
    targets, problems = [], []
    for raw in args.paths:
        path = user_path(raw)
        if path.is_dir():
            found = find_pdfs_needing_ocr(path)
            if not found:
                out(f"No PDFs in {path} need OCR.")
            targets.extend(found)
        elif path.is_file() and path.suffix.lower() == ".pdf":
            targets.append(path)
        else:
            problems.append(raw)
    for raw in problems:
        warn(f"Not a PDF file or folder: {raw}")
    failures = sum(ocr_pdf(path) is None for path in targets)
    return 1 if failures or problems else 0


def cmd_status(args):
    from core.build_jobs import status_report

    out(status_report(args.database))
    return 0


def cmd_cancel(args):
    from core.build_jobs import read_status, request_cancel
    from core.locks import current_operation

    status = read_status(args.database)
    holder = current_operation()
    if status is None and holder and f"'{args.database}'" in holder.get("operation", ""):
        return fail(f"'{args.database}' is being created from the command line. Press Ctrl+C in that window to stop it.")
    out(request_cancel(args.database))
    return 0


def match_name(text, names, kind):
    wanted = text.strip().lower()
    for name in names:
        if name.lower() == wanted:
            return name
    matches = [name for name in names if wanted in name.lower()]
    if len(matches) == 1:
        return matches[0]
    if matches:
        raise ValueError(f"'{text}' matches more than one {kind}: {', '.join(matches)}.")
    raise ValueError(f"There is no {kind} called '{text}'.")


def cmd_transcribe(args):
    from core.utilities import usable_whisper_models

    models = usable_whisper_models()
    if args.list_models:
        for name in models:
            out(name)
        return 0
    if not args.files:
        return fail("Name at least one audio file, or use --list-models.")
    model = models[0] if args.model is None else match_name(args.model, models, "Whisper model usable here")
    paths = [user_path(f) for f in args.files]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        return fail("Not found: " + ", ".join(missing))
    from core.initialize import check_for_necessary_folders
    from core.locks import exclusive
    from core.staging import staged_files
    from modules.transcribe import WhisperTranscriber

    check_for_necessary_folders()
    with exclusive("transcribing audio"):
        for path in paths:
            out(f"Transcribing {path.name} with {model}...")
            before = set(staged_files())
            started = time.monotonic()
            WhisperTranscriber(model_key=model, batch_size=args.batch_size).start_transcription_process(str(path))
            new = sorted(set(staged_files()) - before)
            out(f"  Done in {format_seconds(time.monotonic() - started)}. "
                + (f"The transcript {new[0]} will go into the next database." if new
                   else "The transcript in the list was updated."))
    return 0


def cmd_vision(args):
    from core.constants import VISION_MODELS
    from core.settings import read_config
    from core.utilities import runs_on_this_hardware

    chosen = (read_config().get("vision") or {}).get("chosen_model")
    entries = [{
        "name": name,
        "selected": name == chosen,
        "size": info.get("size"),
        "vram": info.get("vram"),
        "needs_gpu": bool(info.get("requires_cuda")),
        "works_here": runs_on_this_hardware(info),
        "average_description_characters": info.get("avg_length"),
    } for name, info in VISION_MODELS.items()]
    if args.json:
        emit_json(entries)
        return 0
    out(table(["  MODEL", "SIZE", "VRAM", "NEEDS GPU", "WORKS HERE", "AVG DESCRIPTION"],
              [[("* " if e["selected"] else "  ") + e["name"], e["size"], e["vram"], "yes" if e["needs_gpu"] else "no",
                "yes" if e["works_here"] else "no", f"{e['average_description_characters']} characters"]
               for e in entries]))
    out("\n* Describes the images in new databases. Change it with: python cli.py settings vision-model NAME")
    return 0


def print_report(path):
    try:
        out(Path(path).read_text(encoding="utf-8").rstrip())
    finally:
        os.unlink(path)


def cmd_vision_compare(args):
    from core.constants import VISION_MODELS
    from core.settings import resolve_vision_model
    from core.utilities import runs_on_this_hardware
    from core.vision_benchmark import compare_models_on_image, write_comparison_report

    image = user_path(args.image)
    if not image.is_file():
        return fail(f"Not found: {image}")
    if image.suffix.lower() not in IMAGE_SUFFIXES:
        return fail("Choose a .png, .jpg, .jpeg, .bmp, .gif, .tif or .tiff image.")
    if args.models:
        names = list(dict.fromkeys(resolve_vision_model(name) for name in args.models))
    else:
        names = [name for name, info in VISION_MODELS.items() if runs_on_this_hardware(info)]
    unusable = [name for name in names if not runs_on_this_hardware(VISION_MODELS[name])]
    if unusable:
        return fail(f"{', '.join(unusable)} needs a supported NVIDIA GPU, which this computer does not have.")
    results = compare_models_on_image(image, names)
    print_report(write_comparison_report(image, results))
    return 0


def cmd_vision_preview(args):
    from core.constants import VISION_MODELS
    from core.settings import read_config
    from core.staging import staged_files
    from core.utilities import fallback_if_unavailable, runs_on_this_hardware
    from core.vision_benchmark import summarize_documents, write_folder_report

    images = [name for name in staged_files() if Path(name).suffix.lower() in IMAGE_SUFFIXES]
    if not images:
        out("No images are waiting to be added.")
        return 0
    default = next(name for name, info in VISION_MODELS.items() if runs_on_this_hardware(info))
    chosen = fallback_if_unavailable((read_config().get("vision") or {}).get("chosen_model"), VISION_MODELS, default)
    out(f"Describing {len(images)} image(s) with {chosen}...")
    from modules.process_images import choose_image_loader

    documents, seconds = choose_image_loader({"vision": {"chosen_model": chosen}}, return_timing=True)
    print_report(write_folder_report(summarize_documents(documents), seconds, chosen))
    return 0


def cmd_settings(args):
    from core.settings import SETTINGS, change_setting, current_settings

    if args.key is None:
        values = current_settings()
        if args.json:
            emit_json(values)
            return 0
        out(table(["SETTING", "VALUE", "MEANING"],
                  [[key, "-" if values[key] is None else values[key], SETTINGS[key]] for key in SETTINGS]))
        out('\nChange one with: python cli.py settings SETTING VALUE')
        return 0
    if args.key == "chunk-overlap":
        return fail("The chunk overlap is always half the chunk size, so change chunk-size instead.")
    if args.key not in SETTINGS:
        return fail(f"There is no setting called '{args.key}'. Settings: {', '.join(SETTINGS)}.")
    if args.value is None:
        value = current_settings()[args.key]
        out("-" if value is None else str(value))
        return 0
    if args.key in ("create-device", "search-device"):
        from core.initialize import prepare

        prepare()
    if args.key == "embedding-model":
        from core.downloads import is_vector_model_downloaded, resolve_vector_model

        model = resolve_vector_model(args.value)
        if not is_vector_model_downloaded(model):
            return fail(f"{model['name']} has not been downloaded yet. Download it with: "
                        f"python cli.py download {model['name']}")
    if args.key in BUILD_SETTINGS:
        from core.locks import exclusive

        with exclusive("changing settings"):
            value = change_setting(args.key, args.value)
    else:
        value = change_setting(args.key, args.value)
    out(f"{args.key} is now {value}.")
    return 0


def mask(token):
    return f"{token[:4]}...{token[-4:]}" if len(token) > 12 else "hidden"


def cmd_token(args):
    from core.settings import clear_hf_token, read_config, set_hf_token

    if args.action == "set":
        if sys.stdin.isatty():
            import getpass

            token = getpass.getpass("Hugging Face access token (typing is hidden): ")
        else:
            token = sys.stdin.readline()
        set_hf_token(token)
        out("Saved your Hugging Face access token.")
        return 0
    if args.action == "clear":
        clear_hf_token()
        out("Cleared the saved Hugging Face access token.")
        return 0
    saved = (read_config().get("hf_access_token") or "").strip()
    environment = (os.environ.get("HF_TOKEN") or "").strip()
    if saved:
        out(f"A Hugging Face access token is saved ({mask(saved)}).")
    elif environment:
        out(f"No token is saved, so the one in the HF_TOKEN environment variable ({mask(environment)}) is used.")
    else:
        out("No Hugging Face access token is set. The models this program offers are public, so one is optional.")
    return 0


def cmd_wiki(args):
    from core.constants import WIKI_DATABASE, WIKI_MODEL, WIKI_ZIP
    from core.downloads import is_vector_model_downloaded, resolve_vector_model
    from core.initialize import prepare
    from core.wiki import (
        digest, download_wiki, installed_wiki_info, saved_wiki, update_wiki, wiki_changes, wiki_database_exists,
    )

    prepare()
    installed = installed_wiki_info()
    if installed is not None:
        out(f"'{WIKI_DATABASE}' holds the KoboldCpp wiki as downloaded on {str(installed.get('downloaded'))[:10]}.")
    out("Downloading the current KoboldCpp wiki...")
    text = download_wiki()
    current = installed is not None and installed.get("sha256") == digest(text)
    if installed is not None and not current:
        added, removed = wiki_changes(saved_wiki(), text)
        out(f"The wiki has changed since then: {added} line(s) added and {removed} removed.")
    if args.action != "update":
        if current:
            out(f"'{WIKI_DATABASE}' is up to date.")
        elif installed is not None:
            out("Update it with: python cli.py wiki update")
        elif wiki_database_exists():
            out(f"'{WIKI_DATABASE}' doesn't record which version of the wiki it holds. "
                "Rebuild it with: python cli.py wiki update")
        else:
            out(f"'{WIKI_DATABASE}' isn't installed. Create it with: python cli.py wiki update")
        return 0
    if current and WIKI_ZIP.exists() and not args.force:
        out(f"'{WIKI_DATABASE}' is already up to date.")
        return 0
    model = resolve_vector_model(WIKI_MODEL)
    if not is_vector_model_downloaded(model):
        download_model(model)
    out(f"{'Rebuilding' if wiki_database_exists() else 'Creating'} '{WIKI_DATABASE}' with {model['name']}...")
    printer = BuildPrinter(args.verbose)
    started = time.monotonic()
    try:
        update_wiki(text, printer)
    except RuntimeError:
        if printer.progress.log and not args.verbose:
            warn("Last lines of the build log:")
            for line in printer.progress.log[-15:]:
                warn(f"  {line}")
        raise
    chunks = printer.progress.chunks
    out(f"'{WIKI_DATABASE}' now holds the current KoboldCpp wiki"
        + (f" ({chunks} chunks)" if chunks is not None else "") + f". Took {format_seconds(time.monotonic() - started)}.")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="python cli.py",
        description="Create and search vector databases of your own documents for KoboldCpp.",
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    commands = parser.add_subparsers(dest="command", metavar="COMMAND", title="commands")

    def command(name, handler, summary, description=None):
        sub = commands.add_parser(name, help=summary, description=description or summary)
        sub.set_defaults(handler=handler)
        return sub

    sub = command("models", cmd_models, "List the embedding models and whether each suits English or multilingual documents")
    sub.add_argument("--json", action="store_true", help="print the list as JSON")

    sub = command("download", cmd_download, "Download an embedding model")
    sub.add_argument("model", help="model name, or a unique part of it such as 'yuan'")
    sub.add_argument("--force", action="store_true", help="download again even if it is already downloaded")

    sub = command("add", cmd_add, "Add files or folders to the list of files for the next database")
    sub.add_argument("paths", nargs="+", metavar="PATH", help="file or folder")
    sub.add_argument("--recursive", action="store_true", help="include files in subfolders")

    sub = command("staged", cmd_staged, "Show the files waiting to go into the next database")
    sub.add_argument("--json", action="store_true", help="print the list as JSON")

    sub = command("unstage", cmd_unstage, "Remove files from the list without deleting the originals")
    sub.add_argument("names", nargs="*", metavar="NAME", help="file name as shown by 'staged'")
    sub.add_argument("--all", action="store_true", help="empty the list")

    sub = command("create", cmd_create, "Create a database from the files in the list",
                  "Create a database from the files in the list, plus any files or folders given here. "
                  "--chunk-size applies to this database only; the other options are saved as the new defaults.")
    sub.add_argument("name", help="new database name: lowercase letters, numbers, - and _")
    sub.add_argument("paths", nargs="*", metavar="PATH", help="files or folders to add first")
    sub.add_argument("--recursive", action="store_true", help="include files in subfolders of the folders given")
    sub.add_argument("--model", help="embedding model, downloaded first if needed (see 'models')")
    sub.add_argument("--chunk-size", type=int_between(MIN_CHUNK_SIZE, MAX_CHUNK_SIZE),
                     help="characters in each chunk of this database (default: setting 'chunk-size'); "
                          "chunks always overlap by half of it")
    sub.add_argument("--device", choices=["cpu", "cuda"], help="device that creates the database")
    sub.add_argument("--half", action=argparse.BooleanOptionalAction, help="use half precision on the GPU")
    sub.add_argument("--vision-model", help="vision model that describes images (see 'vision')")
    sub.add_argument("--skip-ocr-check", action="store_true", help="don't check whether PDFs need OCR first")
    sub.add_argument("--verbose", action="store_true", help="show the full build log")

    sub = command("databases", cmd_databases, "List the databases")
    sub.add_argument("--json", action="store_true", help="print the list as JSON")

    sub = command("files", cmd_files, "List the files in a database")
    sub.add_argument("database", help="database name")
    sub.add_argument("--json", action="store_true", help="print the list as JSON")

    sub = command("search", cmd_search, "Search a database and print the best matching passages")
    sub.add_argument("database", help="database name")
    sub.add_argument("query", help="question or topic to look for")
    sub.add_argument("--contexts", type=int_between(1, 1000), help="most passages to return (default: setting 'contexts')")
    sub.add_argument("--similarity", type=fraction, help="lowest score, 0 to 1, to return (default: setting 'similarity')")
    sub.add_argument("--contains", help="only return passages that contain this text")
    sub.add_argument("--type", choices=DOCUMENT_TYPES, help="only return passages from this kind of file")
    sub.add_argument("--json", action="store_true", help="print the results as JSON")

    sub = command("delete", cmd_delete, "Delete a database")
    sub.add_argument("database", help="database name")
    sub.add_argument("--yes", action="store_true", help="don't ask for confirmation")

    sub = command("status", cmd_status, "Show the progress or result of creating a database from KoboldCpp",
                  "Show the progress of a database being created, including ones started from KoboldCpp, or the "
                  "result of the most recent one.")
    sub.add_argument("database", nargs="?", help="database name (default: the current or most recent one)")

    sub = command("cancel", cmd_cancel, "Stop creating a database that was started from KoboldCpp")
    sub.add_argument("database", help="database name")

    sub = command("ocr", cmd_ocr, "Make scanned PDFs searchable with RapidOCR",
                  "Make scanned PDFs searchable with RapidOCR. Each PDF gets a searchable copy next to it named "
                  "NAME_OCR.pdf. Folders are searched for PDFs that have no text layer.")
    sub.add_argument("paths", nargs="*", metavar="PATH", help="PDF file or folder")
    sub.add_argument("--staged", action="store_true",
                     help="process the PDFs in the list that need OCR and put the searchable copies in the list instead")

    sub = command("transcribe", cmd_transcribe, "Transcribe audio files and add the transcripts to the list",
                  "Transcribe audio files with Whisper. Each transcript goes into the list of files for the next database.")
    sub.add_argument("files", nargs="*", metavar="AUDIO", help="audio file")
    sub.add_argument("--model", help="Whisper model, or a unique part of its name (default: the first one listed)")
    sub.add_argument("--batch-size", type=int_between(1, 150), default=8, help="audio segments processed at once (default: 8)")
    sub.add_argument("--list-models", action="store_true", help="list the Whisper models usable on this computer")

    sub = command("vision", cmd_vision, "List the vision models that describe images in new databases")
    sub.add_argument("--json", action="store_true", help="print the list as JSON")

    sub = command("vision-compare", cmd_vision_compare, "Describe one image with each vision model to compare them")
    sub.add_argument("image", help="image file")
    sub.add_argument("--models", nargs="+", metavar="MODEL", help="vision models to compare (default: all that work here)")

    command("vision-preview", cmd_vision_preview, "Describe the images in the list with the chosen vision model")

    sub = command("settings", cmd_settings, "Show or change settings",
                  "Show all settings, show one setting, or change one.")
    sub.add_argument("key", nargs="?", metavar="SETTING", help="setting to show or change")
    sub.add_argument("value", nargs="?", metavar="VALUE", help="new value")
    sub.add_argument("--json", action="store_true", help="print the settings as JSON")

    sub = command("token", cmd_token, "Show, set or clear the Hugging Face access token",
                  "Show whether a Hugging Face access token is set, or set or clear it. 'set' asks for the token "
                  "without showing it, or reads it from standard input.")
    sub.add_argument("action", nargs="?", choices=["set", "clear"], help="omit to show the status")

    sub = command("wiki", cmd_wiki, "Check or update the kobold_wiki database of the KoboldCpp wiki",
                  "Download the KoboldCpp wiki and say whether the kobold_wiki database still matches it. "
                  "'update' rebuilds the database when the wiki has changed, along with the copy in the wiki "
                  "folder that ships with the program.")
    sub.add_argument("action", nargs="?", choices=["update"], help="omit to only check")
    sub.add_argument("--force", action="store_true", help="rebuild even if the wiki hasn't changed")
    sub.add_argument("--verbose", action="store_true", help="show the full build log")

    return parser


def main(argv=None):
    configure_output()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "handler", None):
        parser.print_help()
        return 0
    from core.environment import prepare_process

    prepare_process()
    from core.downloads import DownloadError
    from core.locks import BusyError

    try:
        return args.handler(args)
    except (BusyError, DownloadError, FileNotFoundError, RuntimeError, ValueError) as e:
        return fail(str(e))
    except KeyboardInterrupt:
        warn("Stopped.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
