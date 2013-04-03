package com.tizen.tizenrunner;
import java.net.Socket;
import java.io.InputStream;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.io.IOException;

/**
 * This class provides the ability to interact with the daemon on device.
 * The class instance holds the connection between host and device.
 * @author Bao Hongbin
 */
public class ConnectionManager{
    public static final int MAX_BUF_SIZE = 4096;
    public static final int MAX_CMD_SIZE = 100;
    public static final int MAX_MSG_SIZE = 100;
    public static final String BUFFER_CODEC = "UTF-8";
    private Socket gasSocket;
    private BufferedWriter gasWriter;
    private InputStream dataInput; 
    
    /**
     * Create instance for ConnectionManager.
     * @param socket the socket between host-side and the device daemon.
     * @throws IOException if socket init exception.
     */
    public ConnectionManager(Socket socket) throws IOException {
        gasSocket = socket;
        gasSocket.setSoTimeout(5000);
        gasWriter = new BufferedWriter(new OutputStreamWriter(gasSocket.getOutputStream()));
        dataInput = gasSocket.getInputStream();
    }

    /**
     * Get the welcome message from device daemon. Used to make sure the daemon already started.
     * This will block until connection successfully.
     * @return true if connection setup successfully. false if exception.
     * @throws IOException if read from input stream timeout.
     */
    public boolean gotServerResponse(){
        byte[] res = new byte[MAX_MSG_SIZE];
        int i = 0;
		try {
			i = dataInput.read(res);
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}finally{
			res = null;
		}
        return true;
    }

    /**
     * Press a hard key on the device.
     * @param keyname the name of the hard key. Like SHOME LHOME MENU POWER....
     * @return true or false
     * @throws IOException on error communicating with the device
     */
    public boolean press(String keyname) throws IOException {
        return sendEvent(keyname);
    }

    /**
     * Touch the specified location(x,y) of devices.
     * @param x the x coordinate of the location.
     * @param y the y coordinate of the location.
     * @return true or false.
     * @throws IOException on error communicating with the device.
     */
    public boolean touch(int x, int y) throws IOException {
        return sendEvent("TOUCH " + x + " " + y);
    }

    /**
     * Send event to the target device via sdb or netowork connection.
     * @param command the supported command which send to the device.
     * @return true or false.
     * @throws IOException on error communicating with the device.
     */
    synchronized private boolean sendEvent(String command) throws IOException {     
            String resp = sendGASEventAndGetResponse(command);
            return checkResponse(resp);
    }

    /**
     * Check the device daemon response.
     * @param resp the response
     * @return true or false
     */
    private boolean checkResponse(String resp) {
        if (resp == null) {
            return false;
        }
        resp = null;
        return true;
    }
    
    /**
     * Send event to the target tizen device via sdb or netowork connection.
     * @param command the supported command which send to the device.
     * @return true or false.
     * @throws IOException on error communicating with the device.
     */
    private String sendGASEventAndGetResponse(String command) throws IOException {
        command = command.trim();
        gasWriter.write(command);
        gasWriter.flush();
        byte[] res = new byte[MAX_MSG_SIZE];
        int i = dataInput.read(res);
        String s = new String(res,0,i);
        res = null;
        return s;
    }
    
    /**
     * Grab screen snapshot from device.
     * resp byte size 100,
     * @param command the snapshot command supported by the device.
     * @return the snapshot file bytes.
     * @throws IOException on error communicating with the device.
     */    
    synchronized public byte[] takeSnapshot(String command) throws IOException{
            command = command.trim();
            gasWriter.write(command);
            gasWriter.flush();
            //got snapshot bytes size
            byte[] buffer = new byte[MAX_MSG_SIZE];
            dataInput.read(buffer, 0, buffer.length);
            int size = Integer.parseInt((new String(buffer,BUFFER_CODEC)).trim());
            buffer = null;
            byte[] snapshot = new byte[size];
            int readCount = 0;
            while (readCount < size) {
                readCount += dataInput.read(snapshot, readCount, size - readCount);
            }
            return snapshot;
    }
    
    /**
     * Close related resources.
     */
    public void close() {
        try {
            gasSocket.close();
        } catch (IOException e) {
        	e.printStackTrace();
        }
        try {
        	dataInput.close();
        } catch (IOException e) {
        	e.printStackTrace();
        }
        try {
            gasWriter.close();
        } catch (IOException e) {
        	e.printStackTrace();
        }
    }

    /**
     * Notify the device daemon a task finished.
     * @throws IOException on error communicating with the device
     */
    public void done() throws IOException {
        synchronized (this) {
            gasWriter.write("FINISH");
            gasWriter.flush();     
        }
    }

    /**
     * Resource released.
     * @throws IOException on error communicating with the device.
     */
    public void quit() throws IOException {
        synchronized (this) {
                close();
        }
    }
    
    
    /**
     * Not support yet.
     * Wake the device up from sleep status.
     * @throws IOException on error communicating with the device
     */
    public void wake() throws IOException {
        sendEvent("wake");
    }
    
    /**
     * Make sure the resources released when host-side shutdown.
     * @throws IOException on error communicating with the device
     */    
    protected void finalize() throws Throwable {
        try {
            close();
        }catch(Exception e){
        	//ingore
            }finally{
                super.finalize();
            }
    }
}