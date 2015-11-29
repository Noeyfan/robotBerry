using UnityEngine;
using System.Collections;
using RobotBerry;

public class client : MonoBehaviour {

	// Use this for initialization
	void Start () {
        Connector cntr = new Connector("10.0.0.4", 9999);
        cntr.Send("S");
	}
	
	// Update is called once per frame
	void Update () {
	
	}
}
