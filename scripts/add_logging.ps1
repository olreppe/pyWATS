# Add logging imports to all repository files

$repositories = @(
    "src\pywats\domains\asset\repository.py",
    "src\pywats\domains\production\repository.py",
    "src\pywats\domains\report\repository.py",
    "src\pywats\domains\app\repository.py",
    "src\pywats\domains\software\repository.py",
    "src\pywats\domains\rootcause\repository.py",
    "src\pywats\domains\process\repository.py"
)

foreach ($repo in $repositories) {
    Write-Host "Processing $repo..."
    
    $content = Get-Content $repo -Raw
    
    # Check if logging is already imported
    if ($content -notmatch "import logging") {
        # Find the imports section and add logging
        $content = $content -replace '("""[^"]*"""\s+from typing[^\n]+\nimport[^\n]+)', "`$1`nimport logging"
        
        # Add logger after imports, before the class definition
        $content = $content -replace '(from \.models import [^\n]+)(\s+class)', "`$1`n`nlogger = logging.getLogger(__name__)`$2"
        
        Set-Content $repo -Value $content -NoNewline
        Write-Host "  Added logging to $repo"
    } else {
        Write-Host "  - Logging already present in $repo"
    }
}

Write-Host ""
Write-Host "Done! Logging infrastructure added to all repositories."
