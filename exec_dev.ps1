.\env.ps1

# バッチ実行関数
function Invoke-Batch {
    param (
        [string]$in = "./input",
        [string]$out = "./output"
    )
    Set-Location -Path $PSScriptRoot
    Write-Host "psd_maskdata Start"
    py -m psd_maskdata --input $in --output $out
    Write-Host "psd_maskdata Completed"
}

# # psd_maskdataの実行
# Invoke-Batch -in ./input/subfolder -out ./output/subfolder
