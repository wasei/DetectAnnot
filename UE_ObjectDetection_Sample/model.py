import torch
import torchvision

def get_model(num_classes):
    """
    物体検出モデル（Faster R-CNN）を作成する
    
    引数:
        num_classes: 検出するクラス数（背景クラスを含む）
        
    戻り値:
        model: 設定済みのFaster R-CNNモデル
    """
    # 事前学習済みのResNet50バックボーンを使用したFaster R-CNNを読み込む
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=None)
    
    # 分類器の出力層を対象クラス数に合わせて変更
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(
        in_features, num_classes
    )
    
    return model


def save_model(model, path):
    """
    モデルを保存する
    
    引数:
        model: 保存するモデル
        path: 保存先のパス
    """
    torch.save(model.state_dict(), path)
    print(f"モデルを保存しました: {path}")


def load_model(path, num_classes, device):
    """
    保存されたモデルを読み込む
    
    引数:
        path: モデルファイルのパス
        num_classes: クラス数
        device: 使用するデバイス（CPUまたはGPU）
        
    戻り値:
        model: 読み込まれたモデル
    """
    model = get_model(num_classes)
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device)
    return model
