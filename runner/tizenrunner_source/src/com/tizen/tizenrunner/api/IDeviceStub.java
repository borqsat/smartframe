package com.tizen.tizenrunner.api;

/**
 * Interface between the StubManager API and the TizenRunner that communicates with GASClient.
 * @author Bao Hongbin
 */
public interface IDeviceStub {
    //IDevice waitForConnection();
    //IDevice waitForConnection(long timeout, String deviceId);
    IDevice waitForConnection(long timeout, String deviceId,int localPort,int remotePort);
    void shutdown();
}
