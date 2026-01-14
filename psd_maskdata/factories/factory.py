from psd_maskdata.interfaces import AbstractPsdExport
from typing import Optional
import importlib

class Factory:
    _instance : Optional[object] = None
    _cached_type : Optional[type] = None

    #
    # コンストラクタ / デストラクタ
    # 
    def __init__(self) -> None:
        """コンストラクタ
        """
        pass

    def __del__(self) -> None:
        """デストラクタ
        """
        pass

    #
    # public methods
    #
    @classmethod
    def create(cls, adaptor_type_name: Optional[str] = None) -> AbstractPsdExport:
        """PSDエクスポートアダプターの生成

        Args:
            adaptor_type_name (Optional[str], optional): アダプターの型名. デフォルトはNone.
        Returns:
            AbstractPsdExport: AbstractPsdExportオブジェクト
        """
        # 同じ型のアダプターがキャッシュされている場合はそれを返す（シングルトン）
        if cls._instance is not None and cls._cached_type == adaptor_type_name:
            return cls._instance

        if adaptor_type_name is None:
            # デフォルトで必要なモジュールをインポート
            from psd_maskdata.adaptors import DefaultPsdExportAdaptor
            from psd_maskdata.psd_analyze import PsdAnalyze
            # adaptor_type_nameが指定されていない場合はデフォルトのアダプターを使用
            psd_analyze = PsdAnalyze()
            cls._instance = DefaultPsdExportAdaptor(psd_analyze)
            cls._cached_type = adaptor_type_name
        else:
            # 指定された型名からアダプタークラスを動的にインポートして生成
            module_path, class_name = adaptor_type_name.rsplit('.', 1)
            module = importlib.import_module(module_path)
            adaptor_class = getattr(module, class_name)
            cls._instance = adaptor_class()
            cls._cached_type = adaptor_type_name

        # 生成したアダプターを返す
        return cls._instance
