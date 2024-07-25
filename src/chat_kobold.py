import json
from pathlib import Path
import requests
import logging
import sseclient
from PySide6.QtCore import QThread, Signal, QObject
from database_interactions import QueryVectorDB

ROOT_DIRECTORY = Path(__file__).resolve().parent
contexts_output_file_path = ROOT_DIRECTORY / "contexts.txt"
metadata_output_file_path = ROOT_DIRECTORY / "metadata.txt"

class KoboldSignals(QObject):
    response_signal = Signal(str)
    error_signal = Signal(str)
    finished_signal = Signal()
    citation_signal = Signal(str)

class KoboldAPIWorker(QThread):
    def __init__(self, url, payload):
        super().__init__()
        self.url = url
        self.payload = payload
        self.signals = KoboldSignals()

    def run(self):
        try:
            response = requests.post(self.url, json=self.payload, stream=True)
            response.raise_for_status()
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.event == "message":
                    try:
                        data = json.loads(event.data)
                        if 'token' in data:
                            logging.debug(f"Received token: {data['token']}")
                            self.signals.response_signal.emit(data['token'])  # Corrected this line
                        else:
                            logging.warning(f"Unexpected data format: {data}")
                    except json.JSONDecodeError:
                        logging.error(f"Failed to parse JSON: {event.data}")
                        self.signals.error_signal.emit(f"Failed to parse: {event.data}")  # Corrected this line
                else:
                    logging.info(f"Received non-message event: {event.event}")
        except Exception as e:
            logging.error(f"Error in API request: {str(e)}")
            self.signals.error_signal.emit(str(e))  # Corrected this line
        finally:
            self.signals.finished_signal.emit()

class KoboldChat:
    def __init__(self):
        self.signals = KoboldSignals()
        self.api_url = "http://localhost:5001/api/extra/generate/stream"
        self.query_vector_db = None

    def ask_kobold(self, query, chunks_only, selected_database):
        logging.debug(f"ask_kobold called with query: {query}, chunks_only: {chunks_only}, selected_database: {selected_database}")
        
        if self.query_vector_db is None or self.query_vector_db.selected_database != selected_database:
            logging.debug(f"Initializing QueryVectorDB with database: {selected_database}")
            self.query_vector_db = QueryVectorDB(selected_database)

        contexts, metadata_list = self.query_vector_db.search(query)
        logging.debug(f"Retrieved {len(contexts)} contexts from vector database")
        
        if chunks_only:
            logging.debug("Chunks only mode, displaying contexts")
            self.display_chunks(contexts, metadata_list)
            self.signals.finished_signal.emit()
            return

        prepend_string = "Only base your answer on the provided context/contexts. If you cannot, please state so."
        augmented_query = f"{prepend_string}\n\n---\n\n" + "\n\n---\n\n".join(contexts) + f"\n\n-----\n\n{query}"
        logging.debug(f"Augmented query: {augmented_query[:100]}...") # Log first 100 characters of augmented query

        payload = {
            "prompt": augmented_query,
            "max_context_length": 4096,
            "max_length": 512,
            "temperature": 0.1,
            "top_p": 0.9,
            "rep_pen": 1.1
        }

        logging.debug("Creating KoboldAPIWorker")
        self.worker = KoboldAPIWorker(self.api_url, payload)
        self.worker.signals.response_signal.connect(self.on_response_received)
        self.worker.signals.error_signal.connect(self.signals.error_signal.emit)
        self.worker.signals.finished_signal.connect(self.on_response_finished)
        logging.debug("Starting Kobold API worker")
        self.worker.start()

        self.metadata_list = metadata_list  # Store for citation use later
        logging.debug("ask_kobold method completed")

    def on_response_received(self, token):
        logging.debug(f"Response received in KoboldChat: {token}")
        self.signals.response_signal.emit(token)

    def display_chunks(self, contexts, metadata_list):
        formatted_chunks = self.format_chunks(contexts, metadata_list)
        self.signals.response_signal.emit(formatted_chunks)

    def format_chunks(self, contexts, metadata_list):
        formatted_chunks = ""
        for i, (context, metadata) in enumerate(zip(contexts, metadata_list), 1):
            formatted_chunks += f"---------- Context {i} | From File: {metadata.get('file_name', 'Unknown')} ----------\n\n{context}\n\n"
        return formatted_chunks

    def on_response_finished(self):
        self.signals.citation_signal.emit(self.format_citations(self.metadata_list))
        self.signals.finished_signal.emit()

    def format_citations(self, metadata_list):
        return "\n".join([Path(metadata['file_path']).name for metadata in metadata_list])

class KoboldChatThread(QThread):
    def __init__(self, query, chunks_only, selected_database):
        super().__init__()
        self.query = query
        self.chunks_only = chunks_only
        self.selected_database = selected_database
        self.kobold_chat = KoboldChat()

    def run(self):
        logging.debug("KoboldChatThread started running")
        try:
            self.kobold_chat.ask_kobold(self.query, self.chunks_only, self.selected_database)
        except Exception as e:
            logging.error(f"Error in KoboldChatThread: {str(e)}")
            self.kobold_chat.signals.error_signal.emit(str(e))