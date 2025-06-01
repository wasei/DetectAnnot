import torch
import torchvision.ops as ops
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import torchvision.transforms as T

# 日本語フォントの設定
plt.rcParams['font.family'] = 'MS Gothic'

def evaluate_model(model, data_loader, device, num_images=5):
    """
    モデルの性能評価を行い、IoUスコアを計算する
    
    引数:
        model: 評価するモデル
        data_loader: データローダー
        device: 使用するデバイス（CPUまたはGPU）
        num_images: 評価する画像数
        
    戻り値:
        avg_iou: 平均IoUスコア
    """
    model.eval()
    iou_scores = []
    
    with torch.no_grad():
        for i, (imgs, targets) in enumerate(data_loader):
            if i >= num_images:
                break
                
            imgs = [img.to(device) for img in imgs]
            outputs = model(imgs)

            for output, target in zip(outputs, targets):
                pred_boxes = output['boxes'].cpu()
                true_boxes = target['boxes'].cpu()

                if len(pred_boxes) == 0 or len(true_boxes) == 0:
                    iou_scores.append(0)
                    continue

                # IoUを計算（予測ボックスと正解ボックスの全組み合わせ）
                ious = ops.box_iou(pred_boxes, true_boxes)
                max_ious = ious.max(dim=1)[0]  # 各予測に対する最大IoU
                mean_iou = max_ious.mean().item()
                iou_scores.append(mean_iou)

    avg_iou = np.mean(iou_scores)
    print(f"{num_images}画像の平均IoU: {avg_iou:.4f}")
    
    model.train()  # モデルを訓練モードに戻す
    return avg_iou


def visualize_comparison(model_untrained, model_trained, image_path, device):
    """
    学習前と学習後のモデルの検出結果を並べて可視化
    
    引数:
        model_untrained: 学習前のモデル
        model_trained: 学習後のモデル
        image_path: JPEG画像のファイルパス
        device: 使用するデバイス（CPUまたはGPU）
    """
    model_untrained.eval()
    model_trained.eval()

    # 画像の読み込みと前処理
    img = Image.open(image_path).convert('RGB')  # 画像をRGB形式で読み込み
    transform = T.Compose([
        T.ToTensor(),  # PIL画像をテンソルに変換（値は[0, 1]に正規化）
    ])
    img_tensor = transform(img).to(device)

    # モデルの入力としてバッチ次元を追加
    img_tensor = img_tensor.unsqueeze(0)  # 形状を [1, C, H, W] に

    with torch.no_grad():
        # 学習前と学習後のモデルでの予測
        pred_before = model_untrained(img_tensor)[0]['boxes'].cpu()
        pred_after = model_trained(img_tensor)[0]['boxes'].cpu()

        plot_side_by_side(img_tensor.cpu().squeeze(0), pred_before, pred_after)


def plot_side_by_side(image, pred_boxes_before, pred_boxes_after):
    """
    学習前と学習後の検出結果を並べて表示
    
    引数:
        image: 入力画像
        pred_boxes_before: 学習前のモデルによる予測ボックス
        pred_boxes_after: 学習後のモデルによる予測ボックス
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    for ax, title, pred_boxes in zip(axes, ['学習前', '学習後'], [pred_boxes_before, pred_boxes_after]):
        ax.imshow(image.permute(1, 2, 0).cpu().numpy())

        # 予測バウンディングボックス（赤色）
        if pred_boxes is not None:
            for box in pred_boxes:
                x1, y1, x2, y2 = box
                rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                         linewidth=2, edgecolor='red', facecolor='none', linestyle='--')
                ax.add_patch(rect)

        ax.set_title(title)
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def detect_and_visualize(image_path, model, device, score_threshold=0.5):
    """
    指定された画像に対して物体検出を行い、結果を可視化
    
    引数:
        image_path: 画像ファイルのパス
        model: 物体検出モデル
        device: 使用するデバイス（CPUまたはGPU）
        score_threshold: 検出信頼度の閾値
    """
    model.eval()
    transform = T.ToTensor()

    # 画像読み込みと前処理
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).to(device)

    # 推論
    with torch.no_grad():
        prediction = model([image_tensor])[0]

    # 予測結果の取得
    boxes = prediction['boxes'].cpu()
    scores = prediction['scores'].cpu()
    labels = prediction['labels'].cpu()

    # 閾値以上のバウンディングボックスを抽出
    mask = scores > score_threshold
    filtered_boxes = boxes[mask]
    filtered_labels = labels[mask]
    filtered_scores = scores[mask]

    # 描画
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.imshow(image)
    
    for box, label, score in zip(filtered_boxes, filtered_labels, filtered_scores):
        x1, y1, x2, y2 = box
        rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)
        ax.text(x1, y1, f"Class: {label.item()}, {score:.2f}", 
                bbox=dict(facecolor='white', alpha=0.5))
    
    ax.set_title(f"検出結果: {image_path}")
    ax.axis("off")
    plt.tight_layout()
    plt.show()
