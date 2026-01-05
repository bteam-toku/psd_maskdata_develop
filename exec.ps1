# バッチ実行関数
function Invoke-Batch {
    param (
        [string]$in = "./input",
        [string]$out = "./output"
    )
    Set-Location -Path $PSScriptRoot
    Write-Host "psd_maskdata Start"

    $fullInPath = Join-Path (Get-Location) $in
    $fullOutPath = Join-Path (Get-Location) $out

    docker run -it --rm `
        -v "${fullInPath}:/app/input" `
        -v "${fullOutPath}:/app/output" `
        psd_maskdata --input /app/input --output /app/output

    Write-Host "psd_maskdata Completed"
}

# # psd_maskdataの実行
# Invoke-Batch -in ./input/subfolder -out ./output/subfolder