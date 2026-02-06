# Script to replace string status values with enum members

$files = @(
    "examples\report\report_builder_examples.py",
    "examples\converters\csv_converter.py",
    "examples\converters\xml_converter.py",
    "src\pywats\tools\report_builder.py",
    "src\pywats_client\converters\models.py",
    "src\pywats_client\converters\standard\klippel_converter.py",
    "tests\integration\test_boxbuild.py",
    "tests\domains\rootcause\test_d8_workflow.py",
    "tests\domains\report\test_workflow.py"
)

foreach ($file in $files) {
    $fullPath = Join-Path "c:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS" $file
    if (Test-Path $fullPath) {
        Write-Host "Processing: $file"
        
        # Read content
        $content = Get-Content $fullPath -Raw
        
        # Replace status values with enum members
        $content = $content -replace 'status="Passed"', 'status=StepStatus.Passed'
        $content = $content -replace 'status="Failed"', 'status=StepStatus.Failed'
        $content = $content -replace 'status="Skipped"', 'status=StepStatus.Skipped'
        $content = $content -replace 'status="Done"', 'status=StepStatus.Done'
        $content = $content -replace 'status="Error"', 'status=StepStatus.Error'
        $content = $content -replace 'status="Terminated"', 'status=StepStatus.Terminated'
        
        # Handle conditional expressions
        $content = $content -replace '"Passed" if (.+?) else "Failed"', 'StepStatus.Passed if $1 else StepStatus.Failed'
        $content = $content -replace '"Passed" if (.+?) else "F"', 'StepStatus.Passed if $1 else StepStatus.Failed'
        $content = $content -replace '"P" if (.+?) else "F"', 'StepStatus.Passed if $1 else StepStatus.Failed'
        
        # Save
        Set-Content $fullPath $content -NoNewline
    }
}

Write-Host "Done!"
