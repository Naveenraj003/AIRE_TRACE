param (
    [string]$DocxPath = "p:\Projects\AIRE-TRACE\AIRE-Trace_Universal_IEEE_Conference_Master.docx",
    [string]$PdfPath = "p:\Projects\AIRE-TRACE\scratch\test_word_export.pdf"
)

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($DocxPath)
    $pages = $doc.ComputeStatistics(2)
    $words = $doc.ComputeStatistics(0)
    Write-Host "Page count: $pages, Word count: $words"
    $doc.ExportAsFixedFormat($PdfPath, 17)
    $doc.Close([ref]0)
    $word.Quit()
    Write-Host "Exported to $PdfPath successfully."
} catch {
    Write-Host "Error: $_"
}
