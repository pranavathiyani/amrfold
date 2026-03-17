"""
Step 1: Download and parse CARD v4.x data.
Parses protein_fasta_protein_homolog_model.fasta + aro_index.tsv
CARD data is NOT committed to git per McMaster license.
"""

import csv
import json
import tarfile
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CARD_VERSION = "4.0.1"
CARD_URL = f"https://card.mcmaster.ca/download/0/broadstreet-v{CARD_VERSION}.tar.bz2"
DATA_DIR = Path(__file__).parent.parent / "data" / "card"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TARBALL = DATA_DIR / "card.tar.bz2"

def download():
    if TARBALL.exists():
        print(f"Tarball exists, skipping download.")
        md5 = hashlib.md5(TARBALL.read_bytes()).hexdigest()
        return md5
    print(f"Downloading CARD v{CARD_VERSION}...")
    urllib.request.urlretrieve(CARD_URL, TARBALL)
    md5 = hashlib.md5(TARBALL.read_bytes()).hexdigest()
    print(f"Downloaded (md5: {md5})")
    return md5

def extract():
    fasta = DATA_DIR / "protein_fasta_protein_homolog_model.fasta"
    if fasta.exists():
        print("Already extracted, skipping.")
        return
    print("Extracting...")
    with tarfile.open(TARBALL, "r:bz2") as tf:
        tf.extractall(DATA_DIR)
    print("Extracted.")

def parse_aro_index():
    """Build ARO -> metadata dict from aro_index.tsv"""
    aro_meta = {}
    with open(DATA_DIR / "aro_index.tsv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            aro = row["ARO Accession"].strip()
            aro_meta[aro] = {
                "gene_family": row.get("AMR Gene Family", "").strip(),
                "drug_class":  row.get("Drug Class", "").strip(),
                "mechanism":   row.get("Resistance Mechanism", "").strip(),
                "short_name":  row.get("CARD Short Name", "").strip(),
            }
    print(f"Loaded metadata for {len(aro_meta)} ARO entries")
    return aro_meta

def parse_fasta(aro_meta):
    """
    Parse protein homolog model FASTA.
    Header: >gb|PROTEIN_ACC|ARO:XXXXXXX|GENE_NAME [organism]
    """
    fasta = DATA_DIR / "protein_fasta_protein_homolog_model.fasta"
    args = []
    skipped = 0

    with open(fasta, encoding="utf-8") as f:
        for line in f:
            if not line.startswith(">"):
                continue
            header = line[1:].strip()
            parts = header.split("|")
            if len(parts) < 3:
                skipped += 1
                continue

            protein_acc = parts[1].strip()
            aro_field   = parts[2].strip()          # e.g. ARO:3002999
            name_org    = parts[3] if len(parts) > 3 else ""
            gene_name   = name_org.split("[")[0].strip()

            if not aro_field.startswith("ARO:"):
                skipped += 1
                continue

            meta = aro_meta.get(aro_field, {})
            args.append({
                "aro":         aro_field,
                "name":        gene_name,
                "protein_acc": protein_acc,
                "gene_family": meta.get("gene_family", ""),
                "drug_class":  meta.get("drug_class", ""),
                "mechanism":   meta.get("mechanism", ""),
                "short_name":  meta.get("short_name", ""),
            })

    print(f"Parsed {len(args)} protein homolog model ARGs ({skipped} skipped)")
    return args

def write_outputs(args, md5):
    out = DATA_DIR / "args_filtered.json"
    with open(out, "w") as f:
        json.dump(args, f, indent=2)

    prov = {
        "card_version":  CARD_VERSION,
        "download_url":  CARD_URL,
        "download_date": datetime.now(timezone.utc).isoformat(),
        "n_args":        len(args),
        "md5":           md5,
        "source_file":   "protein_fasta_protein_homolog_model.fasta",
    }
    with open(DATA_DIR / "provenance.json", "w") as f:
        json.dump(prov, f, indent=2)

    print(f"Written: {out}")
    print(f"Written: {DATA_DIR}/provenance.json")

if __name__ == "__main__":
    md5      = download()
    extract()
    aro_meta = parse_aro_index()
    args     = parse_fasta(aro_meta)
    write_outputs(args, md5)
    print("Step 1 complete.")
