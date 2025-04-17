import gc
import json
import logging
from pathlib import Path
import torch
import yaml
import requests
import sseclient
from PySide6.QtCore import QThread, Signal, QObject

from database_interactions import QueryVectorDB
from utilities import format_citations, normalize_chat_text
from constants import rag_string

ROOT_DIRECTORY = Path(__file__).resolve().parent

contexts_output_file_path = ROOT_DIRECTORY / "contexts.txt"
metadata_output_file_path = ROOT_DIRECTORY / "metadata.txt"

class KoboldSignals(QObject):
    response_signal = Signal(str)
    error_signal = Signal(str)
    finished_signal = Signal()
    citation_signal = Signal(str)

class KoboldChat:
    def __init__(self):
        self.signals = KoboldSignals()
        self.config = self.load_configuration()
        self.query_vector_db = None
        self.api_url = "http://localhost:5001/api/extra/generate/stream"

    def load_configuration(self):
        with open('config.yaml', 'r') as config_file:
            return yaml.safe_load(config_file)

    def connect_to_kobold(self, augmented_query):
        payload = {
            "prompt": augmented_query,
            "max_context_length": 4096,
            "max_length": 512,
            "temperature": 0.1,
            "top_p": 0.9,
            "rep_pen": 1.1,
            # "opmode": 0,
            # "stop_sequence": []
            # "bypass_eos": True
            # "use_default_badwordsids": True
        }

        try:
            logging.debug(f"Sending request to Kobold API with prompt length: {len(augmented_query)} characters")
            response = requests.post(self.api_url, json=payload, stream=True)
            logging.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()

            client = sseclient.SSEClient(response)
            full_response = ""

            for event in client.events():
                if event.event == "message":
                    try:
                        data = json.loads(event.data)
                        if 'token' in data:
                            token = data['token']
                            logging.debug(f"Received token: '{token}', finish_reason: {data.get('finish_reason')}")
                            # Directly emit the signal
                            self.signals.response_signal.emit(token)
                            full_response += token
                        else:
                            logging.warning(f"Event has no token: {data}")
                    except json.JSONDecodeError:
                        logging.error(f"Failed to parse JSON: {event.data}")
                else:
                    logging.debug(f"Received non-message event: {event.event}")

            return full_response
        except Exception as e:
            logging.error(f"Error in Kobold API request: {str(e)}")
            self.signals.error_signal.emit(f"API error: {str(e)}")
            raise

    def handle_response_and_cleanup(self, full_response, metadata_list):
        citations = format_citations(metadata_list)

        if self.query_vector_db:
            self.query_vector_db.cleanup()
            # print("Embedding model removed from memory.")

        if torch.cuda.empty_cache():
            torch.cuda.empty_cache()
        gc.collect()

        return citations

    def save_metadata_to_file(self, metadata_list):
        with metadata_output_file_path.open('w', encoding='utf-8') as output_file:
            for metadata in metadata_list:
                output_file.write(f"{metadata}\n")

    def ask_kobold(self, query, selected_database):
        if self.query_vector_db is None or self.query_vector_db.selected_database != selected_database:
            self.query_vector_db = QueryVectorDB(selected_database)

        contexts, metadata_list = self.query_vector_db.search(query)

        self.save_metadata_to_file(metadata_list)

        if not contexts:
            self.signals.error_signal.emit("No relevant contexts found.")
            self.signals.finished_signal.emit()
            return

        prepend_string = "Only base your answer on the provided context/contexts. If you cannot, please state so."
        augmented_query = f"{prepend_string}\n\n---\n\n" + "\n\n---\n\n".join(contexts) + f"\n\n-----\n\n{query}"
        print(augmented_query)

        # Instead of using a generator, get the full response directly
        try:
            full_response = self.connect_to_kobold(augmented_query)
            
            with open('chat_history.txt', 'w', encoding='utf-8') as f:
                normalized_response = normalize_chat_text(full_response)
                f.write(normalized_response)

            self.signals.response_signal.emit("\n")

            citations = self.handle_response_and_cleanup(full_response, metadata_list)
            self.signals.citation_signal.emit(citations)
        except Exception as e:
            self.signals.error_signal.emit(f"Error: {str(e)}")
        finally:
            self.signals.finished_signal.emit()

class KoboldThread(QThread):
    def __init__(self, query, selected_database):
        super().__init__()
        self.query = query
        self.selected_database = selected_database
        self.kobold_chat = KoboldChat()

    def run(self):
        try:
            self.kobold_chat.ask_kobold(self.query, self.selected_database)
        except Exception as e:
            logging.error(f"Error in KoboldThread: {str(e)}")
            self.kobold_chat.signals.error_signal.emit(str(e))