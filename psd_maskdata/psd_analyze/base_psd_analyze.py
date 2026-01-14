from abc import ABC, abstractmethod
from psd_tools import PSDImage
import xml.etree.ElementTree as Et
import os

class BasePsdAnalyze(ABC):
    #
    # Constructor / Destructor
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
    def analyze_layer_to_xml(self, infile_path:str) -> Et.Element:
        """PSDレイヤー情報のXML解析

        このメソッドはPSDファイルを解析し、そのレイヤー情報をXMLのElementとして返します。

        Args:
            psd (PSDImage): PSDImageオブジェクト
            infile_path (str): 入力ファイルパス
        Returns:
            Et.Element: XMLのRoot要素
        """
        # PSDファイルの読み込み
        psd = PSDImage.open(infile_path)
        psd_name = os.path.splitext(os.path.basename(infile_path))[0]
        # XMLツリーの構築
        root = Et.Element("root")
        root.set('name', psd_name)
        for layer in psd:
            self._build_xml_recursive(layer, root)
        # XMLのRoot要素を返す
        return(root)

    #
    # protected methods
    #
    def _build_xml_recursive(self, layer:PSDImage, parent:Et.Element) -> None:
        """XMLツリーの構築(再帰処理)

        Args:
            layer (PSDImage): PSDImageオブジェクト
            parent (Et.Element): 親Element
        Returns:
            None
        """
        # グループレイヤーの場合
        if layer.is_group():
            # グループ要素の追加
            element = self._set_xml_group_attributes(layer, parent)
            # 再帰処理
            for child in layer:
                self._build_xml_recursive(child, element)
        # 通常レイヤーの場合
        else:
            # レイヤー要素の追加
            element = self._set_xml_node_attributes(layer, parent)

    def _set_xml_group_attributes(self, layer:PSDImage, parent:Et.Element) -> Et.Element:
        """XMLグループ要素の属性設定

        Args:
            layer (PSDImage): PSDImageオブジェクト
            parent (Et.Element): 親Element
        """
        element = Et.SubElement(parent, "group")
        element.set('name', str(layer.name))
        return(element)

    def _set_xml_node_attributes(self, layer:PSDImage, parent:Et.Element) -> Et.Element:
        """XMLノード要素の属性設定

        Args:
            layer (PSDImage): PSDImageオブジェクト
            parent (Et.Element): 親Element
            element (Et.Element): XMLのElement
        """
        element = Et.SubElement(parent, "node")
        element.set('name', str(layer.name))
        element.set('x', str(layer.left))
        element.set('y', str(layer.top))
        element.set('w', str(layer.width))
        element.set('h', str(layer.height))
        return(element)
