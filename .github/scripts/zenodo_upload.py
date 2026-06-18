#!/usr/bin/env python3
"""Upload a Quarto presentation to Zenodo.

Reads file list from {PRES_PATH}/zenodo.yml and metadata from {PRES_PATH}/CITATION.cff.
Triggered by GitHub Actions via the zenodo-publish workflow.

Sandbox mode  (ZENODO_SANDBOX=true):  creates and publishes on sandbox.zenodo.org
Production    (ZENODO_SANDBOX=false): creates a draft on zenodo.org — human reviews
                                      and clicks Publish to mint the DOI
"""

import os
import sys
import yaml
import requests
from pathlib import Path


def load_config(pres_path: Path) -> dict:
    with open(pres_path / "zenodo.yml") as f:
        return yaml.safe_load(f)


def load_citation(pres_path: Path) -> dict:
    with open(pres_path / "CITATION.cff") as f:
        return yaml.safe_load(f)


def cff_to_zenodo_metadata(cff: dict, config: dict) -> dict:
    creators = []
    for author in cff.get("authors", []):
        creator = {"name": f"{author['family-names']}, {author['given-names']}"}
        if "affiliation" in author:
            creator["affiliation"] = author["affiliation"]
        if "orcid" in author:
            creator["orcid"] = author["orcid"].replace("https://orcid.org/", "")
        creators.append(creator)

    related = []
    if "url" in cff:
        related.append({"identifier": cff["url"], "relation": "isSupplementTo", "scheme": "url"})
    if "repository-code" in cff:
        related.append({"identifier": cff["repository-code"], "relation": "isSupplementTo", "scheme": "url"})

    metadata = {
        "upload_type":      config.get("upload_type", "presentation"),
        "title":            cff["title"],
        "creators":         creators,
        "description":      cff.get("abstract", "").strip(),
        "access_right":     "open",
        "license":          cff.get("license", "CC-BY-4.0").lower(),
        "keywords":         cff.get("keywords", []),
        "publication_date": str(cff.get("date-released", "")),
    }

    if related:
        metadata["related_identifiers"] = related

    if "conference" in cff:
        metadata["conference_title"] = cff["conference"]["name"]

    # Default: submit every deposit to the UC OSPO Network Zenodo community.
    # A community curator approves the request. A presentation can override this
    # via `communities` in its zenodo.yml metadata_overrides.
    metadata["communities"] = [{"identifier": "uc-ospo-net"}]

    # Per-presentation Zenodo overrides (conference_url, conference_dates, notes, etc.)
    metadata.update(config.get("metadata_overrides", {}))

    return metadata


def create_deposition(base_url: str, headers: dict) -> tuple:
    r = requests.post(
        f"{base_url}/api/deposit/depositions",
        headers={**headers, "Content-Type": "application/json"},
        json={},
    )
    r.raise_for_status()
    data = r.json()
    return data["id"], data["links"]["bucket"]


def upload_file(bucket_url: str, file_path: Path, headers: dict) -> None:
    print(f"  uploading {file_path.name} ({file_path.stat().st_size // 1024} KB)")
    with open(file_path, "rb") as f:
        r = requests.put(f"{bucket_url}/{file_path.name}", headers=headers, data=f)
    r.raise_for_status()


def set_metadata(base_url: str, deposition_id: int, metadata: dict, headers: dict) -> None:
    r = requests.put(
        f"{base_url}/api/deposit/depositions/{deposition_id}",
        headers={**headers, "Content-Type": "application/json"},
        json={"metadata": metadata},
    )
    if not r.ok:
        print(f"set_metadata failed {r.status_code}: {r.text}")
    r.raise_for_status()


def publish(base_url: str, deposition_id: int, headers: dict) -> str:
    r = requests.post(
        f"{base_url}/api/deposit/depositions/{deposition_id}/actions/publish",
        headers=headers,
    )
    if not r.ok:
        print(f"publish failed {r.status_code}: {r.text}")
    r.raise_for_status()
    return r.json().get("doi", "")


def main():
    sandbox = os.environ.get("ZENODO_SANDBOX", "false").lower() == "true"

    if sandbox:
        token = os.environ.get("ZENODO_SANDBOX_TOKEN")
        base_url = "https://sandbox.zenodo.org"
    else:
        token = os.environ.get("ZENODO_TOKEN")
        base_url = "https://zenodo.org"

    if not token:
        token_var = "ZENODO_SANDBOX_TOKEN" if sandbox else "ZENODO_TOKEN"
        print(f"Error: {token_var} is not set", file=sys.stderr)
        sys.exit(1)

    pres_path = Path(os.environ.get("PRES_PATH", "."))
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Target:       {'sandbox.zenodo.org' if sandbox else 'zenodo.org'}")
    print(f"Presentation: {pres_path}")

    config = load_config(pres_path)
    cff = load_citation(pres_path)
    metadata = cff_to_zenodo_metadata(cff, config)

    print(f"Title:        {metadata['title']}")
    print()

    print("Creating deposition...")
    deposition_id, bucket_url = create_deposition(base_url, headers)
    print(f"  ID: {deposition_id}")

    print("Uploading files...")
    missing = []
    for filename in config.get("files", []):
        file_path = pres_path / filename
        if file_path.exists():
            upload_file(bucket_url, file_path, headers)
        else:
            missing.append(filename)
            print(f"  warning: {filename} not found, skipping")

    if missing:
        print(f"\nSkipped {len(missing)} missing file(s): {', '.join(missing)}")

    print("Setting metadata...")
    set_metadata(base_url, deposition_id, metadata, headers)

    if sandbox:
        print("Publishing (sandbox)...")
        doi = publish(base_url, deposition_id, headers)
        print(f"\nDone. Sandbox DOI: {doi}")
        print(f"URL: {base_url}/record/{deposition_id}")
    else:
        print(f"\nDraft created. Review and publish at:")
        print(f"  {base_url}/deposit/{deposition_id}")
        print("The DOI will be minted when you click Publish.")


if __name__ == "__main__":
    main()
