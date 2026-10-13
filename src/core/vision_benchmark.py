import gc
import statistics
import tempfile
import textwrap
import time
import traceback

import torch
from PIL import Image

import modules.process_images as module_process_images
from core.constants import VISION_MODELS


def _release(loader):
    if getattr(loader, 'model', None) is not None:
        loader.model.cpu()
        del loader.model
    if getattr(loader, 'tokenizer', None) is not None:
        del loader.tokenizer
    if getattr(loader, 'processor', None) is not None:
        del loader.processor


def compare_models_on_image(image_path, model_names, on_started=None, on_completed=None, on_failed=None, should_stop=None):
    results = []
    try:
        with Image.open(image_path) as raw_image:
            for i, model_name in enumerate(model_names):
                if should_stop is not None and should_stop():
                    print("\nProcessing cancelled by user")
                    torch.cuda.empty_cache()
                    gc.collect()
                    break

                if on_started:
                    on_started(i, model_name)

                try:
                    print(f"\nProcessing with {model_name}...")
                    model_config = {"vision": {"chosen_model": model_name}}

                    loader_name = VISION_MODELS[model_name]['loader']
                    loader_class = getattr(module_process_images, loader_name)
                    loader = loader_class(model_config)

                    loader.model, loader.tokenizer, loader.processor = loader.initialize_model_and_tokenizer()
                    start_time = time.time()
                    description = loader.process_single_image(raw_image)
                    process_time = time.time() - start_time
                    results.append((model_name, description, process_time))

                    _release(loader)
                    torch.cuda.empty_cache()
                    gc.collect()

                    print(f"Completed {model_name}")
                    if on_completed:
                        on_completed(i, model_name, process_time)

                except Exception as e:
                    error_msg = f"Error processing with {model_name}: {str(e)}\n{traceback.format_exc()}"
                    results.append((model_name, error_msg, 0.0))
                    print(error_msg)
                    torch.cuda.empty_cache()
                    gc.collect()
                    if on_failed:
                        on_failed(i, model_name)
    finally:
        torch.cuda.empty_cache()
        gc.collect()
    return results


def summarize_documents(documents):
    contents = []
    total_length = 0

    for doc in documents:
        if hasattr(doc, 'page_content') and hasattr(doc, 'metadata'):
            content = doc.page_content
            filepath = doc.metadata.get('source', doc.metadata.get('file_path', doc.metadata.get('file_name', 'Unknown filepath')))
        elif isinstance(doc, dict):
            content = doc.get("page_content", "Document is missing 'page_content'.")
            filepath = doc.get("metadata", {}).get('source',
                     doc.get("metadata", {}).get('file_path',
                     doc.get("metadata", {}).get('file_name', 'Unknown filepath')))
        else:
            content = "Document is missing 'page_content'."
            filepath = 'Unknown filepath'

        content_length = len(content)
        total_length += content_length
        wrapped_content = textwrap.fill(content, width=100)
        contents.append((filepath, wrapped_content, content_length))

    avg_length = total_length / len(documents) if documents else 0
    return contents, avg_length


def write_folder_report(summary, processing_time=0.0, chosen_model="Unknown"):
    contents, avg_length = summary
    image_count = len(contents)
    avg_time = (processing_time / image_count) if image_count else 0.0

    lengths = [length for _, _, length in contents]
    if lengths:
        median_length = statistics.median(lengths)
        min_length = min(lengths)
        max_length = max(lengths)
        stdev_length = statistics.stdev(lengths) if len(lengths) > 1 else 0.0
        cv_pct = (stdev_length / avg_length * 100.0) if avg_length else 0.0
    else:
        median_length = min_length = max_length = stdev_length = cv_pct = 0.0

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False) as temp_file:
        temp_file.write(f"Vision Model: {chosen_model}\n")
        temp_file.write(f"Average Summary Length: {avg_length:.2f} characters\n")
        temp_file.write(f"Median Summary Length: {median_length:.2f} characters\n")
        temp_file.write(f"Shortest / Longest Summary: {min_length} / {max_length} characters\n")
        temp_file.write(f"Standard Deviation: {stdev_length:.2f} characters\n")
        temp_file.write(f"Coefficient of Variation: {cv_pct:.1f}% (lower = more consistent)\n")
        temp_file.write(f"Total Processing Time: {processing_time:.2f} seconds (excludes model load)\n")
        temp_file.write(f"Average Processing Time Per Image: {avg_time:.2f} seconds\n")
        temp_file.write("="*50 + "\n\n")

        for filepath, content, length in contents:
            temp_file.write(f"File Path: {filepath}\n")
            temp_file.write(f"Summary Length: {length} characters\n")
            temp_file.write("-"*50 + "\n")
            temp_file.write(f"{content}\n\n")
            temp_file.write("="*50 + "\n\n")

        return temp_file.name


def write_comparison_report(image_path, results):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False) as temp_file:
        model_col_width = 23
        count_col_width = 12
        time_col_width = 12
        speed_col_width = 12

        temp_file.write(f"Image Path: {image_path}\n")
        temp_file.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        chunk_advice = (
            "Remember to adjust your 'chunk size' setting to exceed the longest image summary that you expect. "
            "For large bodies of text (e.g. from a .pdf) splitting/overlapping chunks of text is fine, but for image "
            "summaries you want any/all summaries to fit within a single chunk that will be put into the vector database."
        )
        temp_file.write(textwrap.fill(chunk_advice, width=100) + "\n\n")

        temp_file.write("Model Performance Comparison Table:\n")
        temp_file.write("+" + "-"*model_col_width + "+" + "-"*count_col_width + "+" +
                       "-"*time_col_width + "+" + "-"*speed_col_width + "+\n")
        temp_file.write("|" + "Model Name".center(model_col_width) + "|" +
                       "Char Count".center(count_col_width) + "|" +
                       "Time (sec)".center(time_col_width) + "|" +
                       "Char/Sec".center(speed_col_width) + "|\n")
        temp_file.write("+" + "-"*model_col_width + "+" + "-"*count_col_width + "+" +
                       "-"*time_col_width + "+" + "-"*speed_col_width + "+\n")

        for model_name, description, process_time in results:
            char_count = len(description)
            chars_per_sec = char_count / process_time if process_time > 0 else 0

            temp_file.write("|" + model_name.ljust(model_col_width) + "|" +
                          str(char_count).center(count_col_width) + "|" +
                          f"{process_time:.2f}".center(time_col_width) + "|" +
                          f"{chars_per_sec:.1f}".center(speed_col_width) + "|\n")

        temp_file.write("+" + "-"*model_col_width + "+" + "-"*count_col_width + "+" +
                       "-"*time_col_width + "+" + "-"*speed_col_width + "+\n\n")

        for model_name, description, process_time in results:
            char_count = len(description)
            chars_per_sec = char_count / process_time if process_time > 0 else 0

            temp_file.write(f"Model: {model_name}\n")
            temp_file.write(f"Summary Length: {char_count}\n")
            temp_file.write(f"Processing Time: {process_time:.2f} seconds\n")
            temp_file.write(f"Characters per Second: {chars_per_sec:.1f}\n")
            temp_file.write("="*50 + "\n")
            if description.strip():
                temp_file.write(textwrap.fill(description, width=100) + "\n\n")
            else:
                temp_file.write("[No output generated]\n\n")
            temp_file.write("-"*50 + "\n\n")

        return temp_file.name
