import os
import logging
import warnings
import yaml
import math
import tqdm
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from pathlib import Path
from langchain_community.docstore.document import Document
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    Docx2txtLoader,
    TextLoader,
    EverNoteLoader,
    UnstructuredEPubLoader,
    UnstructuredEmailLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    UnstructuredRTFLoader,
    UnstructuredODTLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader
)

from constants import DOCUMENT_LOADERS
from extract_metadata import extract_document_metadata
from utilities import my_cprint
import traceback

datasets_logger = logging.getLogger('datasets')
datasets_logger.setLevel(logging.WARNING)

logging.getLogger("transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger().setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(filename)s:%(lineno)d - %(message)s'
)

ROOT_DIRECTORY = Path(__file__).parent
SOURCE_DIRECTORY = ROOT_DIRECTORY / "Docs_for_DB"
INGEST_THREADS = max(4, os.cpu_count() - 4)

for ext, loader_name in DOCUMENT_LOADERS.items():
    DOCUMENT_LOADERS[ext] = globals()[loader_name]

def load_single_document(file_path: Path) -> Document:
    '''
    loads a single document file using the appropriate loader based on its file
    extension, extracts metadata, and returns a Document object.
    '''
    file_extension = file_path.suffix.lower()
    loader_class = DOCUMENT_LOADERS.get(file_extension)

    if not loader_class:
        raise ValueError(f"Document type for extension {file_extension} is undefined")

    loader_options = {}

    if file_extension in [".epub", ".rtf", ".odt", ".md", ".html"]:
        loader_options.update({"mode": "single", "strategy": "fast"})
    elif file_extension in [".xlsx", ".xlsd"]:
        loader_options.update({"mode": "single"})
    elif file_extension in [".csv", ".txt"]:
        loader_options.update({
            "encoding": "utf-8",
            "autodetect_encoding": True
        })

    loader = loader_class(str(file_path), **loader_options)

    document = loader.load()[0]

    # Extract and update metadata
    metadata = extract_document_metadata(file_path)
    document.metadata.update(metadata)
    
    print(f"Loaded---> {file_path.name}")
    
    return document

def load_document_batch(filepaths, threads_per_process):
    '''
    takes a batch of file paths and uses multi-threading to load multiple documents concurrently,
    returning a list of loaded Document objects and their corresponding file paths.
    '''
    with ThreadPoolExecutor(threads_per_process) as exe:
        futures = [exe.submit(load_single_document, name) for name in filepaths]
        data_list = [future.result() for future in futures]
    return (data_list, filepaths)

def load_documents(source_dir: Path) -> list:
    '''
    scans a source directory for supported document types, divides the workload among multiple processes, and
    uses the loadDocumentBatch function to efficiently load all documents in parallel.
    '''
    all_files = list(source_dir.iterdir())
    doc_paths = [f for f in all_files if f.suffix.lower() in (key.lower() for key in DOCUMENT_LOADERS.keys())]
    
    docs = []

    if doc_paths:
        n_workers = min(INGEST_THREADS, max(len(doc_paths), 1))
        
        total_cores = os.cpu_count()
        max_threads = max(4, total_cores - 8)
        threads_per_process = 1
        
        with ProcessPoolExecutor(n_workers) as executor:
            chunksize = math.ceil(len(doc_paths) / n_workers)
            futures = []
            for i in range(0, len(doc_paths), chunksize):
                chunk_paths = doc_paths[i:i + chunksize]
                futures.append(executor.submit(load_document_batch, chunk_paths, threads_per_process))
            
            for future in as_completed(futures):
                contents, _ = future.result()
                docs.extend(contents)
    
    return docs

def split_documents(documents):
    '''
    Uses a RecursiveCharacterTextSplitter from Langchain to split the input documents into smaller chunks
    '''
    with open("config.yaml", "r", encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
        chunk_size = config["database"]["chunk_size"]
        chunk_overlap = config["database"]["chunk_overlap"]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    for i, doc in enumerate(documents):
        if not isinstance(doc.page_content, str):
            documents[i].page_content = str(doc.page_content)
    
    print(f"\nSplitting {len(documents)} documents.")
    texts = text_splitter.split_documents(documents)
    print(f"Created {len(texts)} chunks.")
    
    return texts