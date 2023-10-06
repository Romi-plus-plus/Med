using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class ButtonHighlightScript : MonoBehaviour
{
    public VirtualInput vInput;
    public bool isHandleHighlight = true;
    public bool isEyeHighlight = false;

    public static Color normalColor = new Color(1.0f, 1.0f, 1.0f);
    public static Color highlightedColor = new Color(0.9f, 0.9f, 0.9f);
    public static Color pressedColor = new Color(0.7f, 0.7f, 0.7f);

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        // Debug.Log(this.gameObject);
        GameObject hitObj;
        if (isHandleHighlight){
            gameObject.GetComponent<Image>().color = normalColor;

            if (vInput.isLeftHandleFocus(out hitObj)){
                if (hitObj == gameObject){
                    if (vInput.isLeftHandleDown()){
                        gameObject.GetComponent<Image>().color = pressedColor;
                        return;
                    }else{
                        gameObject.GetComponent<Image>().color = highlightedColor;
                        return;
                    }
                }
            }

            if (vInput.isRightHandleFocus(out hitObj)){
                if (hitObj == gameObject){
                    if (vInput.isRightHandleDown()){
                        gameObject.GetComponent<Image>().color = pressedColor;
                        return;
                    }else{
                        gameObject.GetComponent<Image>().color = highlightedColor;
                        return;
                    }
                }
            }

            gameObject.GetComponent<Image>().color = normalColor;
        }

        if (isEyeHighlight && vInput.isVisualAid){
            if (vInput.isViewFocus(out hitObj)){
                if (hitObj == gameObject){
                    if (vInput.isLeftEarDown() || vInput.isRightEarDown()){
                        gameObject.GetComponent<Image>().color = pressedColor;
                        return;
                    }else{
                        gameObject.GetComponent<Image>().color = highlightedColor;
                        return;
                    }
                }
            }

            gameObject.GetComponent<Image>().color = normalColor;
        }

    }
}
