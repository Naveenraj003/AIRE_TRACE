import pymupdf
import hashlib
import re

pdf_path = "AIRE-Trace_IEEE.pdf"

with open(pdf_path, "rb") as f:
    sha256 = hashlib.sha256(f.read()).hexdigest()
print(f"PDF SHA-256: {sha256}")

doc = pymupdf.open(pdf_path)
text = "".join(page.get_text() for page in doc)

# Normalize text
text = text.replace('\ufb01', 'fi').replace('\ufb02', 'fl')
# Replace newlines with spaces for easier phrase matching
text_normalized = re.sub(r'\s+', ' ', text)

assert "AIRE-Trace: A Standardized Prospective Evaluation Protocol" in text_normalized, "Not the AIRE-Trace manuscript"
assert "Deepfake" not in text_normalized, "Contains Deepfake text"

# Verify models
assert "H1, H2, H3, H4, M1, S1, S2" in text_normalized, "Missing exact model set"
assert "XGBoost" not in text_normalized, "XGBoost still in PDF"
assert "1D-CNN" not in text_normalized, "1D-CNN still in PDF"

# K=30 count - we look in the original text (without spaces collapsed) to ensure exact matches
k30_count = text.count("K=30")
assert k30_count == 3, f"Expected 3 occurrences of K=30, found {k30_count}"

assert "0.7667" in text_normalized, "PDC 0.7667 missing"
assert "416" in text_normalized, "416 TEST missing"
assert "257" in text_normalized, "257 valid failure episodes missing"
assert "0.6371" in text_normalized, "0.6371 missing"
assert "0.5074" in text_normalized, "0.5074 missing"
assert "0.0000" in text_normalized, "0.0000 missing"
assert "0.5302" in text_normalized, "0.5302 missing"
assert "3,339" in text_normalized or "3339" in text_normalized, "3339 missing"
assert "19.84" in text_normalized, "19.84% missing"
assert "51" in text_normalized, "51 missing"

assert "TODO" not in text_normalized, "TODO found"
assert "PLACEHOLDER" not in text_normalized, "PLACEHOLDER found"
assert "SOURCE TEXT REQUIRED" not in text_normalized, "SOURCE TEXT REQUIRED found"

# Check mode B string (allow for slight formatting differences)
mode_b_pattern = r"Mode B represents protocol capability and context only.*does not form part of the reported experimental evidence"
assert re.search(mode_b_pattern, text_normalized), "Mode B semantics missing"

sections = ["Abstract", "Methodology", "Results", "Reproducibility Statement", "References"]
for sec in sections:
    assert sec in text_normalized, f"Section {sec} missing"

print("PDF Verification Passed Successfully!")
