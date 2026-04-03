# AMRfold

**Structure-informed antimicrobial resistance gene mining using FoldSeek + ProstT5**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.placeholder.svg)](https://doi.org/10.5281/zenodo.placeholder)

---

## Overview

AMRfold identifies AMR-associated proteins in bacterial proteomes through **structural similarity search**, recovering candidates invisible to conventional sequence-based methods. By encoding CARD protein homolog sequences into 3Di structural tokens via ProstT5 and searching against AlphaFold Database v6 proteomes using FoldSeek, AMRfold achieves a **3.7-fold gain** over the best sequence-based approach.

**Case study**: *Neisseria gonorrhoeae* FA 1090 — a WHO critical priority pathogen with escalating multi-drug resistance.

---

## Key Results

| Metric | Value |
|--------|-------|
| NEIG1 proteome coverage | 2,106 proteins |
| AMR structural hits (strict filters) | **299 (14.2%)** |
| Cryptic hits (<30% identity) | **272 (91.0%)** |
| High-confidence AF2 models (pLDDT >70) | 296/299 (99%) |
| Priority drug targets (no human homolog) | ~120 |
| PDB real-structure concordance | **100%** |

### Four-Method Comparison

| Method | Hits | % Proteome | Gain vs FoldSeek |
|--------|------|-----------|-----------------|
| MMseqs2 (sequence) | 71 | 3.4% | 4.2x fewer |
| DIAMOND BLASTp | 81 | 3.8% | 3.7x fewer |
| ESM2 pLM (cosine ≥0.85) | 120 | 5.7% | 2.5x fewer |
| **FoldSeek + ProstT5** | **299** | **14.2%** | — |
| PDB validation (10 templates) | — | — | 100% concordance |

---

## Pipeline

```
CARD v4.0.1 + MEGARes v3.0 (combined, 90% non-redundant)
        │
        ▼ ProstT5 (sequence → 3Di tokens, GPU)
        │
        ▼ FoldSeek easy-search
        │
NEIG1 AFDB v6 (2,106 CIF structures)
        │
        ▼ Filter: e < 1e-5, qcov ≥ 0.5, tcov ≥ 0.3
        │
        ▼ Annotate: CARD metadata + UniProt + KEGG + GO
        │
        ▼ Validate: pLDDT + PDB concordance + human screen
        │
   299 AMR structural hits + HTML report
```

---

## Usage

### Requirements

- Google Colab with T4 GPU (**recommended**) or local GPU with ≥12GB VRAM
- Runtime: ~50 minutes on T4

### Run

1. Open `notebooks/AMRfold_Complete_v2.ipynb` in Google Colab
2. Set Runtime → Change runtime type → **T4 GPU**
3. Run all cells sequentially (Ctrl+F9)
4. Download outputs from Cell 16

### Apply to another pathogen

Change one line in Cell 2:

```python
# Replace NEIG1 with your pathogen's AFDB proteome
('https://ftp.ebi.ac.uk/pub/databases/alphafold/v6/UP000000535_242231_NEIG1_v6.tar',
 'data/neisseria/NEIG1_v6.tar', 'NEIG1 AFDB v6'),
```

All AFDB v6 proteomes: `https://ftp.ebi.ac.uk/pub/databases/alphafold/v6/`

---

## Data Sources

| Source | Version | License | Note |
|--------|---------|---------|------|
| CARD | v4.0.1 | McMaster academic | Not redistributed |
| MEGARes | v3.0 | CC BY 4.0 | CARD + ResFinder + NDARO combined |
| AlphaFold DB | v6 | CC BY 4.0 | NEIG1 proteome UP000000535 |
| UniProt | 2024 | CC BY 4.0 | Annotation + KW-0046 cross-validation |
| ProstT5 | — | MIT | Via FoldSeek databases |

---

## Methodology Notes

### Asymmetric search (validated)
CARD sequences are converted to 3Di tokens via ProstT5 (predicted structural alphabet). NEIG1 target DB uses real AF2 CIF structures. This asymmetry is **validated** against 10 experimental PDB structures of known AMR proteins: 100% concordance between predicted and real structure-based search results.

### Scope
This pipeline covers **acquired resistance genes** (CARD protein homolog model + MEGARes). Chromosomal mutation-based resistance (e.g., *penA*, *gyrA*, *parC* in gonorrhea) requires the CARD variant model and is outside current scope.

### Known limitations
1. ProstT5 3Di prediction accuracy ~60-70% per residue — mitigated by PDB validation
2. FoldSeek and MMseqs2 e-values use different scoring — thresholds are indicative
3. ESM2 comparison uses cosine similarity threshold (not e-value) — not directly equivalent
4. KEGG pathway mapping partial (requires UniProt gene name annotation)
5. Coverage >1.0 cases capped at 1.0 (FoldSeek circular permutation behavior, documented)

---

## Output Files

| File | Description |
|------|-------------|
| `neig1_amr_final.tsv` | All 299 hits with full annotation |
| `amrfold_report.html` | Interactive HTML report |
| `amrfold_figures.png` | 9-panel analysis figure |
| `uniprot_cache.json` | UniProt annotations (gene, function, KEGG, GO) |
| `kegg_pathways.json` | KEGG pathway mappings |
| `provenance.json` | Full reproducibility metadata |

---

## Citation

If you use AMRfold, please cite:

```bibtex
@misc{pranavathiyani2026amrfold,
  title  = {AMRfold: Structure-informed mining of antimicrobial resistance
            determinants in Neisseria gonorrhoeae using proteome-wide
            FoldSeek search},
  author = {Pranavathiyani, Gnanasekar},
  year   = {2026},
  url    = {https://github.com/pranavathiyani/amrfold}
}
```

Also cite the underlying tools:
- FoldSeek: van Kempen et al. (2024) doi:10.1038/s41587-023-01773-0
- ProstT5: Heinzinger et al. (2024) doi:10.1093/nargab/lqae150
- CARD: Alcock et al. (2023) doi:10.1093/nar/gkac920
- MEGARes: Bonin et al. (2023) doi:10.1093/nar/gkac1047

---

## Author

**Pranavathiyani Gnanasekar**  
Assistant Professor (Research), Division of Bioinformatics  
SASTRA Deemed University, Thanjavur, India  
ORCID: [0000-0003-4854-8238](https://orcid.org/0000-0003-4854-8238)
