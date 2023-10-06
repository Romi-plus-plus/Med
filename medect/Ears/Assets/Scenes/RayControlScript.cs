// 创建射线，记录选中对象和射线状态（存在与否）
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RayControlScript : MonoBehaviour
{
    // public VirtualInput vInput;
    public Transform rayPos;
    public LineRenderer rayLine;
    public int rayLength = 10;

    // 设置
    public bool isActive = true;
    public bool isShowFocus = true;

    // 可接出
    public bool isHit = false;
    public RaycastHit hit;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        // 射线开启与否
        gameObject.GetComponent<Renderer>().enabled = isActive;

        // 射线朝向跟随
        Ray ray = new Ray(rayPos.position, rayPos.forward);
        rayLine.SetPosition(0, ray.origin);
        isHit = Physics.Raycast(ray, out hit, rayLength);
        if (isHit) {
            rayLine.SetPosition(1, hit.point);
        } else {
            rayLine.SetPosition(1, ray.origin + ray.direction * rayLength);
        }
    }
}
