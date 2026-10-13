import re

LOG_LINES = 400
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

STAGES = [
    ("extract", "Reading"),
    ("media", "Images and audio"),
    ("split", "Splitting"),
    ("tokenize", "Tokenization"),
    ("embed", "Embedding"),
    ("write", "Saving"),
]
STAGE_INDEX = {key: i for i, (key, _) in enumerate(STAGES)}
STAGE_LABELS = dict(STAGES)


class BuildProgress:
    PATTERNS = [
        (re.compile(r"Extracting documents"), "stage", "extract"),
        (re.compile(r"Extracted ([\d,]+) documents"), "documents", None),
        (re.compile(r"Processing any (audio transcripts|images)"), "stage", "media"),
        (re.compile(r"Splitting documents into chunks"), "stage", "split"),
        (re.compile(r"Split into ([\d,]+) chunks"), "chunks", None),
        (re.compile(r"Computing vectors"), "stage", "tokenize"),
        (re.compile(r"Running forward pass on (\d+) pre-padded batches"), "batches", None),
        (re.compile(r"Forward pass: (\d+)/(\d+) batches"), "batch", None),
        (re.compile(r"Forward pass complete"), "embedded", None),
        (re.compile(r"Creating TileDB array|Writing TileDB array|Write attempt"), "stage", "write"),
        (re.compile(r"Database created\. Total time"), "stage", "done"),
    ]

    def __init__(self):
        self.stage = "start"
        self.documents = None
        self.chunks = None
        self.batches = None
        self.batch = None
        self.log = []

    def feed(self, line):
        line = ANSI.sub("", line).replace("\r", " ").strip()
        if not line:
            return False
        self.log.append(line)
        if len(self.log) > LOG_LINES:
            del self.log[: len(self.log) - LOG_LINES]
        for pattern, kind, value in self.PATTERNS:
            match = pattern.search(line)
            if not match:
                continue
            if kind == "stage":
                self.advance(value)
            elif kind == "documents":
                self.documents = int(match.group(1).replace(",", ""))
            elif kind == "chunks":
                self.chunks = int(match.group(1).replace(",", ""))
            elif kind == "batches":
                self.advance("embed")
                self.batches = int(match.group(1))
                self.batch = 0
            elif kind == "batch":
                self.batch, self.batches = int(match.group(1)), int(match.group(2))
            elif kind == "embedded" and self.batches:
                self.batch = self.batches
            return True
        return False

    def advance(self, stage):
        if stage == "done" or STAGE_INDEX.get(stage, -1) >= STAGE_INDEX.get(self.stage, -1):
            self.stage = stage

    def state(self):
        current = STAGE_INDEX.get(self.stage, -1)
        if self.stage == "done":
            current = len(STAGES)
        return {
            "stage": self.stage,
            "stages": [
                {"key": key, "label": label,
                 "status": "done" if i < current else "running" if i == current else "pending"}
                for i, (key, label) in enumerate(STAGES)
            ],
            "documents": self.documents,
            "chunks": self.chunks,
            "batches": self.batches,
            "batch": self.batch,
            "line": self.log[-1] if self.log else "",
        }
