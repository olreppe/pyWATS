# PowerShell script to update additional example files to use enum members instead of strings

$files = @(
    "examples\converters\converter_template.py",
    "examples\domains\production_examples.py",
    "examples\report\create_uut_report.py"
)

foreach ($file in $files) {
    $fullPath = Join-Path (Get-Location) $file
    
    if (Test-Path $fullPath) {
        Write-Host "Processing: $file" -ForegroundColor Cyan
        
        $content = Get-Content $fullPath -Raw
        
        # Replace status="Passed" with status=StepStatus.Passed
        $content = $content -replace 'status\s*=\s*"Passed"', 'status=StepStatus.Passed'
        
        # Replace status="Failed" with status=StepStatus.Failed
        $content = $content -replace 'status\s*=\s*"Failed"', 'status=StepStatus.Failed'
        
        # Replace conditional expressions: "Passed" if x else "Failed"
        $content = $content -replace '"Passed"\s+if\s+', 'StepStatus.Passed if '
        $content = $content -replace '\s+else\s+"Failed"', ' else StepStatus.Failed'
        
        # Replace ternary "P" if x else "F"
        $content = $content -replace '"P"\s+if\s+', 'StepStatus.Passed.value if '
        $content = $content -replace '\s+else\s+"F"', ' else StepStatus.Failed.value'
        
        # Save the updated content
        Set-Content -Path $fullPath -Value $content -NoNewline
        
        Write-Host "  Updated OK" -ForegroundColor Green
    } else {
        Write-Host "  File not found: $fullPath" -ForegroundColor Red
    }
}

Write-Host "Done! Updated files." -ForegroundColor Green
