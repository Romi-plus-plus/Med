// 通信
using UnityEngine;
using UnityEngine.UI;

public class HelloClient : MonoBehaviour
{
    private HelloRequester _helloRequester;
    public Text comMessage1;
    public Text comMessage2;
    private bool isStarted = false;

    public static int t = 0;
    public static bool isLeftEarDown = false;
    public static bool isRightEarDown = false;
    public static bool shouldReconnect = false;

    public bool flagLeftEarDown = false;
    public bool flagRightEarDown = false;

    public bool useFakeInput = false; //替代性按键 (注:将会覆盖)
    public KeyCode fakeInputLeftKey = KeyCode.A;
    public KeyCode fakeInputRightKey = KeyCode.A;


    private void Start()
    {

    }

    public void StartCom()
    {
        Debug.Log("Start Com");
        if (!isStarted){
            isStarted = true;
            _helloRequester = new HelloRequester();
            _helloRequester.Start();
        }
    }

    public void StopCom()
    {
        Debug.Log("Stop Com");
        if (isStarted){
            isStarted = false;
            _helloRequester.Stop();
        }        
    }

    private void OnDestroy()
    {
        StopCom();
    }

    void FixedUpdate()
    {
        if (useFakeInput){
            HelloClient.isLeftEarDown = Input.GetKey(fakeInputLeftKey);
            HelloClient.isRightEarDown = Input.GetKey(fakeInputRightKey);
        }

        flagLeftEarDown = HelloClient.isLeftEarDown;
        flagRightEarDown = HelloClient.isRightEarDown;

        comMessage1.text = "" + t;
        comMessage2.text = "" + t;

        if (HelloClient.shouldReconnect){
            StopCom();
            StartCom();
            HelloClient.shouldReconnect = false;
        }
    }
}