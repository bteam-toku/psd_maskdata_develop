# バッチ実行用関数
function Invoke-Batch {
    param (
        [string]$in = "./input",
        [string]$out = "./output"
    )
    # psd_maskdataの実行
    py -m psd_maskdata --input $in --output $out
}

# 一つ上の親ディレクトリをカレントフォルダリに設定（環境に合わせて変更してください）
Set-Location -Path (Join-Path $PSScriptRoot "..")
# venvの有効化
.\scripts\env.ps1

# バッチ実行
Invoke-Batch -in ./input -out ./output
