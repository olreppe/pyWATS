# Remove Old GUI Script
#
# This script removes the old GUI directory from pywats_client
# Run this after verifying the new GUI is working correctly.
#
# Usage: .\remove_old_gui.ps1

Write-Host "=" * 80
Write-Host "pyWATS Old GUI Removal Script"
Write-Host "=" * 80
Write-Host ""

$oldGuiPath = "src\pywats_client\gui"

# Check if directory exists
if (Test-Path $oldGuiPath) {
    Write-Host "Found old GUI directory at: $oldGuiPath"
    
    # Count files
    $fileCount = (Get-ChildItem -Path $oldGuiPath -Recurse -File | Measure-Object).Count
    Write-Host "  Files to remove: $fileCount"
    
    # Ask for confirmation
    Write-Host ""
    $confirmation = Read-Host "Remove old GUI directory? (yes/no)"
    
    if ($confirmation -eq "yes") {
        Write-Host "Removing old GUI directory using git..."
        
        # Use git rm to remove tracked files
        git rm -r $oldGuiPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Old GUI directory removed successfully!"
            Write-Host ""
            Write-Host "Next steps:"
            Write-Host "  1. Test new GUI: python run_client_a.py"
            Write-Host "  2. Test dual instances: python test_both_guis.py"
            Write-Host "  3. Commit changes: git commit -m 'refactor: Remove old GUI'"
        } else {
            Write-Host "Error: git rm failed"
            Write-Host "Falling back to manual removal..."
            Remove-Item -Path $oldGuiPath -Recurse -Force
            Write-Host "Old GUI directory removed (untracked)"
        }
    } else {
        Write-Host "Operation cancelled."
    }
} else {
    Write-Host "Old GUI directory not found at: $oldGuiPath"
    Write-Host "Already removed or path incorrect."
}

Write-Host ""
Write-Host "=" * 80
