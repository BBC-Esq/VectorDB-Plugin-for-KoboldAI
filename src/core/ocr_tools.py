from pathlib import Path

from modules.ocr import process_documents

OCR_ENGINES = {
    "RapidOCR": "rapidocr",
}


def ocr_output_path(pdf_path):
    original_file = Path(pdf_path)
    return original_file.with_stem(f"{original_file.stem}_OCR").with_suffix(".pdf")


def run_ocr(pdf_path, backend):
    try:
        events = process_documents(
            pdf_paths=Path(pdf_path),
            backend=backend,
        )
        return True, None, events if isinstance(events, dict) else {}
    except Exception as e:
        return False, str(e), {}


def ocr_staged_pdfs(on_start=None, on_result=None, should_stop=None):
    from core.databases import find_pdfs_needing_ocr
    from core.staging import DOCS_DIR, remove_staged_file, stage_files

    pdfs = find_pdfs_needing_ocr(DOCS_DIR)
    converted = 0
    for index, link in enumerate(pdfs, 1):
        if should_stop is not None and should_stop():
            break
        source = link.resolve()
        if on_start is not None:
            on_start(index, len(pdfs), source)
        ok, error, events = run_ocr(source, OCR_ENGINES["RapidOCR"])
        output = ocr_output_path(source)
        if ok and output.exists():
            remove_staged_file(link.name)
            stage_files([str(output)])
            converted += 1
        else:
            output = None
            error = error or "no output was written"
        if on_result is not None:
            on_result(index, len(pdfs), source, output, error, events)
    return len(pdfs), converted


def _page_list(pages, limit=10):
    shown = ", ".join(str(p) for p in pages[:limit])
    return shown + ", ..." if len(pages) > limit else shown


def summarize_ocr_events(events):
    events = events or {}
    def entries(key):
        return [e for e in events.get(key, []) if isinstance(e, dict)]
    def pages(items):
        return sorted({e.get('page') for e in items if e.get('page')})
    warnings, infos = [], []
    lc = pages(entries('lowconf'))
    if lc:
        warnings.append(f"{len(lc)} low-confidence page(s): {_page_list(lc)} (worth a manual review)")
    nt = entries('notext')
    nt_sus = pages([e for e in nt if e.get('ink_frac', 0) >= 0.002])
    nt_blank = pages([e for e in nt if e.get('ink_frac', 0) < 0.002])
    if nt_sus:
        warnings.append(f"{len(nt_sus)} page(s) with visible content but no OCR text: {_page_list(nt_sus)}")
    if nt_blank:
        infos.append(f"{len(nt_blank)} blank page(s): {_page_list(nt_blank)}")
    pe = pages(entries('pageerror'))
    if pe:
        warnings.append(f"{len(pe)} page(s) failed OCR (image kept, no text layer): {_page_list(pe)}")
    mm = pages(entries('datamismatch'))
    if mm:
        warnings.append(f"{len(mm)} page(s) with inconsistent OCR data (partial text kept): {_page_list(mm)}")
    for e in entries('verifyfail'):
        warnings.append(f"verification: {e.get('msg', 'output verification warning')}")
    for e in entries('fileerror'):
        warnings.append(f"file failed: {e.get('error', 'unknown error')}")
    orp = pages(entries('oriented'))
    if orp:
        infos.append(f"{len(orp)} page(s) auto-rotated to read: {_page_list(orp)}")
    return warnings, infos
