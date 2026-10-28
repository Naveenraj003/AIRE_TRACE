$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open('P:\Projects\AIRE-TRACE\AIRE_Trace__A_Standardized_Prospective_Evaluation_and_Trajectory_Risk_Decomposition_Framework_for_Online_Agent_Failure_Warning__12_.docx')
    $pages = $doc.ComputeStatistics(2)
    Write-Host "Page count in Word: $pages"
    $doc.ExportAsFixedFormat('P:\Projects\AIRE-TRACE\05_archive\scratch\test_word_export_4auth.pdf', 17)
    Write-Host "Exported to scratch PDF"
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
