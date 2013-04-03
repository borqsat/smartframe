package com.tizen.tizenrunner.impl;
import com.tizen.tizenrunner.TizenRunnerOptions;
import com.tizen.tizenrunner.api.IDevice;
import com.tizen.tizenrunner.api.IDeviceStub;

/**
 * Class for implement the IDeviceStub interface on Tizen.
 * It holds a TizenDeviceImpl instance which provides the ability to talk with device daemon.
 * @author Bao Hongbin
 */
public class TizenStub implements IDeviceStub {
	private String ipaddr = "127.0.0.1";
	//private int localport = 3490;
	private IDevice tizenDevice;
	
	
	public TizenStub(TizenRunnerOptions options){
    	ipaddr = options.getHost();
    	//localport = options.getPort();
	}

	/**
	@Override
	public IDevice waitForConnection() {
		tizenDevice = new TizenDeviceImpl(ipaddr,stubport);
		return tizenDevice;
	}
**/
	/**
	@Override
	public IDevice waitForConnection(long timeoutMs, String deviceId) {
		tizenDevice = new TizenDeviceImpl(ipaddr,localport,deviceId);
		return tizenDevice;
		
	}
**/
	@Override
	public IDevice waitForConnection(long timeoutMs, String deviceId,int localPort,int remotePort) {
		tizenDevice = new TizenDeviceImpl(ipaddr,deviceId,localPort,remotePort);
		return tizenDevice;
		
	}
	/**
	 * Disconnect from the device daemon.
	 */ 
	@Override
	public void shutdown() {
	       if(tizenDevice != null){
	           tizenDevice.dispose();
	       }
	}

}
