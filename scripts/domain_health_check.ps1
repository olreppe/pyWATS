<#
.SYNOPSIS
    Domain Health Check Management Script for pyWATS

.DESCRIPTION
    Checks and updates domain health check documents, validates freshness,
    and helps maintain documentation quality across all pyWATS domains.

.PARAMETER Domain
    Specific domain to check (e.g., 'analytics', 'report', 'product')

.PARAMETER All
    Check all domains

.PARAMETER FindStale
    Find health checks older than 3 months

.PARAMETER DryRun
    Preview what would happen without making changes

.EXAMPLE
    .\scripts\domain_health_check.ps1 -Domain analytics

.EXAMPLE
    .\scripts\domain_health_check.ps1 -All

.EXAMPLE
    .\scripts\domain_health_check.ps1 -FindStale
#>

param(
    [string]$Domain,
    [switch]$All,
    [switch]$FindStale,
    [switch]$DryRun
)

# Colors
function Write-Step { param([string]$msg) Write-Host "`n[>] $msg" -ForegroundColor Cyan }
function Write-Success { param([string]$msg) Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Info { param([string]$msg) Write-Host "  [i] $msg" -ForegroundColor Gray }
function Write-Warn { param([string]$msg) Write-Host "  [!] $msg" -ForegroundColor Yellow }

$RepoRoot = Split-Path -Parent $PSScriptRoot
$HealthDir = "$RepoRoot\docs\domain_health"

$ValidDomains = @(
    "analytics",
    "asset",
    "process",
    "product",
    "production",
    "report",
    "rootcause",
    "software"
)

function Get-HealthCheckAge {
    param([string]$FilePath)
    
    $content = Get-Content $FilePath -Raw
    if ($content -match '\*\*Last Updated:\*\*\s+(\d{4}-\d{2}-\d{2})') {
        $lastUpdate = [DateTime]::ParseExact($matches[1], "yyyy-MM-dd", $null)
        return (Get-Date) - $lastUpdate
    }
    
    # Fallback to file modification time
    return (Get-Date) - (Get-Item $FilePath).LastWriteTime
}

function Show-StaleHealthChecks {
    Write-Step "Finding Stale Health Checks (>3 months old)"
    
    $staleChecks = @()
    
    foreach ($domain in $ValidDomains) {
        $file = "$HealthDir\$domain.md"
        if (Test-Path $file) {
            $age = Get-HealthCheckAge $file
            if ($age.TotalDays -gt 90) {
                $staleChecks += [PSCustomObject]@{
                    Domain = $domain
                    AgeInDays = [int]$age.TotalDays
                    File = $file
                }
            }
        }
    }
    
    if ($staleChecks.Count -eq 0) {
        Write-Success "All health checks are up-to-date!"
        return
    }
    
    Write-Warn "Found $($staleChecks.Count) stale health check(s):`n"
    $staleChecks | Sort-Object AgeInDays -Descending | ForEach-Object {
        Write-Host "  - $($_.Domain): $($_.AgeInDays) days old" -ForegroundColor Yellow
    }
    
    Write-Host "`nRecommendation: Update with:" -ForegroundColor Cyan
    $staleChecks | ForEach-Object {
        Write-Host "  .\scripts\domain_health_check.ps1 -Domain $($_.Domain)" -ForegroundColor Gray
    }
}

function Update-HealthCheck {
    param([string]$DomainName)
    
    $file = "$HealthDir\$DomainName.md"
    
    if (-not (Test-Path $file)) {
        Write-Warn "Health check file not found: $file"
        return $false
    }
    
    Write-Step "Checking $DomainName domain"
    
    # Check age
    $age = Get-HealthCheckAge $file
    $ageInDays = [int]$age.TotalDays
    
    if ($ageInDays -lt 30) {
        Write-Success "Health check is fresh ($ageInDays days old)"
        return $true
    }
    elseif ($ageInDays -lt 90) {
        Write-Info "Health check is $ageInDays days old (acceptable)"
        return $true
    }
    else {
        Write-Warn "Health check is stale! ($ageInDays days old)"
        Write-Info "Please review and update: $file"
        return $false
    }
}

function Show-AllHealthChecks {
    Write-Step "Domain Health Summary (60-point scale)"
    
    $results = @()
    
    foreach ($domain in $ValidDomains) {
        $file = "$HealthDir\$domain.md"
        if (Test-Path $file) {
            $content = Get-Content $file -Raw
            
            # Extract score (now 60-point scale)
            $score = "N/A"
            if ($content -match '\*\*Health Score:\*\*\s+(\d+)/60') {
                $score = $matches[1]
            }
            elseif ($content -match '\*\*Health Score:\*\*\s+(\d+)/50') {
                # Legacy 50-point scale - flag for update
                $score = "$($matches[1])*"
            }
            
            # Extract grade
            $grade = "N/A"
            if ($content -match '\(([A-F][+-]?)\)') {
                $grade = $matches[1]
            }
            
            # Get age
            $age = Get-HealthCheckAge $file
            $ageInDays = [int]$age.TotalDays
            
            $status = if ($ageInDays -lt 30) { "✅" } elseif ($ageInDays -lt 90) { "⚠️" } else { "❌" }
            
            $results += [PSCustomObject]@{
                Domain = $domain.ToUpper()
                Score = "$score/60"
                Grade = $grade
                Age = "$ageInDays days"
                Status = $status
            }
        }
        else {
            $results += [PSCustomObject]@{
                Domain = $domain.ToUpper()
                Score = "N/A"
                Grade = "N/A"
                Age = "Missing"
                Status = "❌"
            }
        }
    }
    
    $results | Format-Table -AutoSize
    
    # Grade scale reference
    Write-Host "Grade Scale: A+ (58-60) | A (54-57) | A- (50-53) | B+ (46-49) | B (42-45) | B- (38-41)" -ForegroundColor Gray
    Write-Host "             C (30-37) | D (20-29) | F (<20)" -ForegroundColor Gray
    Write-Host ""
    
    $staleCount = ($results | Where-Object { $_.Status -eq "❌" }).Count
    if ($staleCount -gt 0) {
        Write-Warn "$staleCount health check(s) need updating"
    }
    else {
        Write-Success "All health checks are current!"
    }
}

# Main Logic
Write-Host @"

===============================================================
           pyWATS Domain Health Check Tool
===============================================================

"@ -ForegroundColor Cyan

if ($FindStale) {
    Show-StaleHealthChecks
    exit 0
}

if ($All) {
    Show-AllHealthChecks
    exit 0
}

if ($Domain) {
    if ($Domain -notin $ValidDomains) {
        Write-Host "ERROR: Invalid domain '$Domain'" -ForegroundColor Red
        Write-Host "`nValid domains: $($ValidDomains -join ', ')" -ForegroundColor Gray
        exit 1
    }
    
    $success = Update-HealthCheck $Domain
    
    if ($success) {
        Write-Success "Health check is current!"
        exit 0
    }
    else {
        Write-Warn "Health check needs attention"
        exit 1
    }
}

# No parameters - show usage
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  .\scripts\domain_health_check.ps1 -Domain <domain>   # Check specific domain"
Write-Host "  .\scripts\domain_health_check.ps1 -All                # Show all health checks"
Write-Host "  .\scripts\domain_health_check.ps1 -FindStale          # Find stale checks (>3 months)"
Write-Host ""
Write-Host "Valid domains: $($ValidDomains -join ', ')" -ForegroundColor Gray
exit 0
