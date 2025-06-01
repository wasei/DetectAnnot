import torch
import torchvision.transforms as T

class ComposeTransforms:
    """
    画像とアノテーションの両方に対応した変換処理を行うクラス
    """
    def __init__(self, transforms):
        """
        変換処理のリストを初期化
        
        引数:
            transforms: 画像変換処理のリスト
        """
        self.transforms = transforms

    def __call__(self, image, target):
        """
        画像に対して変換処理を適用し、ターゲット（アノテーション）も同時に返す
        
        引数:
            image: 入力画像
            target: アノテーション情報
            
        戻り値:
            変換後の画像とアノテーション
        """
        for t in self.transforms:
            image = t(image)
        return image, target


def get_transform():
    """
    データセット用の標準的な変換処理を返す
    
    戻り値:
        ComposeTransforms: 変換処理オブジェクト
    """
    return ComposeTransforms([T.ToTensor()])
