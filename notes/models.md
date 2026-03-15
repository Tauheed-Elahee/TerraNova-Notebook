# Candidate Models for TerraNova

Models with TransformerLens support and pre-trained SAEs available.
Sorted by company (ascending) then release date (descending).

| Model Family | Parameters | d_model | Layers | SAEs Available | Company | Released |
|---|---|---|---|---|---|---|
| **Gemma-2** (2b/9b/27b, base + it) | 2.1B–27B | 2304–4608 | 26–46 | Yes (Gemma Scope — all layers, residual/attn/MLP) | Google | 2024-06-27 |
| **Llama-3.1-8B** (base + instruct) | 7.8B | 4096 | 32 | Yes (EleutherAI — MLP layers) | Meta | 2024-07-23 |
| **Llama-3-8B** (base + instruct) | 7.8B | 4096 | 32 | Yes (EleutherAI — MLP layers) | Meta | 2024-04-17 |
| **GPT-2 small** | 85M | 768 | 12 | Yes (Bloom 2024 — all layers, residual stream, via SAELens) | OpenAI | 2019-02-14 |
| **Pythia** (70m/160m/410m, base + deduped) | 19M–302M | 512–1024 | 6–24 | Yes (EleutherAI — residual stream) | EleutherAI | 2023-04-03 |
