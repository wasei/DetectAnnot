// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "Kismet/BlueprintFunctionLibrary.h"
#include "DetectAnnotPluginBPLibrary.generated.h"

/* 
*	Function library class.
*	Each function in it is expected to be static and represents blueprint node that can be called in any blueprint.
*
*	When declaring function you can define metadata for the node. Key function specifiers will be BlueprintPure and BlueprintCallable.
*	BlueprintPure - means the function does not affect the owning object in any way and thus creates a node without Exec pins.
*	BlueprintCallable - makes a function which can be executed in Blueprints - Thus it has Exec pins.
*	DisplayName - full name of the node, shown when you mouse over the node and in the blueprint drop down menu.
*				Its lets you name the node using characters not allowed in C++ function names.
*	CompactNodeTitle - the word(s) that appear on the node.
*	Keywords -	the list of keywords that helps you to find node when you search for it using Blueprint drop-down menu. 
*				Good example is "Print String" node which you can find also by using keyword "log".
*	Category -	the category your node will be under in the Blueprint drop-down menu.
*
*	For more info on custom blueprint nodes visit documentation:
*	https://wiki.unrealengine.com/Custom_Blueprint_Node_Creation
*/

// X 座標と Y 座標の最小値と最大値で定義される 2D 範囲の境界を表します。
USTRUCT(BlueprintType)
struct FRangeBounds
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BoundingBox2D")
    float MinX;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BoundingBox2D")
    float MinY;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BoundingBox2D")
    float MaxX;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BoundingBox2D")
    float MaxY;

    FRangeBounds() : MinX(0), MinY(0), MaxX(0), MaxY(0) {}

    FRangeBounds(float InMinX, float InMinY, float InMaxX, float InMaxY)
        : MinX(InMinX), MinY(InMinY), MaxX(InMaxX), MaxY(InMaxY) {
    }
};

UCLASS()
class UDetectAnnotPluginBPLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_UCLASS_BODY()

    UFUNCTION(BlueprintCallable, meta = (DisplayName = "Get Bounding Box 2D", Keywords = "2D bounding box screen coordinates vertices"), Category = "DetectAnnot")
    static FRangeBounds GetBoundingBox2D(APlayerController* PlayerController, FTransform ActorTransform, const TArray<FVector>& ActorVertices);
};
