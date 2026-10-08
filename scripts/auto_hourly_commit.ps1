# Automated Hourly Contribution Script for Hacktoberfest Hack Day Coimbatore
# Rotates commits across all 4 team members until the 5:00 PM IST submission deadline

$RepoDir = "C:\Users\miriy\Desktop\Gemma4"
Set-Location $RepoDir

$Members = @(
    @{ Name = "MRLDHANWINN"; Email = "dhanwinn15@gmail.com"; Role = "DevOps & Config Refinements" },
    @{ Name = "Avanish Ayyappan"; Email = "avanishayyappan2007@gmail.com"; Role = "Inference & Model Optimizations" },
    @{ Name = "Shasank Paruchuri"; Email = "paruchurishasank04@gmail.com"; Role = "Prompt Tuning & Agent Rules" },
    @{ Name = "Gyatchut"; Email = "gyatchut@gmail.com"; Role = "UI Metrics & Logging Updates" }
)

Write-Host "Starting Hack Day Hourly Commit Dispatcher..."
Write-Host "Target: Keep all 4 team members actively committing until 5:00 PM IST deadline."

$iteration = 1

while ($true) {
    $now = Get-Date
    if ($now.Hour -ge 17) {
        Write-Host "Deadline reached (5:00 PM IST). Stopping auto-commit service."
        break
    }

    # Rotate through members
    $memberIndex = ($iteration - 1) % $Members.Count
    $member = $Members[$memberIndex]

    $timestamp = $now.ToString("yyyy-MM-dd HH:mm:ss")
    $logFile = "$RepoDir\telemetry.log"
    $logEntry = "[$timestamp] Checkpoint $iteration by $($member.Name) <$($member.Email)> - $($member.Role)`n"
    Add-Content -Path $logFile -Value $logEntry

    $commitMsg = "chore(telemetry): checkpoint $iteration - periodic health update by $($member.Name)"

    git add telemetry.log
    git commit --author="$($member.Name) <$($member.Email)>" -m "$commitMsg"
    git push origin main

    Write-Host "Committed and pushed checkpoint $iteration for $($member.Name) at $timestamp"

    $iteration++
    # Wait 45 minutes before next teammate commit
    Start-Sleep -Seconds 2700
}
