// 测试任务的定制脚本
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class Task2Script : MonoBehaviour
{
    public VirtualInput vInput;
    public Text messageText;            // 信息输出框：按钮一旁
    public Text infoText;               // 信息输出框：方块上方
    public GameObject task2panel;       // 任务2窗体
    public int task1times = 10;         // 测试次数
    public int task2times = 10;
    public int task3times = 10;
    public HelloClient client;         // 通信客户端

    // 说明性文字
    public string[] taskInfoWithHandle = new string[3];
    public string[] taskInfoWithEar = new string[3];   

    // 测试1的待选方块
    public GameObject[] test1selectors = new GameObject[6];
    public string[] test1selectorsName = new string[6];
    GameObject test1targetSelector;
    string test1targetSelectorName;

    // 测试2的待选方块
    public GameObject[] test2selectors = new GameObject[3];
    GameObject test2targetSelector;

    public bool isTask1Started = false; // 是否开始
    public bool isTask2Started = false;
    public bool isTask3Started = false;
    public int task1process = 0;        // 任务进度
    public int task2process = 0;
    public int task3process = 0;


    float startTime, endTime;           // 任务1计时
    bool isPanelActive = false;


    void Start()
    {
        task2panel.SetActive(false);
        // task2panel.transform.localScale = Vector3.zero;
        for (int i = 0; i < 3; i++){
            taskInfoWithHandle[i] = taskInfoWithHandle[i].Replace("\\n", "\n");
        }
    }

    void FixedUpdate()
    {
        // debugSelecting();   // debug信息输出

        GameObject hitObj;
        // 主菜单按钮只能用手柄射线点击
        if (vInput.isHandleDown(out hitObj)){
            // 测试1
            if (hitObj.name == "StartTest1Btn" && !isTask2Started && !isTask3Started){
                // 开始测试1/结束测试1
                isTask1Started = true;
                isTask2Started = false;
                isTask3Started = false;
                // 说明文字
                if (!vInput.isVisualAid){
                    messageText.text = taskInfoWithHandle[0];
                }else{
                    messageText.text = taskInfoWithEar[0];
                }
                task1start();
            }

            // 测试2
            if (hitObj.name == "StartTest2Btn" && !isTask1Started && !isTask3Started){
                // 开始测试2/结束测试2
                isTask1Started = false;
                isTask2Started = true;
                isTask3Started = false;
                // 说明文字
                if (!vInput.isVisualAid){
                    messageText.text = taskInfoWithHandle[1];
                }else{
                    messageText.text = taskInfoWithEar[1];
                }
                task2start();
            }

            // 测试3
            if (hitObj.name == "StartTest3Btn" && !isTask1Started && !isTask2Started){
                // 开始测试3/结束测试3
                isTask1Started = false;
                isTask2Started = false;
                isTask3Started = true;
                // 说明文字
                if (!vInput.isVisualAid){
                    messageText.text = taskInfoWithHandle[2];
                }else{
                    messageText.text = taskInfoWithEar[2];
                }
                task3start();
            }

            // 停止测试
            if (hitObj.name == "StopTestBtn"){
                isTask1Started = false;
                isTask2Started = false;
                isTask3Started = false;
                // task2panel.transform.localScale = Vector3.zero;
                task2panel.SetActive(false);
                messageText.text = "";
                infoText.text = "";
            }

            // 开启视觉提示（按钮处于视觉中心时高亮）
            if (hitObj.name == "StartVisualAids"){
                vInput.isVisualAid = true;
            }

            // 关闭视觉提示（按钮处于视觉中心时高亮）
            if (hitObj.name == "StopVisualAids"){
                vInput.isVisualAid = false;
            }

            // 开启通信
            if (hitObj.name == "StartComBtn"){
                client.StartCom();
            }

            // 停止通信
            if (hitObj.name == "StopComBtn"){
                client.StopCom();
            }
        }

        // 测试循环
        if (isTask1Started){
            // 进行测试1
            task1update();
        }else if (isTask2Started){
            // 进程测试2
            task2update();
        }else if (isTask3Started){
            // 进程测试3
            task3update();
        }
    }

    // 测试选择功能
    void debugSelecting()
    {
        GameObject hitObj;
        if (vInput.isHandleDown(out hitObj)){
            Debug.Log("handle click: " + hitObj.name);
        }

        if (vInput.isViewFocus(out hitObj)){
            Debug.Log("focus on: " + hitObj.name);
        }
    }


    // 测试1开始
    void task1start()
    {
        // 开始计时，重置进度
        task1process = 0;
        // 生成不一样的任务目标
        while (true){
            int i = Random.Range(0, 3);
            if (test1selectors[i] != test1targetSelector){
                test1targetSelector = test1selectors[i];
                test1targetSelectorName = test1selectorsName[i];
                break;
            }
        }
        for (int i = 0; i < 3; i++){
            test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                test1selectors[i] == test1targetSelector ? 
                "Click Me" : ""
            );
        }
        // 提示信息
        // messageText.text = "Task 1 start\n";
        // messageText.text += "点击右侧按钮\n";
        infoText.text = "(" + task1process + "/" + task1times + "）\n";
        infoText.text += "Select " + test1targetSelectorName + "\n";
    }

    // 测试1进行中
    void task1update()
    {
        bool isSelected = false;
        GameObject hitObj;
        // 手柄选中且确认
        if (vInput.isHandleDown(out hitObj)){
            if (hitObj == test1targetSelector){
                isSelected = true;
            }
        }
        // 眼选中且耳确认
        if (vInput.isLeftEarDown() && vInput.isViewFocus(out hitObj)){
            if (hitObj == test1targetSelector){
                isSelected = true;
            }
        }

        // 完成一步测试
        if (isSelected){
            if (task1process == 0){
                startTime = Time.time;
            }

            task1process += 1;
            // Debug.Log("task 1 done: " + task1process + "/" + task1times);

            if (task1process < task1times){
                // 未完成测试
                // 生成不一样的任务目标
                while (true){
                    int i = Random.Range(0, 3);
                    if (test1selectors[i] != test1targetSelector){
                        test1targetSelector = test1selectors[i];
                        test1targetSelectorName = test1selectorsName[i];
                        break;
                    }
                }
                for (int i = 0; i < 3; i++){
                    test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                        test1selectors[i] == test1targetSelector ? 
                        "Click Me" : ""
                    );
                }
                // 提示信息
                infoText.text = "(" + task1process + "/" + task1times + "）\n";
                infoText.text += "Select " + test1targetSelectorName + "\n";
            }else{
                // 完成测试
                isTask1Started = false;
                endTime = Time.time;
                for (int i = 0; i < 3; i++){
                    test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = "";
                }
                // 提示信息
                infoText.text = "(" + task1process + "/" + task1times + "）\n";
                infoText.text += "Test 1 Done\n";
                infoText.text += "time of " + (endTime - startTime).ToString("N2") + "s\n";
                messageText.text = "Test 1 Done\n";
                messageText.text += "time of " + (endTime - startTime).ToString("N2") + "s\n";
            }
        }
    }

    // 测试2开始
    void task2start()
    {
        // 开始计时
        // startTime = Time.time;
        task2process = 0;
        
        // 生成不一样的任务目标
        while (true){
            int i = Random.Range(0, 3);
            if (test1selectors[i] != test1targetSelector){
                test1targetSelector = test1selectors[i];
                break;
            }
        }
        while (true){
            int i = Random.Range(0, 3);
            if (test2selectors[i] != test2targetSelector){
                test2targetSelector = test2selectors[i];
                break;
            }
        }
        for (int i = 0; i < 3; i++){
            test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                test1selectors[i] == test1targetSelector ? 
                "Long Press Me" : ""
            );
        }
        for (int i = 0; i < 3; i++){
            test2selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                test2selectors[i] == test2targetSelector ? 
                "Click Me" : ""
            );
        }
        // 提示信息
        // messageText.text = "Task 2 start\n";
        // messageText.text += "长按手柄以唤出菜单并按下\n";
    }

    // 测试2进行中
    void task2update()
    {
        GameObject hitObj;

        // 面前展开窗体
        if (vInput.isLeftHandleLongDown() || vInput.isRightHandleLongDown()){
            if (vInput.isHandleDown(out hitObj)){
                if (hitObj == test1targetSelector){
                    task2panel.SetActiveRecursively(true);
                    task2panel.transform.position = Camera.main.transform.position + Camera.main.transform.forward * 100.0f;
                    task2panel.transform.forward  = Camera.main.transform.forward;
                }
            }
        }
        if (vInput.isRightEarDown()){
            if (vInput.isViewFocus(out hitObj)){
                if (hitObj.tag == "Selectable"){
                    task2panel.SetActiveRecursively(true);
                    task2panel.transform.position = Camera.main.transform.position + Camera.main.transform.forward * 100.0f;
                    task2panel.transform.forward  = Camera.main.transform.forward;
                }
            }
        }


        bool isSelected = false;
        // 手柄选中
        if (vInput.isHandleDown(out hitObj)){
            if (hitObj == test2targetSelector){
                isSelected = true;
            }
        }
        // 眼选中且耳确认
        if (vInput.isLeftEarDown() && vInput.isViewFocus(out hitObj)){
            if (hitObj == test2targetSelector){
                isSelected = true;
            }
        }

        // 完成测试
        if (isSelected){
            if (task2process == 0){
                startTime = Time.time;
            }

            task2process += 1;
            task2panel.SetActive(false);

            if (task2process < task2times){
                // 未完成测试
                // 生成不一样的任务目标
                while (true){
                    int selectorIdx = Random.Range(0, 3);
                    if (test1selectors[selectorIdx] != test1targetSelector){
                        test1targetSelector = test1selectors[selectorIdx];
                        break;
                    }
                }
                while (true){
                    int selectorIdx = Random.Range(0, 3);
                    if (test2selectors[selectorIdx] != test2targetSelector){
                        test2targetSelector = test2selectors[selectorIdx];
                        break;
                    }
                }
                for (int i = 0; i < 3; i++){
                    test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                        test1selectors[i] == test1targetSelector ? 
                        "Long Press Me" : ""
                    );
                }
                for (int i = 0; i < 3; i++){
                    test2selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                        test2selectors[i] == test2targetSelector ? 
                        "Click Me" : ""
                    );
                }
                // 提示信息
                infoText.text = "(" + task2process + "/" + task2times + "）\n";

            }else{
                // 完成测试
                isTask2Started = false;
                endTime = Time.time;
                for (int i = 0; i < 3; i++){
                    test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = "";
                }
                for (int i = 0; i < 3; i++){
                    test2selectors[i].transform.GetChild(0).GetComponent<Text>().text = "";
                }

                // 提示信息
                infoText.text = "(" + task2process + "/" + task2times + "）\n";
                infoText.text += "Test 2 Done\n";
                infoText.text += "time of " + (endTime - startTime).ToString("N2") + "s\n";
                messageText.text = "Test 2 Done\n";
                messageText.text += "time of " + (endTime - startTime).ToString("N2") + "s\n";

            }

            
        }
    }

    // 测试3开始
    void task3start()
    {
        // 开始计时
        // startTime = Time.time;
        task3process = 0;
        int idx = 0;
        // 生成不一样的任务目标
        idx = (task3process % 2 == 0) ? Random.Range(0, 3) : Random.Range(3, 6);
        test1targetSelector = test1selectors[idx];
        idx = Random.Range(0, 3);
        test2targetSelector = test2selectors[idx];

        for (int i = 0; i < 6; i++){
            test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                test1selectors[i] == test1targetSelector ? 
                "Long Press Me" : ""
            );
        }
        for (int i = 0; i < 3; i++){
            test2selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                test2selectors[i] == test2targetSelector ? 
                "Click Me" : ""
            );
        }


        // 提示信息
        // messageText.text = "Task 3 start\n";
        // messageText.text += "长按手柄以唤出菜单并按下\n";
    }

    // 测试3进行中
    void task3update()
    {
        GameObject hitObj;

        // 面前展开窗体
        if (vInput.isLeftHandleLongDown() || vInput.isRightHandleLongDown()){
            if (vInput.isHandleDown(out hitObj)){
                if (hitObj == test1targetSelector){
                    task2panel.SetActiveRecursively(true);
                    task2panel.transform.position = Camera.main.transform.position + Camera.main.transform.forward * 100.0f;
                    task2panel.transform.forward  = Camera.main.transform.forward;
                }
            }
        }
        if (vInput.isRightEarDown()){
            if (vInput.isViewFocus(out hitObj)){
                if (hitObj.tag == "Selectable"){
                    task2panel.SetActiveRecursively(true);
                    task2panel.transform.position = Camera.main.transform.position + Camera.main.transform.forward * 100.0f;
                    task2panel.transform.forward  = Camera.main.transform.forward;
                }
            }
        }


        bool isSelected = false;
        // 手柄选中
        if (vInput.isHandleDown(out hitObj)){
            if (hitObj == test2targetSelector){
                isSelected = true;
            }
        }
        // 眼选中且耳确认
        if (vInput.isLeftEarDown() && vInput.isViewFocus(out hitObj)){
            if (hitObj == test2targetSelector){
                isSelected = true;
            }
        }

        // 完成测试
        if (isSelected){
            if (task3process == 0){
                startTime = Time.time;
            }

            task3process += 1;
            task2panel.SetActive(false);

            if (task3process < task3times){
                // 未完成测试
                int idx = 0;
                // 生成不一样的任务目标
                idx = (task3process % 2 == 0) ? Random.Range(0, 3) : Random.Range(3, 6);
                test1targetSelector = test1selectors[idx];
                idx = Random.Range(0, 3);
                test2targetSelector = test2selectors[idx];

                for (int i = 0; i < 6; i++){
                    test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                        test1selectors[i] == test1targetSelector ? 
                        "Long Press Me" : ""
                    );
                }
                for (int i = 0; i < 3; i++){
                    test2selectors[i].transform.GetChild(0).GetComponent<Text>().text = (
                        test2selectors[i] == test2targetSelector ? 
                        "Click Me" : ""
                    );
                }
                // 提示信息
                infoText.text = "(" + task3process + "/" + task3times + "）\n";

            }else{
                // 完成测试
                isTask3Started = false;
                endTime = Time.time;
                for (int i = 0; i < 6; i++){
                    test1selectors[i].transform.GetChild(0).GetComponent<Text>().text = "";
                }
                for (int i = 0; i < 3; i++){
                    test2selectors[i].transform.GetChild(0).GetComponent<Text>().text = "";
                }

                // 提示信息
                infoText.text = "(" + task3process + "/" + task3times + "）\n";
                infoText.text += "Test 3 Done\n";
                infoText.text += "time of " + (endTime - startTime).ToString("N2") + "s\n";
                messageText.text = "Test 3 Done\n";
                messageText.text += "time of " + (endTime - startTime).ToString("N2") + "s\n";

            }

            
        }
    }

    public void startTest1()
    {
        
    }

    public void startTest2()
    {
        isTask2Started = !isTask2Started;
        messageText.text = isTask2Started ? "Task 2 start\n" : "Task 2 end\n";
    }
}
