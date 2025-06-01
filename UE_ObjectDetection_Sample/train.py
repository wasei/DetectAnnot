import os
import torch
from torch.utils.data import DataLoader
import numpy as np
import torchvision.ops as ops

from dataset import CocoDetectionDataset
from transforms import get_transform
from model import get_model, save_model, load_model
from visualization import evaluate_model, visualize_comparison, detect_and_visualize

def train(model, data_loader, optimizer, device, epoch):
    """
    1エポック分のモデル学習を実行
    
    引数:
        model: 学習するモデル
        data_loader: 訓練データローダー
        optimizer: オプティマイザ
        device: 使用するデバイス（CPUまたはGPU）
        epoch: 現在のエポック番号
        
    戻り値:
        avg_loss: エポックの平均損失
    """
    model.train()
    total_loss = 0
    num_batches = 0
    
    for imgs, targets in data_loader:
        # データをデバイスに転送
        imgs = [img.to(device) for img in imgs]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
        
        # 順伝播と損失計算
        loss_dict = model(imgs, targets)
        losses = sum(loss for loss in loss_dict.values())
        
        # 逆伝播とパラメータ更新
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        
        total_loss += losses.item()
        num_batches += 1
    
    avg_loss = total_loss / num_batches
    print(f"エポック {epoch+1}, 損失: {avg_loss:.4f}")
    return avg_loss


def main():
    # 設定
    DATA_ROOT = "./dataset/images"
    ANN_FILE = "./annotations.json"
    MODEL_PATH = "./model.pth"
    NUM_CLASSES = 4  # 3クラス + 背景
    NUM_EPOCHS = 10
    BATCH_SIZE = 4
    
    # デバイスの設定
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用デバイス: {device}")
    
    # データセットとデータローダーの準備
    transform = get_transform()
    train_dataset = CocoDetectionDataset(
        root=DATA_ROOT,
        annFile=ANN_FILE,
        transforms=transform
    )
    data_loader = DataLoader(
        train_dataset, 
        batch_size=BATCH_SIZE, 
        shuffle=True, 
        collate_fn=lambda x: tuple(zip(*x))
    )
    
    # モデルの準備
    model = get_model(NUM_CLASSES)
    model.to(device)
    
    # 既存モデルの読み込みまたは新規学習
    if os.path.exists(MODEL_PATH):
        print("既存のモデルを読み込んでいます...")
        model = load_model(MODEL_PATH, NUM_CLASSES, device)
        
        # 学習前の未学習モデルを保持（可視化用）
        model_untrained = get_model(NUM_CLASSES).to(device)

        # テスト画像のパス
        image_path = './dataset/test_images/test01.jpg'

        # モデル可視化
        visualize_comparison(model_untrained, model, image_path, device)
    else:
        print("モデルを学習します...")
        
        # オプティマイザの設定
        params = [p for p in model.parameters() if p.requires_grad]
        optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
        
        # 学習前の評価
        print("学習前のモデル評価...")
        evaluate_model(model, data_loader, device)
        
        # 学習ループ
        for epoch in range(NUM_EPOCHS):
            train(model, data_loader, optimizer, device, epoch)
        
        # 学習後の評価
        print("学習後のモデル評価...")
        evaluate_model(model, data_loader, device)
        
        # モデル保存
        save_model(model, MODEL_PATH)
    
    # テスト画像での検出
    test_images = [
        "./dataset/test_images/test01.jpg",
        "./dataset/test_images/test02.jpg"
    ]
    
    # 学習後の可視化
    print("学習後の可視化...")
    for image_path in test_images:
        detect_and_visualize(image_path, model, device)



if __name__ == "__main__":
    main()
