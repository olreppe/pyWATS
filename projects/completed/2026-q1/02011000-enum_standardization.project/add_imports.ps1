# Add StepStatus import to files that need it

$files = @{
    "examples\converters\csv_converter.py" = @{
        "after" = "from pywats.shared.enums import CompOp"
        "import" = "from pywats.domains.report.report_models.common_types import StepStatus"
    }
    "examples\converters\xml_converter.py" = @{
        "after" = "from pywats.shared.enums import CompOp, ChartType"
        "import" = "from pywats.domains.report.report_models.common_types import StepStatus"
    }
    "src\pywats\tools\report_builder.py" = @{
        "after" = "from ..domains.report.report_models.common_types import ReportStatus"
        "import" = "from ..domains.report.report_models.common_types import ReportStatus, StepStatus"
        "replace" = $true
    }
    "src\pywats_client\converters\models.py" = @{
        "after" = "from pywats.domains.report.report_models.uut import UUTReport"
        "import" = "from pywats.domains.report.report_models.common_types import StepStatus"
    }
    "src\pywats_client\converters\standard\klippel_converter.py" = @{
        "after" = "from pywats.shared.enums import CompOp, ChartType"
        "import" = "from pywats.domains.report.report_models.common_types import StepStatus"
    }
    "tests\integration\test_boxbuild.py" = @{
        "after" = "from pywats.domains.report.report_models.uut import UUTReport"
        "import" = "from pywats.domains.report.report_models.common_types import StepStatus"
    }
    "tests\domains\rootcause\test_d8_workflow.py" = @{
        "after" = "from pywats.domains.report.report_models.uut import UUTReport"
        "import" = "from pywats.domains.report.report_models.common_types import StepStatus"
    }
    "tests\domains\report\test_workflow.py" = @{
        "after" = "from pywats.shared.enums import CompOp, ChartType"
        "import" = "from pywats.domains.report.report_models.common_types import StepStatus"
    }
}

$basePath = "c:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS"

foreach ($file in $files.Keys) {
    $fullPath = Join-Path $basePath $file
    $config = $files[$file]
    
    if (Test-Path $fullPath) {
        Write-Host "Adding import to: $file"
        
        $content = Get-Content $fullPath -Raw
        
        if ($config.replace) {
            # Replace existing import
            $content = $content -replace [regex]::Escape($config.after), $config.import
        } else {
            # Add new import after specified line
            $content = $content -replace ([regex]::Escape($config.after)), "$($config.after)`n$($config.import)"
        }
        
        Set-Content $fullPath $content -NoNewline
    }
}

Write-Host "Import additions complete!"
