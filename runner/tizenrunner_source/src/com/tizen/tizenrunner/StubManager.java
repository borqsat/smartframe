package com.tizen.tizenrunner;

import com.tizen.tizenrunner.api.IDevice;
import com.tizen.tizenrunner.api.IDeviceStub;
import com.tizen.tizenrunner.impl.TizenStub;

/**
 * StubManager holds a TizenStub instance.
 * @author Bao Hongbin
 */
public class StubManager {
    private final IDeviceStub mStub;

    private StubManager(IDeviceStub stub) {
        this.mStub = stub;
    }

    /** 
     * Create a instance of StubManager.
     * @return a instance of StubManager
     */
    public static StubManager getInstance(TizenRunnerOptions option) {
    	IDeviceStub stub =  createTizenStub(option);
    	StubManager manager = new StubManager(stub);
        return manager;
    }
    
    private static IDeviceStub createTizenStub(TizenRunnerOptions option){
    	return new TizenStub(option);
    }
    
    
    /**
     * Get an instance of the target device.
     * @param timeout length of time to wait before timing out
     * @param serial the id of the device you want to connect to (not support yet)
     * @return an instance of the device
     */
    public IDevice waitForConnection(long timeout, String deviceId,int localPort,int remotePort){
        return mStub.waitForConnection(timeout, deviceId,localPort,remotePort);
    }

    /**
     * Get an instance of the target device by default setting.
     * @return an instance of the device
     */
    /**
    public IDevice waitForConnection(){
        return mStub.waitForConnection(Integer.MAX_VALUE, ".*");
    }
**/
    /**
     * Close StubManager.
     */
    public void shutdown(){
    	mStub.shutdown();
    }
}
