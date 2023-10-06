// 导出手柄按钮是否按下
using UnityEngine;
using System.Collections;

[RequireComponent(typeof(SteamVR_TrackedObject))]
public class HandleKeyScript : MonoBehaviour
{
	public int longDownThreshold = 50;
	public bool disableController = true;
	public bool useFakeInput = true; //替代性按键
	public KeyCode fakeInputKey = KeyCode.A;
	// 导出
	public bool isDown = false;
	public bool isJustDown = false;
	public bool isJustUp = false;
	public bool isLongDown = false;

	SteamVR_TrackedObject trackedObj;
	int downTime = 0;


	void Awake()
	{
		trackedObj = GetComponent<SteamVR_TrackedObject>();
	}


	void FixedUpdate()
	{
		// 手柄按键绑定至VirtualInput
		if (!disableController){
			var device = SteamVR_Controller.Input((int)trackedObj.index);
			isDown = device.GetTouch(SteamVR_Controller.ButtonMask.Trigger);
			isJustDown = device.GetTouchDown(SteamVR_Controller.ButtonMask.Trigger);
			isJustUp = device.GetTouchUp(SteamVR_Controller.ButtonMask.Trigger);
		}
		if (useFakeInput){
			isDown = Input.GetKey(fakeInputKey);
			isJustDown = Input.GetKeyDown(fakeInputKey);
			isJustUp = Input.GetKeyUp(fakeInputKey);
		}

		downTime = isDown ? downTime + 1 : 0;
		isLongDown = downTime > longDownThreshold;
	}


}
