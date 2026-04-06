# AMRfold

**Structure-informed proteome-wide AMR mining using ProstT5 + Foldseek**

[![DOI](https://img.shields.io/badge/bioRxiv-preprint-blue)](https://github.com/pranavathiyani/amrfold)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pranavathiyani/amrfold/blob/main/AMRfold_Complete_v3.2.ipynb)

AMRfold mines antimicrobial resistance (AMR) proteins from bacterial proteomes by converting protein sequences into 3Di structural alphabet tokens via **ProstT5** and searching against a curated AMR query database using **Foldseek**. Unlike sequence-based methods, AMRfold detects structurally conserved AMR homologs with no detectable sequence signal.

---

## Key Results — *Neisseria gonorrhoeae* FA 1090

| Metric | Value |
|--------|-------|
| **Unique proteins detected** | **412 (19.6% of proteome)** |
| vs DIAMOND BLASTp | **3.2× more** |
| vs MMseqs2 | **2.8× more** |
| vs AMRFinderPlus HMM | **3.8× more** |
| vs ESM2 (stat. calibrated) | **12.1× more** |
| Cryptic hits (<30% identity) | **346 (84.0%)** |
| High-confidence models (pLDDT >70) | **402/412 (97.6%)** |
| Priority drug targets (no human homolog) | **225 (54.6%)** |
| Exclusive to structural search | **263 (63.8%)** |
| PDB TM-score mean | **0.804** |
| Homology probability | **1.000 (374/374)** |

---

## Methodology

```
CARD v4.0.1 + UniProt SwissProt KW-0046 bacteria
         ↓ CD-HIT 90% identity
  2,226 non-redundant AMR query proteins
         ↓ ProstT5
  3Di structural alphabet tokens
         ↓ Foldseek (s=9.5)
  AFDB v6 N. gonorrhoeae FA 1090 proteome (2,106 structures)
         ↓ e<1e-5, qcov≥0.5, tcov≥0.3
  412 structural AMR hits
```

**Five-method comparison:**

| Method | Paradigm | Hits |
|--------|----------|------|
| MMseqs2 | Sequence alignment | 145 |
| DIAMOND BLASTp | Sequence alignment | 130 |
| ESM2 (p=1e-5, calibrated) | Sequence embedding | 34 |
| AMRFinderPlus HMM | Profile HMM | 108 |
| **Foldseek+ProstT5 (AMRfold)** | **Structure** | **412** |

---

## Quick Start

### Google Colab (recommended)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pranavathiyani/amrfold/blob/main/AMRfold_Complete_v3.2.ipynb)

Requires: Google account + Google Drive (for checkpoints). T4 GPU recommended.
Runtime: ~90 min for Session 1 (Foldseek search), ~60 min for Session 2 (analysis).

### Local installation

```bash
# Install dependencies
pip install pyhmmer umap-learn scikit-learn scipy statsmodels goatools

# Install Foldseek + MMseqs2
wget -q https://mmseqs.com/foldseek/foldseek-linux-gpu.tar.gz && tar -xzf foldseek-linux-gpu.tar.gz
wget -q https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz && tar -xzf mmseqs-linux-avx2.tar.gz

# Install DIAMOND
wget -q https://github.com/bbuchfink/diamond/releases/download/v2.1.8/diamond-linux64.tar.gz && tar -xzf diamond-linux64.tar.gz

# Run notebook
jupyter notebook AMRfold_Complete_v3.2.ipynb
```

---

## Repository Structure

```
amrfold/
├── notebooks/
│   ├── AMRfold_Complete_v3.2.ipynb   # Main pipeline notebook
│   └── archive/                       # Previous versions (v2.1–v3.1)
├── results/
│   ├── neig1_amr_best.tsv             # Best hit per NEIG1 protein (412 rows)
│   ├── neig1_amr_all_domains.tsv      # All hits with domain analysis
│   ├── amrfinder_out.tsv              # AMRFinderPlus HMM hits (108)
│   ├── cluster_membership.tsv         # Query DB cluster membership
│   ├── umap_embedding.tsv             # UMAP coordinates (2,638 points)
│   ├── kegg_pathways.json             # KEGG pathway mappings
│   ├── provenance.json                # Complete run metadata + versions
│   ├── uniprot_cache.json             # UniProt annotation cache
│   ├── amrfold_report.html            # Full interactive HTML report
│   ├── amrfold_combined_9panel.png    # Combined 9-panel figure
│   ├── A_method_comparison.png        # Five-method bar chart
│   ├── B_venn_foldseek_diamond.png    # Foldseek vs DIAMOND Venn
│   ├── C_sequence_identity.png        # Identity distribution
│   ├── D_plddt_distribution.png       # AlphaFold2 confidence
│   ├── E_gene_families.png            # Top AMR gene families
│   ├── F_mechanisms.png               # Resistance mechanisms pie
│   ├── G_drug_targets.png             # Priority targets bar
│   ├── H_evalue_distribution.png      # E-value distribution
│   ├── I_kegg_pathways.png            # Top KEGG pathways
│   ├── J_esm2_null_distribution.png   # ESM2 null calibration
│   ├── K_coverage_identity_heatmap.png # Coverage-identity matrix
│   ├── L_umap_amr_space.png           # UMAP 3-panel
│   ├── M_pdb_tmscore.png              # PDB TM-score distribution
│   ├── N_go_enrichment.png            # GO enrichment
│   ├── O_kegg_completeness.png        # KEGG pathway completeness
│   └── P_upset_method_overlap.png     # UpSet plot — all intersections
├── README.md
└── CITATION.cff
```

---

## Pipeline Cells

| Cell | Description | Runtime |
|------|-------------|---------|
| 0 | Drive mount + CONFIG | 1 min |
| 1 | Install tools + pyhmmer + AMR.LIB | 5 min |
| 2 | Download CARD, SwissProt, NEIG1 AFDB, human proteome | 5 min |
| 3 | Extract structures + ProstT5 weights | 5 min |
| 4 | Build combined AMR query DB (2,226 NR sequences) | 2 min |
| 5a | **Foldseek GPU search** (13,490 raw hits → 412 strict) | 9 min |
| 5b | MMseqs2 + DIAMOND + human screen (parallel) | 5 min |
| 5c | AMRFinderPlus HMM via pyhmmer (108 hits) | 1 min |
| 6 | ESM2 null calibration + search (34 hits, p=1e-5) | 10 min |
| 7 | Parse + filters + sanity checks | 1 min |
| 8 | Hybrid CARD/SwissProt annotation | 1 min |
| 9 | Multi-domain analysis | 1 min |
| 10 | UniProt annotation (12 workers) | 3 min |
| 10b | GOA FTP download + KEGG conv mapping | 3 min |
| 11 | pLDDT + 25 PDB structural validation | 5 min |
| 12 | Coverage-identity matrix | 1 min |
| 13 | GO enrichment (Fisher+BH) + KEGG completeness | 5 min |
| 14 | UMAP (cosine, seed=142857) | 10 min |
| 15 | Five-way comparison table | 1 min |
| 16 | Save all results + provenance | 1 min |
| 17 | 15 individual figures (300 DPI) | 3 min |
| 18 | Combined 9-panel figure | 1 min |
| 19 | HTML + PDF report | 2 min |
| 20 | Download all outputs | 1 min |

**Session strategy:** Session 1 = Cells 0–5a (~40 min, saves Foldseek checkpoint). Session 2 = load checkpoints, Cells 5b–20 (~90 min).

---

## Databases

| Database | Version | Sequences | Use |
|----------|---------|-----------|-----|
| CARD protein homolog | v4.0.1 | 6,052 | AMR query |
| UniProt SwissProt KW-0046 bacteria | March 2026 | 2,283 | AMR query |
| Combined query (90% NR) | — | **2,226** | Final query |
| AFDB v6 NEIG1 | v6 | **2,106** | Target |
| Human SwissProt | March 2026 | 20,416 | Human screen |
| AMRFinderPlus AMR.LIB | March 2026 | 780 HMMs | Comparator |

---

## Scientific Findings

**84% cryptic AMR reservoir:** 346 of 412 detected proteins have <30% sequence identity to their best AMR query match yet maintain full-length structural similarity (75% with tcov >90%). These would be entirely missed by sequence-based methods.

**ESM2 embedding space does not cluster by AMR mechanism** (silhouette = -0.129), confirming that cosine similarity in embedding space is insufficient for AMR mining and justifying structural search.

**Cell wall and efflux pathways significantly enriched:** KEGG pathway analysis maps structural hits to peptidoglycan biosynthesis (71% completeness) and LPS biosynthesis (75% completeness). GO enrichment identifies 28 significant terms including porin functions and rRNA methyltransferases.

**225 priority drug targets** with no significant human homologs, representing the highest-confidence candidates for *N. gonorrhoeae*-specific therapeutic development.

---

## Technical Notes

- **AMRFinderPlus** is run via `pyhmmer` (pure Python HMMER) rather than the NCBI binary, which requires libstdc++≥3.4.32 not available on Colab. The HMM-only approach is scientifically justified as the BLAST component recovers predominantly high-identity hits already captured by DIAMOND and MMseqs2.
- **ESM2 threshold** is statistically calibrated from a null distribution of 10,000 random NEIG1-NEIG1 protein pairs (p=1e-5, seed=142857), not set arbitrarily.
- **Reproducibility seed:** 142857 (cyclic number, 1/7 = 0.142857...).
- **Claude AI disclosure:** Code generation assisted by Claude (Anthropic) per author's disclosure policy.

---

## Citation

If you use AMRfold, please cite:

> Gnanasekar Pranavathiyani (2026) Structure-informed proteome-wide mining of antimicrobial resistance determinants in *Neisseria gonorrhoeae* using structural similarity search. <!-- *BGRS/SB-2026 Conference Proceedings*. doi:10.18699/bgrs2026-[assigned] -->

### Key dependencies to cite:

- van Kempen M. et al. (2024) Fast and accurate protein structure search with Foldseek. *Nature Biotechnology*. doi:10.1038/s41587-023-01773-0
- Heinzinger M. et al. (2024) Bilingual language model for protein sequence and structure. *NAR Genomics and Bioinformatics*. doi:10.1093/nargab/lqae150
- Alcock B. et al. (2023) CARD 2023. *Nucleic Acids Research*. doi:10.1093/nar/gkac920
- UniProt Consortium (2025). *Nucleic Acids Research*. doi:10.1093/nar/gkae1010

---

## Author

**Pranavathiyani G** (ORCID: [0000-0003-4854-8238](https://orcid.org/0000-0003-4854-8238))  
Assistant Professor (Research), Division of Bioinformatics  
SASTRA Deemed University, Thanjavur, Tamil Nadu, India  
pranavathiyani@scbt.sastra.edu

---

## License

MIT License — see [LICENSE](LICENSE) for details.
