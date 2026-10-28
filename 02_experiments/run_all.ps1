$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "p:\AIRE-TRACE"

Write-Host "===================================="
Write-Host "RUNNING GATE 2: PREPROCESSING"
Write-Host "===================================="
& .venv\Scripts\python.exe -m src.preprocessing.run_pipeline

Write-Host "===================================="
Write-Host "RUNNING GATE 3: BASELINE EXPERIMENTS"
Write-Host "===================================="
& .venv\Scripts\python.exe src\run_gate3_experiments.py

Write-Host "===================================="
Write-Host "RUNNING GATE 5/6: DOWNSTREAM ANALYSIS"
Write-Host "===================================="
& .venv\Scripts\python.exe src\run_gate6_analysis.py
& .venv\Scripts\python.exe src\run_gate6_2_analysis.py
& .venv\Scripts\python.exe src\run_gate6_3_analysis.py

Write-Host "===================================="
Write-Host "ALL REGENERATION GATES COMPLETED"
Write-Host "===================================="
