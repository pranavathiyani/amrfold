"""
Step 2: Map GenBank protein accessions to UniProt accessions.
Uses UniProt ID Mapping API (free, no auth required).
Results cached - safe to re-run if interrupted.
"""

import json
import time
import requests
from pathlib import Path

DATA_DIR  = Path(__file__).parent.parent / "data" / "card"
CACHE     = DATA_DIR / "genbank_to_uniprot.json"
BATCH     = 500
SLEEP     = 1.0

API_SUBMIT = "https://rest.uniprot.org/idmapping/run"
API_STATUS = "https://rest.uniprot.org/idmapping/status/{job}"
API_RESULT = "https://rest.uniprot.org/idmapping/stream/{job}"

def load_cache():
    if CACHE.exists():
        c = json.loads(CACHE.read_text())
        print(f"Cache loaded: {len(c)} mapped so far")
        return c
    return {}

def save_cache(mapping):
    CACHE.write_text(json.dumps(mapping, indent=2))

def submit_batch(accs):
    r = requests.post(API_SUBMIT, data={
        "from": "EMBL-GenBank",
        "to":   "UniProtKB",
        "ids":  ",".join(accs),
    }, timeout=30)
    r.raise_for_status()
    return r.json()["jobId"]

def poll(job_id):
    for _ in range(60):
        r = requests.get(API_STATUS.format(job=job_id), timeout=30)
        r.raise_for_status()
        status = r.json()
        if "results" in status or status.get("jobStatus") == "FINISHED":
            return True
        if status.get("jobStatus") == "FAILED":
            return False
        time.sleep(SLEEP)
    return False

def fetch_results(job_id):
    r = requests.get(API_RESULT.format(job=job_id), timeout=60)
    r.raise_for_status()
    data = r.json()
    mapping = {}
    for item in data.get("results", []):
        gb  = item["from"]
        uni = item["to"]["primaryAccession"]
        mapping[gb] = uni
    return mapping

def run():
    args     = json.loads((DATA_DIR / "args_filtered.json").read_text())
    all_accs = list({a["protein_acc"] for a in args})
    cache    = load_cache()

    todo = [a for a in all_accs if a not in cache]
    print(f"Total: {len(all_accs)} | Already mapped: {len(cache)} | Todo: {len(todo)}")

    for i in range(0, len(todo), BATCH):
        batch = todo[i:i+BATCH]
        print(f"Batch {i//BATCH + 1}: submitting {len(batch)} accessions...")
        try:
            job_id = submit_batch(batch)
            if poll(job_id):
                result = fetch_results(job_id)
                cache.update(result)
                save_cache(cache)
                print(f"  Mapped {len(result)} in this batch")
            else:
                print(f"  Batch failed, skipping")
        except Exception as e:
            print(f"  Error: {e}, skipping batch")
        time.sleep(SLEEP)

    mapped   = {k: v for k, v in cache.items() if v}
    unmapped = [a for a in all_accs if a not in mapped]

    print(f"\nFinal: {len(mapped)} mapped | {len(unmapped)} unmapped")
    print(f"Cache saved: {CACHE}")

    # Save unmapped list for ESMFold fallback later
    (DATA_DIR / "unmapped_accs.json").write_text(
        json.dumps(unmapped, indent=2)
    )
    print(f"Unmapped saved: {DATA_DIR}/unmapped_accs.json")

if __name__ == "__main__":
    run()
