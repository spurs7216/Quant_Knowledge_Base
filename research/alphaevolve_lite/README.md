# AlphaEvolve-Lite Scaffold

This module holds the local control primitives for the Phase 4 search loop.

It is not a full AlphaEvolve implementation. It gives the project the pieces that must exist before strategy-generation prompts are useful:

- detect bounded `# EVOLVE-BLOCK-START` / `# EVOLVE-BLOCK-END` regions
- parse and apply AlphaEvolve-style SEARCH/REPLACE diffs
- store early smoke-test program records with lineage, metrics, descriptors, and status
- sample prior records for prompt construction
- store and retrieve compact reasoning-memory cards for prompt construction

Phase 4 v2 supersedes the initial JSONL-only database design. `program_database.py` remains a small smoke-test primitive; production search should implement the SQLite schema and JSONL audit log described in `projects/quant_research_system/phase4_search_loop/program_database_schema.md`.

The first production use should keep data loading, split dates, duplicate policy, cost accounting, and artifact writing outside evolve blocks.

`reasoning_memory.py` is the local ReasoningBank-style scaffold. It bootstraps evidence-linked Phase 4 seed lessons, retrieves active cards by controller stage and target surface, and writes deterministic batch memory updates. It does not call local Qwen or local embedding inference.
