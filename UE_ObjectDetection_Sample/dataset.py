import os
import json
import torch
from torch.utils.data import Dataset
from PIL import Image

class CocoDetectionDataset(Dataset):
    """
    COCOフォーマットのアノテーションデータとイメージを扱うデータセットクラス
    """
    def __init__(self, root, annFile, transforms=None):
        """
        データセットの初期化
        
        引数:
            root: 画像フォルダへのパス
            annFile: アノテーションJSONファイルへのパス
            transforms: 画像変換処理（オプション）
        """
        self.root = root
        self.transforms = transforms
        
        # アノテーションデータの読み込み
        with open(annFile, 'r') as f:
            coco = json.load(f)

        self.images = coco['images']
        self.annotations = coco['annotations']
        self.categories = coco['categories']
        self.category_id_to_name = {cat['id']: cat['name'] for cat in self.categories}

        # 画像IDごとにアノテーションをグループ化
        self.img_id_to_anns = {}
        for ann in self.annotations:
            img_id = ann['image_id']
            if img_id not in self.img_id_to_anns:
                self.img_id_to_anns[img_id] = []
            self.img_id_to_anns[img_id].append(ann)

        # 画像IDとファイル名のマッピング
        self.id_to_filename = {img['id']: img['file_name'] for img in self.images}

    def __getitem__(self, idx):
        """
        データセットから要素を取得する
        
        引数:
            idx: 取得する要素のインデックス
            
        戻り値:
            image: 前処理済み画像
            target: バウンディングボックスとラベル情報
        """
        img_info = self.images[idx]
        img_id = img_info['id']
        img_path = os.path.join(self.root, img_info['file_name'])
        image = Image.open(img_path).convert("RGB")

        # アノテーションからバウンディングボックスとラベルを抽出
        anns = self.img_id_to_anns.get(img_id, [])
        boxes = []
        labels = []
        for ann in anns:
            x, y, w, h = ann['bbox']
            boxes.append([x, y, x + w, y + h])  # [x, y, width, height] → [x1, y1, x2, y2]
            labels.append(ann['category_id'])

        # テンソル形式に変換
        boxes = torch.tensor(boxes, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.int64)
        target = {
            "boxes": boxes,
            "labels": labels,
            "image_id": torch.tensor([img_id])
        }

        # 画像変換処理の適用
        if self.transforms:
            image, target = self.transforms(image, target)

        return image, target

    def __len__(self):
        """データセットの長さを返す"""
        return len(self.images)
