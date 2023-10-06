// 输入信号量整合类
// 存取了所有信号的获取方式，懒获值
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(SteamVR_TrackedObject))]
public class VirtualInput: MonoBehaviour
{
    // 手柄（按键）
    public HandleKeyScript leftHandle;
    public HandleKeyScript rightHandle;
    // 聚焦射线
    public RayControlScript leftHandleRay;
    public RayControlScript rightHandleRay;
    public RayControlScript cameraRay;

    public bool isVisualAid = false;

    GameObject emptyGameObject;

    void Awake()
    {
        emptyGameObject = new GameObject();
    }

    
    // 左手柄正按下
    public bool isLeftHandleDown(){
        return leftHandle.isDown;
    }
    // 左手柄刚按下
    public bool isLeftHandleJustDown(){
        return leftHandle.isJustDown;
    }
    // 左手柄正长按
    public bool isLeftHandleLongDown(){
        return leftHandle.isLongDown;
    }
    // 右手柄正按下
    public bool isRightHandleDown(){
        return rightHandle.isDown;
    }
    // 右手柄刚按下
    public bool isRightHandleJustDown(){
        return rightHandle.isJustDown;
    }
    // 右手柄正长按
    public bool isRightHandleLongDown(){
        return rightHandle.isLongDown;
    }
    // 左手柄射线正聚焦
    public bool isLeftHandleFocus(out GameObject hitObj){
        if (leftHandleRay.isHit){
            hitObj = leftHandleRay.hit.collider.gameObject;
            return true;
        }else{
            hitObj = emptyGameObject;
            return false;
        }
    }
    // 右手柄射线正聚焦
    public bool isRightHandleFocus(out GameObject hitObj){
        if (rightHandleRay.isHit){
            hitObj = rightHandleRay.hit.collider.gameObject;
            return true;
        }else{
            hitObj = emptyGameObject;
            return false;
        }
    }

    // 左耳正按下
    public bool isLeftEarDown(){
        return HelloClient.isLeftEarDown;
        // return false;
    }
    // 右耳正按下
    public bool isRightEarDown(){
        return HelloClient.isRightEarDown;
        // return false;
    }
    // 视线正聚焦
    public bool isViewFocus(out GameObject hitObj){
        if (cameraRay.isHit){
            hitObj = cameraRay.hit.collider.gameObject;
            return true;
        }else{
            hitObj = emptyGameObject;
            return false;
        }
    }


    // 手柄点击
    public bool isHandleDown(out GameObject hitObj){
        hitObj = emptyGameObject;
        if (isLeftHandleDown() && isLeftHandleFocus(out hitObj)){
            return true;
        }else if (isRightHandleDown() && isRightHandleFocus(out hitObj)){
            return true;
        }else{
            return false;
        }
    }



    


}