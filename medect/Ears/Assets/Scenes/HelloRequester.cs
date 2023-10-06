using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

public class HelloRequester : RunAbleThread
{
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5555");
            Debug.Log("Client Start");
            
            int numFailed = 0;

            for (int i = 0; i < 100000 && Running; i++)
            // while (Running)
            {
                // Thread.Sleep(5);
                Debug.Log("Sending Hello");
                client.SendFrame("Hello");
                
                string message = null;
                bool gotMessage = false;
                while (Running)
                {
                    gotMessage = client.TryReceiveFrameString(out message);
                    if (gotMessage){
                        numFailed = 0;
                        break;
                    }else{
                        numFailed += 1;
                        if (numFailed > 1000){
                            HelloClient.shouldReconnect = true;
                            break;
                        }
                        Debug.Log("waiting for message ... (" + Running + ")");
                    }
                    
                }

                if (HelloClient.shouldReconnect){
                    break;
                }

                if (gotMessage){
                    Debug.Log("Received " + message);
                    HelloClient.t += 1;

                    if (message[0] == '0'){
                        HelloClient.isLeftEarDown = false;
                    }else{
                        HelloClient.isLeftEarDown = true;
                    }

                    if (message[2] == '0'){
                        HelloClient.isRightEarDown = false;
                    }else{
                        HelloClient.isRightEarDown = true;
                    }
                }

                
            }
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}