# バッチ実行関数
function Invoke-Batch {
    param (
        [string]$in = "./input",
        [string]$out = "./output"
    )
    $fullInPath = Join-Path (Get-Location) $in
    $fullOutPath = Join-Path (Get-Location) $out
    $fullCurrentPath = Get-Location

    docker run -it --rm `
        -v "${fullCurrentPath}:/data" `
        -v "${fullInPath}:/app/input" `
        -v "${fullOutPath}:/app/output" `
        ghcr.io/bteam-toku/psd_maskdata:latest --input /app/input --output /app/output
}

# 一つ上の親ディレクトリをカレントフォルダリに設定（環境に合わせて変更してください）
Set-Location -Path (Join-Path $PSScriptRoot "..")

# psd_maskdataの実行
Invoke-Batch -in ./input -out ./output