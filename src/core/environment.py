import faulthandler
import logging
import multiprocessing


def prepare_process(log_level=logging.ERROR):
    faulthandler.enable(all_threads=True)
    multiprocessing.set_start_method("spawn", force=True)
    logging.basicConfig(level=log_level, format="%(message)s")
    from core.gpu_guard import hide_unsupported_gpus
    hide_unsupported_gpus()
    from core.native_preload import preload_native_libraries
    preload_native_libraries()
    from core.cuda_paths import set_cuda_paths
    set_cuda_paths()
