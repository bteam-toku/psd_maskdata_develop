from .psd_export import PsdExport
import argparse
import os

def main():
    """メイン関数
    """
    psd_extension = ['.psd'] # PSDファイルの拡張子リスト

    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="PSDレイヤー情報のXMLエクスポートツール")
    parser.add_argument("--input", type=str, default='./input', help='入力PSDのフォルダパス(デフォルト: ./input)')
    parser.add_argument("--output", type=str, default='./output', help='出力XMLのフォルダパス(デフォルト: ./output)')
    args = parser.parse_args()

    # パスの取得
    input_path = args.input
    output_path = args.output
    # 入力パスの存在確認
    if not os.path.exists(input_path):
        print(f"Error: 入力フォルダが存在しません。{input_path}")
        return
    # 出力パスの存在確認と作成
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 進捗表示の初期化
    max_files = sum(len(files) for _, _, files in os.walk(input_path) if any(file.lower().endswith(tuple(psd_extension)) for file in files))
    processed_files = 0
    progress = 0
    # PSDファイルの処理
    psd_exporter = PsdExport()
    for root, dirs, files in os.walk(input_path):
        files:list[str]
        for file in files:
            # PSDファイルのみ処理
            if file.lower().endswith(tuple(psd_extension)):
                # ファイルパスの設定
                infile_path = os.path.join(root, file)
                outfile_path = os.path.join(output_path, os.path.splitext(file)[0] + '.xml')
                # エクスポート実行
                psd_exporter.export_layer_to_xml(infile_path, outfile_path)
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