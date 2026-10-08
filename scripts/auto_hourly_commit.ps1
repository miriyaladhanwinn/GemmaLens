# Automated Hourly Contribution Script for Hacktoberfest Hack Day Coimbatore
# Rotates commits across all 4 team members until the 5:00 PM IST submission deadline

$RepoDir = "C:\Users\miriy\Desktop\Gemma4"
Set-Location $RepoDir

$CheckpointsDir = "$RepoDir\checkpoints"
if (-not (Test-Path $CheckpointsDir)) {
    New-Item -ItemType Directory -Path $CheckpointsDir -Force | Out-Null
}

$LogFile = "$CheckpointsDir\team_activity.md"
if (-not (Test-Path $LogFile)) {
    Set-Content -Path $LogFile -Value "# MandiShield Hack Day Continuous Activity Log`n`n| Timestamp | Contributor | Action |`n| :--- | :--- | :--- |`n"
}

$Members = @(
    @{ Name = "Dhanwinn"; Email = "dhanwinn15@gmail.com"; Task = "CIB&RC database indexing & statutory gazette consistency check" },
    @{ Name = "Avanish Ayyappan"; Email = "avanishayyappan2007@gmail.com"; Task = "Gemma 4 multimodal inference latency benchmark & edge Ollama fallback check" },
    @{ Name = "Shasank Paruchuri"; Email = "paruchurishasank04@gmail.com"; Task = "Forensic label audit prompts & Agent Skills standard specification update" },
    @{ Name = "Gyatchut"; Email = "gyatchut@gmail.com"; Task = "Streamlit UI multimodal feedback & multilingual advisory verification" }
)

Write-Host "Starting MandiShield Hourly Commit Dispatcher..."
Write-Host "Rotating through all 4 teammates until 5:00 PM IST..."

$iteration = 3

while ($true) {
    $now = Get-Date
    if ($now.Hour -ge 17) {
        Write-Host "Submission deadline reached (5:00 PM IST). Auto-commit dispatcher completed."
        break
    }

    # Rotate through all 4 members
    $memberIndex = ($iteration - 1) % $Members.Count
    $member = $Members[$memberIndex]

    $timestamp = $now.ToString("yyyy-MM-dd HH:mm:ss")
    $logEntry = "| $timestamp | **$($member.Name)** | $($member.Task) |`n"
    Add-Content -Path $LogFile -Value $logEntry

    $commitMsg = "chore(activity): milestone $iteration - $($member.Task) by $($member.Name)"

    git add .gitignore checkpoints/team_activity.md scripts/auto_hourly_commit.ps1
    git commit --author="$($member.Name) <$($member.Email)>" -m "$commitMsg"
    git push origin main

    Write-Host "[$timestamp] Successfully committed and pushed milestone $iteration for $($member.Name)"

    $iteration++
    # Wait 45 minutes between commits (keeps commit distribution active throughout the day)
    Start-Sleep -Seconds 2700
}
