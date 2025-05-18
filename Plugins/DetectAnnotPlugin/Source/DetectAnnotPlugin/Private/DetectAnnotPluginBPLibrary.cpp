// Copyright Epic Games, Inc. All Rights Reserved.

#include "DetectAnnotPluginBPLibrary.h"
#include "DetectAnnotPlugin.h"
#include "GameFramework/Actor.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/KismetMathLibrary.h"
#include "Kismet/GameplayStatics.h"
#include "Blueprint/WidgetLayoutLibrary.h"

UDetectAnnotPluginBPLibrary::UDetectAnnotPluginBPLibrary(const FObjectInitializer& ObjectInitializer)
: Super(ObjectInitializer)
{

}

FRangeBounds UDetectAnnotPluginBPLibrary::GetBoundingBox2D(APlayerController* PlayerController, FTransform ActorTransform, const TArray<FVector>& ActorVertices)
{
    FVector2D ScreenPosition; // スクリーン座標を格納する変数
    TArray<float> ScreenX;
    TArray<float> ScreenY;

    // ビューポートのスケールを取得する
    // float ViewportScale = UWidgetLayoutLibrary::GetViewportScale(PlayerController);

    // TSetを使用して重複を排除する
    TSet<FVector> UniqueVertices(ActorVertices);

    // 各頂点をスクリーン座標に変換し、XとYの値を別々に保存する
    for (const FVector& Vertex : UniqueVertices)
    {
        if (UGameplayStatics::ProjectWorldToScreen(PlayerController, UKismetMathLibrary::TransformLocation(ActorTransform, Vertex), ScreenPosition, true))
        {
            // ビューポートのスケールを調整する
            // ScreenPosition /= ViewportScale;
            ScreenX.Add(ScreenPosition.X);
            ScreenY.Add(ScreenPosition.Y);
        }
    }

    // スクリーン座標が計算された場合のみ結果を返す
    if (ScreenX.Num() > 0 && ScreenY.Num() > 0)
    {
        return FRangeBounds(
            FMath::Min(ScreenX),
            FMath::Min(ScreenY),
            FMath::Max(ScreenX),
            FMath::Max(ScreenY)
        );
    }

    // 頂点が指定されていない場合はデフォルト値を返す
    return FRangeBounds(0, 0, 0, 0);
}

