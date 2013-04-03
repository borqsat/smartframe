package com.tizen.tizenrunner.api;

/**
 * Target Device operation interface.
 * The device instance should provide the ability defined.
 * @author Bao Hongbin
 */
public interface IDevice {
    //take snapshot on device
	ISnapshot takeSnapshot();
    //touch x,y event on device
	boolean touch(int x, int y);
    //press the hard key of device. Like BACK POWER HOME MENU UP DOWN...
	boolean press(String key);
	//disconnect device
	void dispose();
 
}
