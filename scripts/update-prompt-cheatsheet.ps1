#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Auto-generates the Copilot Prompt Commands Cheat Sheet.

.DESCRIPTION
    Scans all .prompt.md files in .github/prompts/, extracts metadata,
    gets last modified dates from git, and generates CHEATSHEET.md.

.EXAMPLE
    .\update-prompt-cheatsheet.ps1
    
.NOTES
    Updates: .github/prompts/CHEATSHEET.md
    Auto-commits if changes detected
#>

param(
    [switch]$NoCommit  # Skip auto-commit
)

$ErrorActionPreference = "Stop"

Write-Host "Updating Copilot Prompt Commands Cheat Sheet..." -ForegroundColor Cyan

# Set paths
$repoRoot = Split-Path -Parent $PSScriptRoot
$promptsDir = Join-Path $repoRoot ".github" "prompts"
$cheatsheetPath = Join-Path $promptsDir "CHEATSHEET.md"

# Get all prompt files
$promptFiles = Get-ChildItem -Path $promptsDir -Filter "*.prompt.md" | Where-Object { $_.Name -ne "CHEATSHEET.md" }

if ($promptFiles.Count -eq 0) {
    Write-Host "No prompt files found" -ForegroundColor Red
    exit 1
}

Write-Host "Found $($promptFiles.Count) prompt files" -ForegroundColor Green

# Function to extract YAML frontmatter
function Get-PromptMetadata {
    param([string]$FilePath)
    
    $content = Get-Content $FilePath -Raw
    
    # Extract YAML frontmatter
    if ($content -match '(?s)^---\s*\n(.*?)\n---') {
        $yaml = $matches[1]
        
        $metadata = @{}
        
        # Extract fields
        if ($yaml -match 'name:\s*(.+)') {
            $metadata['Name'] = $matches[1].Trim()
        }
        
        if ($yaml -match 'description:\s*(.+)') {
            $metadata['Description'] = $matches[1].Trim()
        }
        
        return $metadata
    }
    
    return $null
}

# Function to get last git commit date
function Get-FileLastModified {
    param([string]$FilePath)
    
    try {
        $relativePath = Resolve-Path -Relative $FilePath
        $gitDate = git log -1 --format="%ai" -- $relativePath 2>$null
        
        if ($gitDate) {
            return [DateTime]::Parse($gitDate).ToString("yyyy-MM-dd")
        }
    } catch {
        # Fall back to file system date
    }
    
    return (Get-Item $FilePath).LastWriteTime.ToString("yyyy-MM-dd")
}

# Collect prompt data
$prompts = @()
foreach ($file in $promptFiles) {
    $metadata = Get-PromptMetadata -FilePath $file.FullName
    
    if ($metadata -and $metadata['Name']) {
        $lastModified = Get-FileLastModified -FilePath $file.FullName
        
        $prompts += [PSCustomObject]@{
            Name = $metadata['Name']
            Description = $metadata['Description']
            LastModified = $lastModified
        }
    }
}

$prompts = $prompts | Sort-Object Name

Write-Host "Extracted metadata from $($prompts.Count) prompts" -ForegroundColor Green

# Generate content
$currentDate = Get-Date -Format "MMMM d, yyyy"

$lines = @()
$lines += "# pyWATS Copilot Commands - Quick Reference"
$lines += ""
$lines += "**Print this page and keep it on your wall!**"
$lines += "**Last Updated:** $currentDate"
$lines += ""
$lines += "---"
$lines += ""
$lines += "## Available Commands"
$lines += ""
$lines += "Type / in GitHub Copilot Chat to see these commands:"
$lines += ""
$lines += "---"
$lines += ""

foreach ($prompt in $prompts) {
    $lines += "### /$($prompt.Name)"
    $lines += "**$($prompt.Description)**"
    $lines += ""
    $lines += "**Last Updated:** $($prompt.LastModified)"
    $lines += ""
    $lines += "---"
    $lines += ""
}

$lines += "## Quick Reference Table"
$lines += ""
$lines += "| Command | Description | Last Updated |"
$lines += "|---------|-------------|--------------|"

foreach ($prompt in $prompts) {
    $lines += "| /$($prompt.Name) | $($prompt.Description) | $($prompt.LastModified) |"
}

$lines += ""
$lines += "---"
$lines += ""
$lines += "**Auto-Generated:** $currentDate"
$lines += "**Update Script:** .\scripts\update-prompt-cheatsheet.ps1"
$lines += "**Prompt Files:** $($prompts.Count) commands available"

# Write to file
$content = $lines -join "`n"
$content | Out-File -FilePath $cheatsheetPath -Encoding UTF8 -NoNewline

Write-Host "Cheat sheet updated: $cheatsheetPath" -ForegroundColor Green

# Check if changed
$gitStatus = git status --porcelain $cheatsheetPath 2>$null

if ($gitStatus -and -not $NoCommit) {
    Write-Host "Changes detected, committing..." -ForegroundColor Yellow
    
    try {
        git add $cheatsheetPath
        git commit -m "docs: Auto-update Copilot prompt commands cheat sheet"
        Write-Host "Committed cheat sheet update" -ForegroundColor Green
    } catch {
        Write-Host "Could not commit: $_" -ForegroundColor Yellow
    }
} elseif ($NoCommit) {
    Write-Host "Skipping commit (NoCommit flag)" -ForegroundColor Cyan
} else {
    Write-Host "No changes detected" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Done! Cheat sheet ready at: $cheatsheetPath" -ForegroundColor Green
