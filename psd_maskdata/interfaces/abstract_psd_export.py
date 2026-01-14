from abc import ABC, abstractmethod

class AbstractPsdExport(ABC):
    #
    # コンストラクタ / デストラクタ
    # 
    def __init__(self):
        """コンストラクタ
        """
        pass

    def __del__(self):
        """デストラクタ
        """
        pass

    #
    # public メソッド
    #
    @abstractmethod
    def export(self, input_path: str, output_path: str) -> bool:
        """PSDエクスポートの抽象メソッド
        Args:
            input_path (str): 入力ファイルパス
            output_path (str): 出力ファイルパス
        Returns:
            bool: exportが成功した場合はTrue、失敗した場合はFalseを返す
        """
        pass