"""Measure local CPU generation with a downloaded SmolLM2 checkpoint."""

import argparse
import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path


PROMPTS = {
    "general": "In one short sentence, explain why a source link helps a reader verify an answer.",
    "synthetic_evidence": (
        "Use only this synthetic passage: [SYN-001] The demo library opens at 9 AM. "
        "What time does it open? Answer in one sentence and include [SYN-001]."
    ),
    "missing_evidence": (
        "The evidence list is empty. Do not guess. In one sentence, explain that "
        "you cannot answer whether a sample product is eligible without reviewed evidence."
    ),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_dir", type=Path, help="Local checkpoint directory")
    args = parser.parse_args()
    model_dir = args.model_dir.resolve(strict=True)
    if not (model_dir / "model.safetensors").is_file():
        parser.error("model_dir must contain model.safetensors")

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    network_attempts = []

    def deny_network(event, _args):
        if event in {"socket.connect", "socket.getaddrinfo", "socket.gethostbyname"}:
            network_attempts.append(event)
            raise RuntimeError(f"Offline trial blocked {event}")

    sys.addaudithook(deny_network)
    start = time.perf_counter()
    import psutil
    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    process = psutil.Process()
    torch.set_num_threads(4)
    load_start = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, local_files_only=True, use_safetensors=True, dtype=torch.float32
    ).eval()
    load_seconds = time.perf_counter() - load_start
    results = []
    for name, prompt in PROMPTS.items():
        request_start = time.perf_counter()
        inputs = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], add_generation_prompt=True,
            tokenize=True, return_dict=True, return_tensors="pt",
        )
        input_tokens = inputs["input_ids"].shape[1]
        with torch.inference_mode():
            output = model.generate(**inputs, max_new_tokens=64, do_sample=False)
        new_tokens = output[0, input_tokens:]
        answer = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        results.append({
            "case": name, "seconds": round(time.perf_counter() - request_start, 3),
            "input_tokens": input_tokens, "generated_tokens": len(new_tokens), "output": answer,
        })

    memory = process.memory_info()
    print(json.dumps({
        "platform": platform.platform(),
        "cpu": os.environ.get("PROCESSOR_IDENTIFIER", platform.processor()),
        "cpu_threads": torch.get_num_threads(),
        "logical_cpus": psutil.cpu_count(),
        "system_ram_mib": round(psutil.virtual_memory().total / 2**20),
        "python": platform.python_version(), "torch": torch.__version__,
        "transformers": transformers.__version__, "psutil": psutil.__version__,
        "checkpoint_bytes": sum(p.stat().st_size for p in model_dir.iterdir() if p.is_file()),
        "weight_bytes": (model_dir / "model.safetensors").stat().st_size,
        "load_seconds": round(load_seconds, 3),
        "startup_to_first_response_seconds": round(load_start - start + load_seconds + results[0]["seconds"], 3),
        "warm_median_seconds": statistics.median(item["seconds"] for item in results[1:]),
        "peak_working_set_mib": round(memory.peak_wset / 2**20, 1) if hasattr(memory, "peak_wset") else None,
        "final_rss_mib": round(memory.rss / 2**20, 1),
        "network_attempts": network_attempts, "results": results,
    }, indent=2, ensure_ascii=True))
    if network_attempts or any(not item["output"] for item in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
