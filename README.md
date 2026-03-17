# AMRfold

Structure-informed AMR resistance protein network server.

AMRfold computes a TM-score structural similarity network across WHO 2024
Bacterial Priority Pathogen List (BPPL) resistance genes, enabling:

- Cross-ARG structural comparison beyond sequence identity
- Drug repurposing signals from shared binding pocket geometry
- Variant confidence mapping via per-residue pLDDT

## Data sources

| Source | License |
|---|---|
| CARD | McMaster academic (not redistributed) |
| AlphaFold DB v6 | CC BY 4.0 |
| RCSB PDB | CC0 1.0 |

## Structure format

AMRfold uses mmCIF (.cif) exclusively - future-proof for PDB
extended 12-character IDs, mandatory before 2028.

## License

Code: MIT. Pre-computed data: CC BY 4.0 (Zenodo release).
