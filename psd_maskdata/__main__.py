from psd_maskdata.factories import Factory
from psd_maskdata.interfaces import AbstractPsdExport
from psd_maskdata import Config

import argparse
import os
import sys

def main():
    """メイン関数
    """
    psd_extension = ['.psd'] # PSDファイルの拡張子リスト

    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="PSDレイヤー情報のXMLエクスポートツール。パラメータはsettings.yamlで指定可能。")
    parser.add_argument('--input', type=str, default='', help='入力フォルダパス（デフォルトはsettings.yamlのinput_path）')
    parser.add_argument('--output', type=str, default='', help='出力フォルダパス（デフォルトは設定ファイルのoutput_path）')
    parser.add_argument('--subfolder', type=str, default='', help='処理対象のサブフォルダ名（デフォルトはルートフォルダ）')
    args = parser.parse_args()

    # 設定ファイルの読み込み
    config = Config()
    # パスの取得
    input_path = os.path.join(args.input, args.subfolder) if args.input else os.path.join(config.input_path(), args.subfolder)
    output_path = os.path.join(args.output, args.subfolder) if args.output else os.path.join(config.output_path(), args.subfolder)
    # 入力パスの存在確認
    if not os.path.exists(input_path):
        print(f"Error: 入力フォルダが存在しません。{input_path}")
        sys.exit(1)

    # 進捗表示の初期化
    max_files = sum(len(files) for _, _, files in os.walk(input_path) if any(file.lower().endswith(tuple(psd_extension)) for file in files))
    processed_files = 0
    progress = 0
    # PSDファイルの処理
    exporter: AbstractPsdExport = Factory.create()
    for root, dirs, files in os.walk(input_path):
        # outputフォルダの対応するパスを作成
        relative_path = os.path.relpath(root, input_path)
        output_dir = os.path.join(output_path, relative_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        files:list[str]
        for file in files:
            # PSDファイルのみ処理
            if file.lower().endswith(tuple(psd_extension)):
                # ファイルパスの設定
                infile_path = os.path.join(root, file)
                outfile_path = os.path.join(output_dir, os.path.splitext(file)[0] + '.xml')
                # エクスポート実行
                exporter.export(infile_path, outfile_path)
                processed_files += 1
                progress = int((processed_files / max_files) * 100)
                # 進捗表示の更新
                show_progress(progress, task="PSDデータ処理中", status=f"{processed_files}/{max_files} files")
    # 最終進捗表示の更新
    if progress < 100:
        show_progress(100, task="PSDデータ処理中", status=f"{processed_files}/{max_files} files")

def show_progress(ratio: int, task: str = "", status: str = ""):
    """進捗表示
    Args:
        ratio (int): 進捗率 (0-100)
        task (str): 現在のタスク名
        status (str): 現在の状態メッセージ
    """
    block_num = 50
    ratio = min(max(ratio, 0), 100)
    int_ratio = int(ratio * (block_num / 100))
    
    bar = '[' + '#' * int_ratio + '-' * (block_num - int_ratio) + ']'
    output = f"\r{bar} {ratio:3}% | {task} : {status}"
    print(f"{output:<100}", end="", flush=True)

    if ratio >= 100:
        print()    

if __name__ == "__main__":
    main()