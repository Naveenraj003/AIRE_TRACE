$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = "P:\Projects\AIRE-TRACE\AIRE_Trace__A_Standardized_Prospective_Evaluation_and_Trajectory_Risk_Decomposition_Framework_for_Online_Agent_Failure_Warning__12_.docx"
    $doc = $word.Documents.Open($docPath)
    $pages = $doc.ComputeStatistics(2)
    Write-Host "Page count in Word: $pages"
    
    $pdfPath = "P:\Projects\AIRE-TRACE\05_archive\scratch\test_word_export.pdf"
    $doc.ExportAsFixedFormat($pdfPath, 17) # 17 = wdExportFormatPDF
    Write-Host "Exported PDF to: $pdfPath"
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
