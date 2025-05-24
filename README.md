# DetectAnnot

Unreal Engine × 機械学習｜ 3D モデルから物体検出データを自動生成するツール

## 概要

DetectAnnot は、Unreal Engine 上で 3D モデルを自由に配置し、物体検出タスク向けの画像と、COCO 形式のアノテーションデータ（JSON）を自動生成するツールです。

3D モデルから、簡単に学習用データを作れるようにすることを目的としています。

### 実行中の動作デモ

シーンを作成し PIE プレビューで学習データの画像と、アノテーションデータを出力します。  
レンダリング中に表示されるバウンディングボックスの表示はデバッグ用で出力される画像には表示されません。
![DetectAnnot 実行中の動作デモ](docs/images/detectannot_run_demo.gif)

## ⚠️ 注意：Git LFS を使用しています

このリポジトリでは一部の大容量ファイルを [Git LFS](https://git-lfs.com/) で管理しています。

GitHub の「Download ZIP」ではこれらのファイルは正しく取得されません。クローン後は以下のコマンドを実行してください。

## 使い方（サンプルシーンの動作確認）

1. `DetectAnnot.uproject` を Unreal Engine で開きます
2. `/Game/DetectAnnot/Maps/Sample` レベルを開きます
3. エディタのメニューから  
   `環境設定 > Game Viewport Settings > 新しいビューポート解像度` を **512×512** に設定します  
   ![Viewport設定](docs/images/viewport_setting.png) <!-- 画像1 -->
4. 「新規エディタウィンドウ（PIE）」で実行します  
   ![PIE実行](docs/images/run_pie.png) <!-- 画像2 -->
5. シーンがレンダリングされます  
   ![レンダリング中](docs/images/rendering_scene.png) <!-- 画像3 -->
6. 以下のファイルが出力されます：

   - `annotations.json` → プロジェクトのルートディレクトリ  
     ![annotations.json](docs/images/annotations_output.png) <!-- 画像4 -->
     ![整形済みCOCO形式のアノテーションJSON抜粋](docs/images/annotation_sample_excerpt.png)
     ※ 実際の出力は整形されていません。以下はフォーマッターで整形した例です。
   - 画像（`####.jpeg` 形式）→ `DetectAnnot/Saved/MovieRenders/`  
     ![画像出力](docs/images/image_output.png) <!-- 画像5 -->

## 自作スタティックメッシュでアノテーションを作成する場合

1. レベルに `BP_DetectAnnot` を配置します
1. 詳細パネルの「Mesh」から、使用したいスタティックメッシュを指定します
1. ゲームモードに `BP_MLBase` を設定します
   - `ワールド設定 > ゲームモードオーバーライド` で変更可能です
1. その後は通常通り PIE 実行でアノテーションと画像が出力されます
   ![BP_DetectAnnotとBP_MLBaseの配置ガイド](docs/images/bp_detectannot_setup_guide.png)

## 既知の問題

- **視野外オブジェクトの出力**  
  カメラのフレーム外に存在するオブジェクトについてもアノテーションが出力されます。

- **遮蔽されたオブジェクトの出力**  
  手前のオブジェクトに隠れて見えない場合でも、奥のオブジェクトがアノテーションに含まれます。

## 動作環境

- Unreal Engine 5.5.4
- Windows 10

## ライセンス

MIT License

## 作者

- Kazumasa (和正)
  https://x.com/HDbflat
