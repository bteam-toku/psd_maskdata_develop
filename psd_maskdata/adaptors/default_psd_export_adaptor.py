from psd_maskdata.interfaces import AbstractPsdExport
from psd_maskdata.psd_analyze import BasePsdAnalyze
from bteam_utils import CommonXML
import xml.etree.ElementTree as Et
import os

class DefaultPsdExportAdaptor(AbstractPsdExport):
    _base_psd_analyze : BasePsdAnalyze = None

    #
    # Constructor / Destructor
    # 
    def __init__(self, base_psd_analyze: BasePsdAnalyze) -> None:
        """Constructor

        Args:
            base_psd_analyze (BasePsdAnalyze): BasePsdAnalyzeオブジェクト
        """
        super().__init__()
        self._base_psd_analyze = base_psd_analyze

    def __del__(self) -> None:
        """Destructor
        """
        pass

    #
    # public methods
    #
    def export(self, input_path: str, output_path: str) -> bool:
        """PSDエクスポートの実装メソッド

        Args:
            input_path (str): 入力ファイルパス
            output_path (str): 出力ファイルパス
        Returns:
            bool: exportが成功した場合はTrue、失敗した場合はFalseを返す
        """
        # バリデーションチェック
        if self._base_psd_analyze is None:
            # BasePsdAnalyzeオブジェクトが設定されていない場合は失敗とする
            raise Exception("Fatal error: BasePsdAnalyze object is not set.")   
        if not input_path or not output_path:
            # 入力パスまたは出力パスが空の場合は失敗とする
            print("Error: Input path or output path is empty.")
            return False
        if not os.path.exists(input_path):
            # 入力パスまたは出力パスが存在しない場合は失敗とする
            print("Error: Input path or output path does not exist.")
            return False
        if not os.path.exists(output_path):
            # 出力パスのディレクトリが存在しない場合は作成する
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # PSDエクスポートの実行
        root : Et.Element = self._base_psd_analyze.analyze_layer_to_xml(input_path)
        if root is None:
            # XMLのRoot要素が取得できなかった場合は失敗とする
            print("Error: Failed to analyze PSD layers.")
            return False
        
        # XMLファイルの保存
        common_xml = CommonXML()
        common_xml.save_xml(root, output_path)
        return True