import copy
import importlib
import json
import logging
import math
import os
import queue
import tempfile
import traceback
import warnings
from collections import OrderedDict
from contextlib import contextmanager
from multiprocessing import Queue
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Iterator, List, Literal, Optional, Tuple, Union, overload

import numpy as np
import torch
import torch.multiprocessing as mp
import transformers
from huggingface_hub import HfApi
from numpy import ndarray
from torch import Tensor, device, nn
from tqdm.autonotebook import trange
from transformers import is_torch_npu_available

from sentence_transformers.model_card import SentenceTransformerModelCardData, generate_model_card
from sentence_transformers.similarity_functions import SimilarityFunction

from . import __MODEL_HUB_ORGANIZATION__, __version__
from .evaluation import SentenceEvaluator
from .fit_mixin import FitMixin
from .models import Normalize, Pooling, Transformer
from .quantization import quantize_embeddings
from .util import (
    batch_to_device,
    get_device_name,
    import_from_string,
    is_sentence_transformer_model,
    load_dir_path,
    load_file_path,
    save_to_hub_args_decorator,
    truncate_embeddings,
)

logger = logging.getLogger(__name__)


class SentenceTransformer(nn.Sequential, FitMixin):

    def __init__(
        self,
        model_name_or_path: Optional[str] = None,
        modules: Optional[Iterable[nn.Module]] = None,
        device: Optional[str] = None,
        prompts: Optional[Dict[str, str]] = None,
        default_prompt_name: Optional[str] = None,
        similarity_fn_name: Optional[Union[str, SimilarityFunction]] = None,
        cache_folder: Optional[str] = None,
        trust_remote_code: bool = False,
        revision: Optional[str] = None,
        local_files_only: bool = False,
        token: Optional[Union[bool, str]] = None,
        use_auth_token: Optional[Union[bool, str]] = None,
        truncate_dim: Optional[int] = None,
        model_kwargs: Optional[Dict[str, Any]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        config_kwargs: Optional[Dict[str, Any]] = None,
        model_card_data: Optional[SentenceTransformerModelCardData] = None,
    ) -> None:
        self.prompts = prompts or {}
        self.default_prompt_name = default_prompt_name
        self.similarity_fn_name = similarity_fn_name
        self.truncate_dim = truncate_dim
        self.model_card_data = model_card_data or SentenceTransformerModelCardData()
        self._model_card_vars = {}
        self._model_card_text = None
        self._model_config = {}
        if use_auth_token is not None:
            warnings.warn(
                "The `use_auth_token` argument is deprecated and will be removed in v3 of SentenceTransformers.",
                FutureWarning,
            )
            if token is not None:
                raise ValueError(
                    "`token` and `use_auth_token` are both specified. Please set only the argument `token`."
                )
            token = use_auth_token

        if cache_folder is None:
            cache_folder = os.getenv("SENTENCE_TRANSFORMERS_HOME")

        if device is None:
            device = get_device_name()
            logger.info("Use pytorch device_name: {}".format(device))

        if device == "hpu" and importlib.util.find_spec("optimum") is not None:
            from optimum.habana.transformers.modeling_utils import adapt_transformers_to_gaudi

            adapt_transformers_to_gaudi()

        if model_name_or_path is not None and model_name_or_path != "":
            logger.info("Load pretrained SentenceTransformer: {}".format(model_name_or_path))

            basic_transformer_models = [
                "albert-base-v1",
                "albert-base-v2",
                "albert-large-v1",
                "albert-large-v2",
                "albert-xlarge-v1",
                "albert-xlarge-v2",
                "albert-xxlarge-v1",
                "albert-xxlarge-v2",
                "bert-base-cased-finetuned-mrpc",
                "bert-base-cased",
                "bert-base-chinese",
                "bert-base-german-cased",
                "bert-base-german-dbmdz-cased",
                "bert-base-german-dbmdz-uncased",
                "bert-base-multilingual-cased",
                "bert-base-multilingual-uncased",
                "bert-base-uncased",
                "bert-large-cased-whole-word-masking-finetuned-squad",
                "bert-large-cased-whole-word-masking",
                "bert-large-cased",
                "bert-large-uncased-whole-word-masking-finetuned-squad",
                "bert-large-uncased-whole-word-masking",
                "bert-large-uncased",
                "camembert-base",
                "ctrl",
                "distilbert-base-cased-distilled-squad",
                "distilbert-base-cased",
                "distilbert-base-german-cased",
                "distilbert-base-multilingual-cased",
                "distilbert-base-uncased-distilled-squad",
                "distilbert-base-uncased-finetuned-sst-2-english",
                "distilbert-base-uncased",
                "distilgpt2",
                "distilroberta-base",
                "gpt2-large",
                "gpt2-medium",
                "gpt2-xl",
                "gpt2",
                "openai-gpt",
                "roberta-base-openai-detector",
                "roberta-base",
                "roberta-large-mnli",
                "roberta-large-openai-detector",
                "roberta-large",
                "t5-11b",
                "t5-3b",
                "t5-base",
                "t5-large",
                "t5-small",
                "transfo-xl-wt103",
                "xlm-clm-ende-1024",
                "xlm-clm-enfr-1024",
                "xlm-mlm-100-1280",
                "xlm-mlm-17-1280",
                "xlm-mlm-en-2048",
                "xlm-mlm-ende-1024",
                "xlm-mlm-enfr-1024",
                "xlm-mlm-enro-1024",
                "xlm-mlm-tlm-xnli15-1024",
                "xlm-mlm-xnli15-1024",
                "xlm-roberta-base",
                "xlm-roberta-large-finetuned-conll02-dutch",
                "xlm-roberta-large-finetuned-conll02-spanish",
                "xlm-roberta-large-finetuned-conll03-english",
                "xlm-roberta-large-finetuned-conll03-german",
                "xlm-roberta-large",
                "xlnet-base-cased",
                "xlnet-large-cased",
            ]

            if not os.path.exists(model_name_or_path):
                if "\\" in model_name_or_path or model_name_or_path.count("/") > 1:
                    raise ValueError("Path {} not found".format(model_name_or_path))

                if "/" not in model_name_or_path and model_name_or_path.lower() not in basic_transformer_models:
                    model_name_or_path = __MODEL_HUB_ORGANIZATION__ + "/" + model_name_or_path

            if is_sentence_transformer_model(
                model_name_or_path,
                token,
                cache_folder=cache_folder,
                revision=revision,
                local_files_only=local_files_only,
            ):
                modules = self._load_sbert_model(
                    model_name_or_path,
                    token=token,
                    cache_folder=cache_folder,
                    revision=revision,
                    trust_remote_code=trust_remote_code,
                    local_files_only=local_files_only,
                    model_kwargs=model_kwargs,
                    tokenizer_kwargs=tokenizer_kwargs,
                    config_kwargs=config_kwargs,
                )
            else:
                modules = self._load_auto_model(
                    model_name_or_path,
                    token=token,
                    cache_folder=cache_folder,
                    revision=revision,
                    trust_remote_code=trust_remote_code,
                    local_files_only=local_files_only,
                    model_kwargs=model_kwargs,
                    tokenizer_kwargs=tokenizer_kwargs,
                    config_kwargs=config_kwargs,
                )

        if modules is not None and not isinstance(modules, OrderedDict):
            modules = OrderedDict([(str(idx), module) for idx, module in enumerate(modules)])

        super().__init__(modules)

        self.to(device)
        self.is_hpu_graph_enabled = False

        if self.default_prompt_name is not None and self.default_prompt_name not in self.prompts:
            raise ValueError(
                f"Default prompt name '{self.default_prompt_name}' not found in the configured prompts "
                f"dictionary with keys {list(self.prompts.keys())!r}."
            )

        if self.prompts:
            logger.info(f"{len(self.prompts)} prompts are loaded, with the keys: {list(self.prompts.keys())}")
        if self.default_prompt_name:
            logger.warning(
                f"Default prompt name is set to '{self.default_prompt_name}'. "
                "This prompt will be applied to all `encode()` calls, except if `encode()` "
                "is called with `prompt` or `prompt_name` parameters."
            )

        if model_name_or_path in ("hkunlp/instructor-base", "hkunlp/instructor-large", "hkunlp/instructor-xl"):
            self.set_pooling_include_prompt(include_prompt=False)
        elif (
            model_name_or_path
            and "/" in model_name_or_path
            and "instructor" in model_name_or_path.split("/")[1].lower()
        ):
            if any([module.include_prompt for module in self if isinstance(module, Pooling)]):
                logger.warning(
                    "Instructor models require `include_prompt=False` in the pooling configuration. "
                    "Either update the model configuration or call `model.set_pooling_include_prompt(False)` after loading the model."
                )

        self.model_card_data.register_model(self)

    def encode(
        self,
        sentences: Union[str, List[str]],
        prompt_name: Optional[str] = None,
        prompt: Optional[str] = None,
        batch_size: int = 32,
        show_progress_bar: bool = None,
        output_value: Optional[Literal["sentence_embedding", "token_embeddings"]] = "sentence_embedding",
        precision: Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32",
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        device: str = None,
        normalize_embeddings: bool = False,
    ) -> Union[List[Tensor], ndarray, Tensor]:
        if self.device.type == "hpu" and not self.is_hpu_graph_enabled:
            import habana_frameworks.torch as ht

            ht.hpu.wrap_in_hpu_graph(self, disable_tensor_cache=True)
            self.is_hpu_graph_enabled = True

        self.eval()
        if show_progress_bar is None:
            show_progress_bar = (
                logger.getEffectiveLevel() == logging.INFO or logger.getEffectiveLevel() == logging.DEBUG
            )

        if convert_to_tensor:
            convert_to_numpy = False

        if output_value != "sentence_embedding":
            convert_to_tensor = False
            convert_to_numpy = False

        input_was_string = False
        if isinstance(sentences, str) or not hasattr(
            sentences, "__len__"
        ):
            sentences = [sentences]
            input_was_string = True

        if prompt is None:
            if prompt_name is not None:
                try:
                    prompt = self.prompts[prompt_name]
                except KeyError:
                    raise ValueError(
                        f"Prompt name '{prompt_name}' not found in the configured prompts dictionary with keys {list(self.prompts.keys())!r}."
                    )
            elif self.default_prompt_name is not None:
                prompt = self.prompts.get(self.default_prompt_name, None)
        else:
            if prompt_name is not None:
                logger.warning(
                    "Encode with either a `prompt`, a `prompt_name`, or neither, but not both. "
                    "Ignoring the `prompt_name` in favor of `prompt`."
                )

        extra_features = {}
        if prompt is not None:
            sentences = [prompt + sentence for sentence in sentences]

            tokenized_prompt = self.tokenize([prompt])
            if "input_ids" in tokenized_prompt:
                extra_features["prompt_length"] = tokenized_prompt["input_ids"].shape[-1] - 1

        if device is None:
            device = self.device

        self.to(device)

        all_embeddings = []
        length_sorted_idx = np.argsort([-self._text_length(sen) for sen in sentences])
        sentences_sorted = [sentences[idx] for idx in length_sorted_idx]

        for start_index in trange(0, len(sentences), batch_size, desc="Batches", disable=not show_progress_bar):
            sentences_batch = sentences_sorted[start_index : start_index + batch_size]
            features = self.tokenize(sentences_batch)
            if self.device.type == "hpu":
                if "input_ids" in features:
                    curr_tokenize_len = features["input_ids"].shape
                    additional_pad_len = 2 ** math.ceil(math.log2(curr_tokenize_len[1])) - curr_tokenize_len[1]
                    features["input_ids"] = torch.cat(
                        (
                            features["input_ids"],
                            torch.ones((curr_tokenize_len[0], additional_pad_len), dtype=torch.int8),
                        ),
                        -1,
                    )
                    features["attention_mask"] = torch.cat(
                        (
                            features["attention_mask"],
                            torch.zeros((curr_tokenize_len[0], additional_pad_len), dtype=torch.int8),
                        ),
                        -1,
                    )
                    if "token_type_ids" in features:
                        features["token_type_ids"] = torch.cat(
                            (
                                features["token_type_ids"],
                                torch.zeros((curr_tokenize_len[0], additional_pad_len), dtype=torch.int8),
                            ),
                            -1,
                        )

            features = batch_to_device(features, device)
            features.update(extra_features)

            with torch.no_grad():
                out_features = self.forward(features)
                if self.device.type == "hpu":
                    out_features = copy.deepcopy(out_features)

                out_features["sentence_embedding"] = truncate_embeddings(
                    out_features["sentence_embedding"], self.truncate_dim
                )

                if output_value == "token_embeddings":
                    embeddings = []
                    for token_emb, attention in zip(out_features[output_value], out_features["attention_mask"]):
                        last_mask_id = len(attention) - 1
                        while last_mask_id > 0 and attention[last_mask_id].item() == 0:
                            last_mask_id -= 1

                        embeddings.append(token_emb[0 : last_mask_id + 1])
                elif output_value is None:
                    embeddings = []
                    for sent_idx in range(len(out_features["sentence_embedding"])):
                        row = {name: out_features[name][sent_idx] for name in out_features}
                        embeddings.append(row)
                else:
                    embeddings = out_features[output_value]
                    embeddings = embeddings.detach()
                    if normalize_embeddings:
                        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

                    if convert_to_numpy:
                        embeddings = embeddings.cpu()

                all_embeddings.extend(embeddings)

        all_embeddings = [all_embeddings[idx] for idx in np.argsort(length_sorted_idx)]

        if precision and precision != "float32":
            all_embeddings = quantize_embeddings(all_embeddings, precision=precision)

        if convert_to_tensor:
            if len(all_embeddings):
                if isinstance(all_embeddings, np.ndarray):
                    all_embeddings = torch.from_numpy(all_embeddings)
                else:
                    all_embeddings = torch.stack(all_embeddings)
            else:
                all_embeddings = torch.Tensor()
        elif convert_to_numpy:
            if not isinstance(all_embeddings, np.ndarray):
                if all_embeddings[0].dtype == torch.bfloat16:
                    all_embeddings = np.asarray([emb.float().numpy() for emb in all_embeddings])
                else:
                    all_embeddings = np.asarray([emb.numpy() for emb in all_embeddings])
        elif isinstance(all_embeddings, np.ndarray):
            all_embeddings = [torch.from_numpy(embedding) for embedding in all_embeddings]

        if input_was_string:
            all_embeddings = all_embeddings[0]

        return all_embeddings

    @property
    def similarity_fn_name(self) -> Optional[str]:
        return self._similarity_fn_name

    @similarity_fn_name.setter
    def similarity_fn_name(self, value: Union[str, SimilarityFunction]) -> None:
        if isinstance(value, SimilarityFunction):
            value = value.value
        self._similarity_fn_name = value

        if value is not None:
            self._similarity = SimilarityFunction.to_similarity_fn(value)
            self._similarity_pairwise = SimilarityFunction.to_similarity_pairwise_fn(value)

    @overload
    def similarity(self, embeddings1: Tensor, embeddings2: Tensor) -> Tensor: ...

    @overload
    def similarity(self, embeddings1: ndarray, embeddings2: ndarray) -> Tensor: ...

    @property
    def similarity(self) -> Callable[[Union[Tensor, ndarray], Union[Tensor, ndarray]], Tensor]:
        if self.similarity_fn_name is None:
            self.similarity_fn_name = SimilarityFunction.COSINE
        return self._similarity

    @overload
    def similarity_pairwise(self, embeddings1: Tensor, embeddings2: Tensor) -> Tensor: ...

    @overload
    def similarity_pairwise(self, embeddings1: ndarray, embeddings2: ndarray) -> Tensor: ...

    @property
    def similarity_pairwise(self) -> Callable[[Union[Tensor, ndarray], Union[Tensor, ndarray]], Tensor]:
        if self.similarity_fn_name is None:
            self.similarity_fn_name = SimilarityFunction.COSINE
        return self._similarity_pairwise

    def start_multi_process_pool(
        self, target_devices: List[str] = None
    ) -> Dict[Literal["input", "output", "processes"], Any]:
        if target_devices is None:
            if torch.cuda.is_available():
                target_devices = ["cuda:{}".format(i) for i in range(torch.cuda.device_count())]
            elif is_torch_npu_available():
                target_devices = ["npu:{}".format(i) for i in range(torch.npu.device_count())]
            else:
                logger.info("CUDA/NPU is not available. Starting 4 CPU workers")
                target_devices = ["cpu"] * 4

        logger.info("Start multi-process pool on devices: {}".format(", ".join(map(str, target_devices))))

        self.to("cpu")
        self.share_memory()
        ctx = mp.get_context("spawn")
        input_queue = ctx.Queue()
        output_queue = ctx.Queue()
        processes = []

        for device_id in target_devices:
            p = ctx.Process(
                target=SentenceTransformer._encode_multi_process_worker,
                args=(device_id, self, input_queue, output_queue),
                daemon=True,
            )
            p.start()
            processes.append(p)

        return {"input": input_queue, "output": output_queue, "processes": processes}

    @staticmethod
    def stop_multi_process_pool(pool: Dict[Literal["input", "output", "processes"], Any]) -> None:
        for p in pool["processes"]:
            p.terminate()

        for p in pool["processes"]:
            p.join()
            p.close()

        pool["input"].close()
        pool["output"].close()

    def encode_multi_process(
        self,
        sentences: List[str],
        pool: Dict[Literal["input", "output", "processes"], Any],
        prompt_name: Optional[str] = None,
        prompt: Optional[str] = None,
        batch_size: int = 32,
        chunk_size: int = None,
        precision: Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32",
        normalize_embeddings: bool = False,
    ) -> np.ndarray:

        if chunk_size is None:
            chunk_size = min(math.ceil(len(sentences) / len(pool["processes"]) / 10), 5000)

        logger.debug(f"Chunk data into {math.ceil(len(sentences) / chunk_size)} packages of size {chunk_size}")

        input_queue = pool["input"]
        last_chunk_id = 0
        chunk = []

        for sentence in sentences:
            chunk.append(sentence)
            if len(chunk) >= chunk_size:
                input_queue.put(
                    [last_chunk_id, batch_size, chunk, prompt_name, prompt, precision, normalize_embeddings]
                )
                last_chunk_id += 1
                chunk = []

        if len(chunk) > 0:
            input_queue.put([last_chunk_id, batch_size, chunk, prompt_name, prompt, precision, normalize_embeddings])
            last_chunk_id += 1

        output_queue = pool["output"]
        results_list = sorted([output_queue.get() for _ in range(last_chunk_id)], key=lambda x: x[0])
        embeddings = np.concatenate([result[1] for result in results_list])
        return embeddings

    @staticmethod
    def _encode_multi_process_worker(
        target_device: str, model: "SentenceTransformer", input_queue: Queue, results_queue: Queue
    ) -> None:
        while True:
            try:
                chunk_id, batch_size, sentences, prompt_name, prompt, precision, normalize_embeddings = (
                    input_queue.get()
                )
                embeddings = model.encode(
                    sentences,
                    prompt_name=prompt_name,
                    prompt=prompt,
                    device=target_device,
                    show_progress_bar=False,
                    precision=precision,
                    convert_to_numpy=True,
                    batch_size=batch_size,
                    normalize_embeddings=normalize_embeddings,
                )

                results_queue.put([chunk_id, embeddings])
            except queue.Empty:
                break

    def set_pooling_include_prompt(self, include_prompt: bool) -> None:
        for module in self:
            if isinstance(module, Pooling):
                module.include_prompt = include_prompt
                break

    def get_max_seq_length(self) -> Optional[int]:
        if hasattr(self._first_module(), "max_seq_length"):
            return self._first_module().max_seq_length

        return None

    def tokenize(self, texts: Union[List[str], List[Dict], List[Tuple[str, str]]]) -> Dict[str, Tensor]:
        return self._first_module().tokenize(texts)

    def get_sentence_features(self, *features) -> Dict[Literal["sentence_embedding"], torch.Tensor]:
        return self._first_module().get_sentence_features(*features)

    def get_sentence_embedding_dimension(self) -> Optional[int]:
        output_dim = None
        for mod in reversed(self._modules.values()):
            sent_embedding_dim_method = getattr(mod, "get_sentence_embedding_dimension", None)
            if callable(sent_embedding_dim_method):
                output_dim = sent_embedding_dim_method()
                break
        if self.truncate_dim is not None:
            return min(output_dim or np.inf, self.truncate_dim)
        return output_dim

    @contextmanager
    def truncate_sentence_embeddings(self, truncate_dim: Optional[int]) -> Iterator[None]:
        original_output_dim = self.truncate_dim
        try:
            self.truncate_dim = truncate_dim
            yield
        finally:
            self.truncate_dim = original_output_dim

    def _first_module(self) -> torch.nn.Module:
        return self._modules[next(iter(self._modules))]

    def _last_module(self) -> torch.nn.Module:
        return self._modules[next(reversed(self._modules))]

    def save(
        self,
        path: str,
        model_name: Optional[str] = None,
        create_model_card: bool = True,
        train_datasets: Optional[List[str]] = None,
        safe_serialization: bool = True,
    ) -> None:
        if path is None:
            return

        os.makedirs(path, exist_ok=True)

        logger.info("Save model to {}".format(path))
        modules_config = []

        self._model_config["__version__"] = {
            "sentence_transformers": __version__,
            "transformers": transformers.__version__,
            "pytorch": torch.__version__,
        }

        with open(os.path.join(path, "config_sentence_transformers.json"), "w") as fOut:
            config = self._model_config.copy()
            config["prompts"] = self.prompts
            config["default_prompt_name"] = self.default_prompt_name
            config["similarity_fn_name"] = self.similarity_fn_name
            json.dump(config, fOut, indent=2)

        for idx, name in enumerate(self._modules):
            module = self._modules[name]
            if idx == 0 and isinstance(module, Transformer):
                model_path = path + "/"
            else:
                model_path = os.path.join(path, str(idx) + "_" + type(module).__name__)

            os.makedirs(model_path, exist_ok=True)
            try:
                module.save(model_path, safe_serialization=safe_serialization)
            except TypeError:
                module.save(model_path)

            modules_config.append(
                {"idx": idx, "name": name, "path": os.path.basename(model_path), "type": type(module).__module__}
            )

        with open(os.path.join(path, "modules.json"), "w") as fOut:
            json.dump(modules_config, fOut, indent=2)

        if create_model_card:
            self._create_model_card(path, model_name, train_datasets)

    def save_pretrained(
        self,
        path: str,
        model_name: Optional[str] = None,
        create_model_card: bool = True,
        train_datasets: Optional[List[str]] = None,
        safe_serialization: bool = True,
    ) -> None:
        self.save(
            path,
            model_name=model_name,
            create_model_card=create_model_card,
            train_datasets=train_datasets,
            safe_serialization=safe_serialization,
        )

    def _create_model_card(
        self, path: str, model_name: Optional[str] = None, train_datasets: Optional[List[str]] = "deprecated"
    ) -> None:
        if model_name:
            model_path = Path(model_name)
            if not model_path.exists() and not self.model_card_data.model_id:
                self.model_card_data.model_id = model_name

        if self._model_card_text and self.model_card_data.trainer is None:
            model_card = self._model_card_text
            if self.model_card_data.model_id:
                model_card = model_card.replace(
                    'model = SentenceTransformer("sentence_transformers_model_id"',
                    f'model = SentenceTransformer("{self.model_card_data.model_id}"',
                )
        else:
            try:
                model_card = generate_model_card(self)
            except Exception:
                logger.error(
                    f"Error while generating model card:\n{traceback.format_exc()}"
                    "Consider opening an issue on https://github.com/UKPLab/sentence-transformers/issues with this traceback.\n"
                    "Skipping model card creation."
                )
                return

        with open(os.path.join(path, "README.md"), "w", encoding="utf8") as fOut:
            fOut.write(model_card)

    @save_to_hub_args_decorator
    def save_to_hub(
        self,
        repo_id: str,
        organization: Optional[str] = None,
        token: Optional[str] = None,
        private: Optional[bool] = None,
        safe_serialization: bool = True,
        commit_message: str = "Add new SentenceTransformer model.",
        local_model_path: Optional[str] = None,
        exist_ok: bool = False,
        replace_model_card: bool = False,
        train_datasets: Optional[List[str]] = None,
    ) -> str:
        logger.warning(
            "The `save_to_hub` method is deprecated and will be removed in a future version of SentenceTransformers."
            " Please use `push_to_hub` instead for future model uploads."
        )

        if organization:
            if "/" not in repo_id:
                logger.warning(
                    f'Providing an `organization` to `save_to_hub` is deprecated, please use `repo_id="{organization}/{repo_id}"` instead.'
                )
                repo_id = f"{organization}/{repo_id}"
            elif repo_id.split("/")[0] != organization:
                raise ValueError(
                    "Providing an `organization` to `save_to_hub` is deprecated, please only use `repo_id`."
                )
            else:
                logger.warning(
                    f'Providing an `organization` to `save_to_hub` is deprecated, please only use `repo_id="{repo_id}"` instead.'
                )

        return self.push_to_hub(
            repo_id=repo_id,
            token=token,
            private=private,
            safe_serialization=safe_serialization,
            commit_message=commit_message,
            local_model_path=local_model_path,
            exist_ok=exist_ok,
            replace_model_card=replace_model_card,
            train_datasets=train_datasets,
        )

    def push_to_hub(
        self,
        repo_id: str,
        token: Optional[str] = None,
        private: Optional[bool] = None,
        safe_serialization: bool = True,
        commit_message: str = "Add new SentenceTransformer model.",
        local_model_path: Optional[str] = None,
        exist_ok: bool = False,
        replace_model_card: bool = False,
        train_datasets: Optional[List[str]] = None,
    ) -> str:
        api = HfApi(token=token)
        repo_url = api.create_repo(
            repo_id=repo_id,
            private=private,
            repo_type=None,
            exist_ok=exist_ok,
        )
        repo_id = repo_url.repo_id
        self.model_card_data.set_model_id(repo_id)
        if local_model_path:
            folder_url = api.upload_folder(
                repo_id=repo_id, folder_path=local_model_path, commit_message=commit_message
            )
        else:
            with tempfile.TemporaryDirectory() as tmp_dir:
                create_model_card = replace_model_card or not os.path.exists(os.path.join(tmp_dir, "README.md"))
                self.save(
                    tmp_dir,
                    model_name=repo_url.repo_id,
                    create_model_card=create_model_card,
                    train_datasets=train_datasets,
                    safe_serialization=safe_serialization,
                )
                folder_url = api.upload_folder(repo_id=repo_id, folder_path=tmp_dir, commit_message=commit_message)

        refs = api.list_repo_refs(repo_id=repo_id)
        for branch in refs.branches:
            if branch.name == "main":
                return f"https://huggingface.co/{repo_id}/commit/{branch.target_commit}"
        return folder_url

    def _text_length(self, text: Union[str, List[str], List[int], List[List[int]]]):
        if isinstance(text, str):
            return len(text)
        elif isinstance(text, dict):
            return len(next(iter(text.values())))
        elif not hasattr(text, "__len__"):
            return 1
        elif len(text) == 0 or isinstance(text[0], int):
            return len(text)
        else:
            return sum([len(t) for t in text])

    def evaluate(self, evaluator: SentenceEvaluator, output_path: str = None) -> Union[Dict[str, float], float]:
        if output_path is not None:
            os.makedirs(output_path, exist_ok=True)
        return evaluator(self, output_path)

    def _load_auto_model(
        self,
        model_name_or_path: str,
        token: Optional[Union[bool, str]],
        cache_folder: Optional[str],
        revision: Optional[str] = None,
        trust_remote_code: bool = False,
        local_files_only: bool = False,
        model_kwargs: Optional[Dict[str, Any]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        config_kwargs: Optional[Dict[str, Any]] = None,
    ) -> List[nn.Module]:
        logger.warning(
            f"No sentence-transformers model found with name {model_name_or_path}. Creating a new one with mean pooling."
        )

        shared_kwargs = {
            "token": token,
            "trust_remote_code": trust_remote_code,
            "revision": revision,
            "local_files_only": local_files_only,
        }
        model_kwargs = shared_kwargs if model_kwargs is None else {**shared_kwargs, **model_kwargs}
        tokenizer_kwargs = shared_kwargs if tokenizer_kwargs is None else {**shared_kwargs, **tokenizer_kwargs}
        config_kwargs = shared_kwargs if config_kwargs is None else {**shared_kwargs, **config_kwargs}

        transformer_model = Transformer(
            model_name_or_path,
            cache_dir=cache_folder,
            model_args=model_kwargs,
            tokenizer_args=tokenizer_kwargs,
            config_args=config_kwargs,
        )
        pooling_model = Pooling(transformer_model.get_word_embedding_dimension(), "mean")
        self.model_card_data.set_base_model(model_name_or_path, revision=revision)
        return [transformer_model, pooling_model]

    def _load_sbert_model(
        self,
        model_name_or_path: str,
        token: Optional[Union[bool, str]],
        cache_folder: Optional[str],
        revision: Optional[str] = None,
        trust_remote_code: bool = False,
        local_files_only: bool = False,
        model_kwargs: Optional[Dict[str, Any]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        config_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, nn.Module]:
        config_sentence_transformers_json_path = load_file_path(
            model_name_or_path,
            "config_sentence_transformers.json",
            token=token,
            cache_folder=cache_folder,
            revision=revision,
            local_files_only=local_files_only,
        )
        if config_sentence_transformers_json_path is not None:
            with open(config_sentence_transformers_json_path) as fIn:
                self._model_config = json.load(fIn)

            if (
                "__version__" in self._model_config
                and "sentence_transformers" in self._model_config["__version__"]
                and self._model_config["__version__"]["sentence_transformers"] > __version__
            ):
                logger.warning(
                    "You try to use a model that was created with version {}, however, your version is {}. This might cause unexpected behavior or errors. In that case, try to update to the latest version.\n\n\n".format(
                        self._model_config["__version__"]["sentence_transformers"], __version__
                    )
                )

            if self.similarity_fn_name is None:
                self.similarity_fn_name = self._model_config.get("similarity_fn_name", None)
            if not self.prompts:
                self.prompts = self._model_config.get("prompts", {})
            if not self.default_prompt_name:
                self.default_prompt_name = self._model_config.get("default_prompt_name", None)

        model_card_path = load_file_path(
            model_name_or_path,
            "README.md",
            token=token,
            cache_folder=cache_folder,
            revision=revision,
            local_files_only=local_files_only,
        )
        if model_card_path is not None:
            try:
                with open(model_card_path, encoding="utf8") as fIn:
                    self._model_card_text = fIn.read()
            except Exception:
                pass

        modules_json_path = load_file_path(
            model_name_or_path,
            "modules.json",
            token=token,
            cache_folder=cache_folder,
            revision=revision,
            local_files_only=local_files_only,
        )
        with open(modules_json_path) as fIn:
            modules_config = json.load(fIn)

        modules = OrderedDict()
        for module_config in modules_config:
            module_class = import_from_string(module_config["type"])
            if module_class == Transformer and module_config["path"] == "":
                kwargs = {}
                for config_name in [
                    "sentence_bert_config.json",
                    "sentence_roberta_config.json",
                    "sentence_distilbert_config.json",
                    "sentence_camembert_config.json",
                    "sentence_albert_config.json",
                    "sentence_xlm-roberta_config.json",
                    "sentence_xlnet_config.json",
                ]:
                    config_path = load_file_path(
                        model_name_or_path,
                        config_name,
                        token=token,
                        cache_folder=cache_folder,
                        revision=revision,
                        local_files_only=local_files_only,
                    )
                    if config_path is not None:
                        with open(config_path) as fIn:
                            kwargs = json.load(fIn)
                            if "model_args" in kwargs and "trust_remote_code" in kwargs["model_args"]:
                                kwargs["model_args"].pop("trust_remote_code")
                            if "tokenizer_args" in kwargs and "trust_remote_code" in kwargs["tokenizer_args"]:
                                kwargs["tokenizer_args"].pop("trust_remote_code")
                            if "config_args" in kwargs and "trust_remote_code" in kwargs["config_args"]:
                                kwargs["config_args"].pop("trust_remote_code")
                        break

                hub_kwargs = {
                    "token": token,
                    "trust_remote_code": trust_remote_code,
                    "revision": revision,
                    "local_files_only": local_files_only,
                }
                if "model_args" not in kwargs:
                    kwargs["model_args"] = {}
                if "tokenizer_args" not in kwargs:
                    kwargs["tokenizer_args"] = {}
                if "config_args" not in kwargs:
                    kwargs["config_args"] = {}

                kwargs["model_args"].update(hub_kwargs)
                kwargs["tokenizer_args"].update(hub_kwargs)
                kwargs["config_args"].update(hub_kwargs)

                if model_kwargs:
                    kwargs["model_args"].update(model_kwargs)
                if tokenizer_kwargs:
                    kwargs["tokenizer_args"].update(tokenizer_kwargs)
                if config_kwargs:
                    kwargs["config_args"].update(config_kwargs)

                module = Transformer(model_name_or_path, cache_dir=cache_folder, **kwargs)
            else:
                if module_class == Normalize:
                    module_path = None
                else:
                    module_path = load_dir_path(
                        model_name_or_path,
                        module_config["path"],
                        token=token,
                        cache_folder=cache_folder,
                        revision=revision,
                        local_files_only=local_files_only,
                    )
                module = module_class.load(module_path)
            modules[module_config["name"]] = module

        if revision is None:
            path_parts = Path(modules_json_path)
            if len(path_parts.parts) >= 2:
                revision_path_part = Path(modules_json_path).parts[-2]
                if len(revision_path_part) == 40:
                    revision = revision_path_part
        self.model_card_data.set_base_model(model_name_or_path, revision=revision)
        return modules

    @staticmethod
    def load(input_path) -> "SentenceTransformer":
        return SentenceTransformer(input_path)

    @property
    def device(self) -> device:
        try:
            return next(self.parameters()).device
        except StopIteration:

            def find_tensor_attributes(module: nn.Module) -> List[Tuple[str, Tensor]]:
                tuples = [(k, v) for k, v in module.__dict__.items() if torch.is_tensor(v)]
                return tuples

            gen = self._named_members(get_members_fn=find_tensor_attributes)
            try:
                first_tuple = next(gen)
                return first_tuple[1].device
            except StopIteration:
                return torch.device("cpu")

    @property
    def tokenizer(self) -> Any:
        return self._first_module().tokenizer

    @tokenizer.setter
    def tokenizer(self, value) -> None:
        self._first_module().tokenizer = value

    @property
    def max_seq_length(self) -> int:
        return self._first_module().max_seq_length

    @max_seq_length.setter
    def max_seq_length(self, value) -> None:
        self._first_module().max_seq_length = value

    @property
    def _target_device(self) -> torch.device:
        logger.warning(
            "`SentenceTransformer._target_device` has been deprecated, please use `SentenceTransformer.device` instead.",
        )
        return self.device

    @_target_device.setter
    def _target_device(self, device: Optional[Union[int, str, torch.device]] = None) -> None:
        self.to(device)

    @property
    def _no_split_modules(self) -> List[str]:
        try:
            return self._first_module()._no_split_modules
        except AttributeError:
            return []

    @property
    def _keys_to_ignore_on_save(self) -> List[str]:
        try:
            return self._first_module()._keys_to_ignore_on_save
        except AttributeError:
            return []

    def gradient_checkpointing_enable(self, gradient_checkpointing_kwargs=None) -> None:
        for module in self:
            if isinstance(module, Transformer):
                return module.auto_model.gradient_checkpointing_enable(gradient_checkpointing_kwargs)
