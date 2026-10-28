import docx
import re
import os

def replace_text_in_paragraph(paragraph, replacements):
    for key, val in replacements.items():
        if key in paragraph.text:
            # Simple replacement by clearing runs and adding new text
            # to preserve the paragraph style. We will try to preserve the style of the first run.
            if paragraph.runs:
                first_run = paragraph.runs[0]
                style = first_run.style
                font = first_run.font
                bold = first_run.bold
                italic = first_run.italic
                underline = first_run.underline
                
                new_text = paragraph.text.replace(key, val)
                for run in paragraph.runs:
                    run.text = ""
                new_run = paragraph.add_run(new_text)
                new_run.bold = bold
                new_run.italic = italic
                new_run.underline = underline
                if font.name:
                    new_run.font.name = font.name
                if font.size:
                    new_run.font.size = font.size

def replace_in_doc(doc_path, output_path, replacements):
    doc = docx.Document(doc_path)
    
    for p in doc.paragraphs:
        replace_text_in_paragraph(p, replacements)
        
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    replace_text_in_paragraph(p, replacements)
                    
    doc.save(output_path)
    print(f"Saved {output_path}")

front_replacements = {
    "AIRGENIX: A GEOSPATIAL MACHINE LEARNING FRAMEWORK FOR PROXY-BASED AIR POLLUTION SOURCE CLASSIFICATION": "AIRE-TRACE: A STANDARDIZED PROSPECTIVE EVALUATION AND TRAJECTORY RISK DECOMPOSITION FRAMEWORK FOR ONLINE AGENT FAILURE WARNING",
    "PAVITHRAN G": "NAVEEN RAJ B",
    "2303737714821029": "2303737714821026",
    "PRAVEEN S": "KRISHNAMOORTHI P",
    "2303737714821030": "2303737714821018",
    "Ms. R. P. HARSHINI, AP": "Ms. JANANI C",
    "Ms. R. P. HARSHINI": "Ms. JANANI C"
}

front_page_path = r"p:\Projects\AIRE-TRACE\Report\Review_1\front-page.docx"
out_front_page = r"p:\Projects\AIRE-TRACE\Report\Review_1\AIRE_Trace_front_page.docx"

replace_in_doc(front_page_path, out_front_page, front_replacements)

# For the review content, it's more complex since we want to replace whole algorithms and sections.
# Let's try replacing exact block headers and their following texts.
# Wait, replacing big blocks via string replacement is hard because the template has multiple paragraphs.
# Let's clear the document and rewrite it using the styles from the template.

def rewrite_review_content(template_path, output_path):
    doc = docx.Document(template_path)
    
    # Save styles we want to use (if they exist), else use defaults
    # Let's just clear all paragraphs and tables
    for p in doc.paragraphs:
        p_element = p._element
        p_element.getparent().remove(p_element)
    for tbl in doc.tables:
        tbl_element = tbl._element
        tbl_element.getparent().remove(tbl_element)
        
    # Now we write AIRE-TRACE content
    doc.add_heading('Algorithm 1: Heuristic Baseline (H)', level=2)
    doc.add_paragraph('INPUT: execution trace up to time t, simple rules')
    doc.add_paragraph('1. Check for specific tool errors or retry loops in the prefix.')
    doc.add_paragraph('2. Apply deterministic rule-based mapping to predict failure.')
    doc.add_paragraph('3. Output prediction without requiring training.')
    doc.add_paragraph('OUTPUT: predicted operational success/failure risk')
    
    doc.add_heading('Algorithm 2: Classical ML Classification (M)', level=2)
    doc.add_paragraph('INPUT: feature matrix X from canonical prefixes, labels y')
    doc.add_paragraph('1. Flatten the feature sequence at checkpoint t.')
    doc.add_paragraph('2. Calculate the aggregated feature vector (retry counts, tool errors).')
    doc.add_paragraph('3. Train Logistic Regression or XGBoost using episode-balanced sample weighting.')
    doc.add_paragraph('4. Predict risk using the trained classifier.')
    doc.add_paragraph('OUTPUT: predicted risk and model confidence')

    doc.add_heading('Algorithm 3: Sequence Model Classification (S)', level=2)
    doc.add_paragraph('INPUT: ordered feature sequence up to time t, labels y')
    doc.add_paragraph('1. Pass the sequence into a small GRU/1D-CNN.')
    doc.add_paragraph('2. Capture the temporal dependencies of the agent trajectory.')
    doc.add_paragraph('3. Use the final hidden state to predict the risk of failure.')
    doc.add_paragraph('OUTPUT: temporal risk prediction')

    doc.add_heading('SYSTEM DESIGN AND MODULE DEVELOPMENT', level=1)
    doc.add_heading('1. SYSTEM DESIGN', level=2)
    p = doc.add_paragraph()
    p.add_run('The AIRE-Trace system follows a strict, pipeline-driven design for standardized prospective evaluation. ')
    p.add_run('The pipeline consists of Ingestion, Outcome Mapping, Sanitization, Episode-level Splitting, ')
    p.add_run('Prefix Generation, Feature Extraction, Model Training, Threshold Calibration, and a Common Evaluator. ')
    p.add_run('This ensures no leakage between train/test splits and maintains an outcome-independent checkpoint policy.')
    
    doc.add_heading('2. MODULE DEVELOPMENT', level=2)
    doc.add_paragraph('Ingestion module: Reads raw source files and produces Run and Event structures in a canonical schema.')
    doc.add_paragraph('Outcome Mapping module: Maps native dataset outcomes to a unified eventual_success/failure boolean flag.')
    doc.add_paragraph('Sanitization module: Strips terminal events that might disclose the episode outcome to monitors.')
    doc.add_paragraph('Prefix Generation module: Generates prefixes using an outcome-independent checkpoint policy.')
    doc.add_paragraph('Feature Extraction module: Extracts common, cross-dataset compatible features safely without leakage.')
    doc.add_paragraph('Threshold Calibration module: Calibrates and freezes thresholds on calibration episodes only.')
    doc.add_paragraph('Evaluation module: Computes metrics (AUROC, AUPRC, FAR, Recall@FAR) and handles statistical bootstrapping.')
    
    doc.add_heading('REFERENCES', level=1)
    doc.add_paragraph('[1] AIRE-Trace_Frozen_Protocol_and_Plan.md - Authoritative scientific protocol for AIRE-Trace.')
    doc.add_paragraph('[2] Tracebench and tau-bench corpora documentation.')
    
    doc.add_heading('SUMMARY', level=1)
    p2 = doc.add_paragraph()
    p2.add_run('AIRE-Trace provides a standardized prospective evaluation and trajectory risk decomposition framework. ')
    p2.add_run('The project combines canonical dataset ingestion, rule-defined feature extraction, evaluates classical ')
    p2.add_run('and sequence-based algorithms, and ensures strict leakage guards. The methodology provides a robust foundation ')
    p2.add_run('for comparing AI-agent failure-warning methods on recorded execution trajectories without post-hoc tuning.')

    doc.save(output_path)
    print(f"Saved {output_path}")

content_template_path = r"p:\Projects\AIRE-TRACE\Report\Review_1\AirGenix_Project_Review_Content.docx"
out_content = r"p:\Projects\AIRE-TRACE\Report\Review_1\AIRE_Trace_Project_Review_Content.docx"
rewrite_review_content(content_template_path, out_content)
