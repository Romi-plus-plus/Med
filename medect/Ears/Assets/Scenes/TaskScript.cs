// 测试任务的定制脚本
// 绑定于GameController，全局操控
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class TaskScript : MonoBehaviour
{
    
    
    public Text messageText;
    public GameObject[] selectors = new GameObject[3];
    public string[] selectorsName = new string[3];
    public GameObject targetSelector;
    public string targetSelectorName;

    bool isTesting = false;
    int idxTests = 0, numTests = 5;
    float startTime, endTime;

    Ray ray;
    RaycastHit hit;
    GameObject obj;

    public void StartTest(){
        startTime = Time.time;

        isTesting = true;
        idxTests = 0;
        int selectorIdx = Random.Range(0, 3);
        targetSelector = selectors[selectorIdx];
        targetSelectorName = selectorsName[selectorIdx];

        messageText.text = "(" + idxTests + "/" + numTests + "）\nTry to select " + targetSelectorName + "\n";
    }

    public void EndTest(){
        endTime = Time.time;

        isTesting = false;
        messageText.text = "Test Complete!\nTime spend: " + (endTime - startTime) + "s\n";
    }

    public void ContinueTest(GameObject selectedObj){
        if (selectedObj == targetSelector){
            idxTests += 1;
            // messageText.text = "Selected!" + "[" + idxTests + "]";
            Debug.Log("Complete Test (" + idxTests + "/" + numTests + "）");
            int selectorIdx = Random.Range(0, 3);
            targetSelector = selectors[selectorIdx];
            targetSelectorName = selectorsName[selectorIdx];

            messageText.text = "(" + idxTests + "/" + numTests + "）\nTry to select " + targetSelectorName + "\n";
            if (idxTests >= numTests){
                EndTest();
            }
        }else{
            // do nothing
        }
    }

    void Update(){
        // 检测测试按钮是否按下


        if (Input.GetKeyDown("1")){
            StartTest();
        }

        if (isTesting){
            // if (Input.GetMouseButtonDown(0)) // 左键
            // if (VirtualInput.isDown())
            // {
            //     ray = Camera.main.ViewportPointToRay(new Vector3(0.5f, 0.5f));
            //     if (Physics.Raycast(ray, out hit))
            //     {
            //         obj = hit.collider.gameObject;
            //         if (obj.tag == "Selectable"){
            //             Debug.Log("点中" + obj.name);
            //             ContinueTest(obj);
            //         }
            //     }
            // }
        }
    }
}
