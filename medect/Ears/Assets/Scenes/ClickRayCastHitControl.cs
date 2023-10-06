using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ClickRayCastHitControl : MonoBehaviour {

    Ray ray;
    RaycastHit hit;
    GameObject focusObj;
    GameObject[] selectableObjs;

    // Use this for initialization
    void Start () {
        selectableObjs = GameObject.FindGameObjectsWithTag("Selectable");

    }

    // Update is called once per frame
    
    void Update() {
        ray = Camera.main.ViewportPointToRay(new Vector3(0.5f, 0.5f));
        if (Physics.Raycast(ray, out hit)) {
            focusObj = hit.collider.gameObject;
        }else{
            focusObj = null;
        }

        // 选中高亮
        // foreach(GameObject selectableObj in selectableObjs){
        //     // if (selectableObj == focusObj && Input.GetMouseButton(0)){
        //     if (selectableObj == focusObj && VirtualInput.isDown()){
        //         selectableObj.GetComponent<Renderer>().material.color = new Color(0.7f, 0.4f, 0.1f, 1.0f);
        //     // }else if (selectableObj == focusObj){
        //     }else if (selectableObj == focusObj){
        //         selectableObj.GetComponent<Renderer>().material.color = new Color(0.2f, 0.2f, 0.3f, 1.0f);
        //     }else{
        //         selectableObj.GetComponent<Renderer>().material.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        //     }
        // }
    }

    // 鼠标左键绑定至VirualInput
    void FixedUpdate()
    {
        // Debug.Log(VirtualInput.isTouchDown);
        // VirtualInput.isTouchDown.value = Input.GetMouseButton(0);
    }
}
