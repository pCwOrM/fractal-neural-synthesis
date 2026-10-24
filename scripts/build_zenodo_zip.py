import os
import zipfile

def create_bundle():
    pkg_dir = os.path.join(os.path.dirname(__file__), "..", "zenodo_oev_liquidation_package")
    zip_path = os.path.join(pkg_dir, "zenodo_bundle_oev_liquidation_empirical_research.zip")

    files_to_zip = [
        ("Empirical_OEV_and_Liquidation_Dynamics_Research_Monograph.pdf", "Empirical_OEV_and_Liquidation_Dynamics_Research_Monograph.pdf"),
        ("EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md", "EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md"),
        ("data/werracle_oev_empirical_dataset_2026.json", "data/werracle_oev_empirical_dataset_2026.json"),
        ("data/checksums.sha256", "data/checksums.sha256"),
        ("scripts/verify_dataset_metrics.py", "scripts/verify_dataset_metrics.py"),
        ("scripts/audit_multicall_bundle.py", "scripts/audit_multicall_bundle.py"),
    ]

    print(f"Creating zip bundle: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for src_rel, arcname in files_to_zip:
            src_full = os.path.join(pkg_dir, src_rel)
            if os.path.exists(src_full):
                zf.write(src_full, arcname=arcname)
                print(f"  + Added: {arcname} ({os.path.getsize(src_full):,} bytes)")
            else:
                print(f"  ! Missing: {src_full}")

    print(f"Successfully generated zip archive: {os.path.getsize(zip_path):,} bytes")

if __name__ == "__main__":
    create_bundle()
