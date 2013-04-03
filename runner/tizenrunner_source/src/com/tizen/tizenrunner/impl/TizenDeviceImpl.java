package com.tizen.tizenrunner.impl;

import java.net.Socket;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import com.tizen.tizenrunner.ConnectionManager;
import com.tizen.tizenrunner.api.IDevice;
import com.tizen.tizenrunner.api.ISnapshot;

/**
 * Connection library for setting up connection between host and device daemon.
 * @author Bao Hongbin
 */
public class TizenDeviceImpl implements IDevice {
	private static final String FORWARD_SDB[] = {"sdb","forward", "tcp:3490","tcp:3490"};
	private static final String START_DAEMON_SDB[] = {"sdb", "shell","GASClient","/dev/input/event0","/dev/input/event1"};	
	///may need future
	//private static final String START_SDB[] = {"sdb","start-server"};
	//private static final String STOP_SDB[] = {"sdb","kill-server"};
	//private static final String TIZEN_DEBUG_BRIDGE = "sdb";
	//private static final String COMMAND_STOP_SDBSERVER = "sdb kill-server";
	//private static final String COMMAND_STOP_STARTSERVER = "start-server";
	//private static final String COMMAND_STOP_SDBFORWARD = "sdb forward tcp:3490 tcp:3490";
	//private static final String COMMAND_INVOKE_DAEMON = "sdb shell GASClient /dev/input/event0 /dev/input/event1";
	//wait for 30s timeout
	private static final long MANAGER_CREATE_TIMEOUT_MS = 30 * 1000;
	private static final long MANAGER_CREATE_WAIT_MS = 3 * 1000;
    private static final String DEFAULT_DAEMON_ADDRESS = "127.0.0.1";
    private static final int DEFAULT_DAEMON_PORT = 3490;
    private ConnectionManager mConnectionManager;
    private String mHost;
    private int mLocalPort;
    private int mRemotePort;
    private String mDeviceId;
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    
	/**public TizenDeviceImpl(String ip,int port){
		mConnectionManager = createConnectionManager(ip, port);
	}**/
/**	
	public TizenDeviceImpl(String ip,int port,String serial){
		mConnectionManager = createConnectionManager(ip, port,serial);
	}
**/	
	public TizenDeviceImpl(String ip,String deviceId,int localPort,int remotePort){
		this.mDeviceId = deviceId;
		this.mHost = ip;
		this.mLocalPort = localPort;
		this.mRemotePort = remotePort;
		mConnectionManager = createConnectionManager();
	}
    
	/**
	 * Try to wait for the connection with device. Keep trying until get the server 
	 * first connection response or timeout(MANAGER_CREATE_TIMEOUT_MS);
	 * @param address device daemon host
	 * @param port device daemon port
	 * @return The instance of ConnectionManager
	 */
	private Socket daemonSocket;
	private ConnectionManager createConnectionManager() {
		InetAddress addr;
        try {
            addr = InetAddress.getByName(this.mHost);
        } catch (UnknownHostException e) {
        	e.printStackTrace();
            return null;
        }
		invokeDaemon();
        boolean success = false;
        ConnectionManager connectionManager = null;
        long start = System.currentTimeMillis();
        while (!success){
            sleep(MANAGER_CREATE_WAIT_MS);
            long now = System.currentTimeMillis();
            long diff = now - start;
            if (diff > MANAGER_CREATE_TIMEOUT_MS) {
                return null;
            }
            try {
            	daemonSocket = new Socket(addr, this.mLocalPort);
            } catch (IOException e) {
        	    success = false;
                continue;
            }
            
            try {
            	connectionManager = new ConnectionManager(daemonSocket);
            } catch (IOException e) {
            	success = false;
                continue;
            }
            
            try{
            	connectionManager.gotServerResponse();
            }catch(Exception e){
            	success = false;
            	continue;
            }
            success = true;
        }
        return connectionManager;
	}

	/**
	 * Touch Event
	 */
	@Override
	public boolean touch(int x, int y) {
		try{
	        return mConnectionManager.touch(x, y);
		}catch (IOException e) {
        	try{
				daemonSocket.close();
			}catch (IOException e1) {
				e1.printStackTrace();
			}
			e.printStackTrace();
		}
		return false;
	}
	
	/**
	 * Hard Key event.(shome,lhome)
	 */
	@Override
	public boolean press(String key) {
		try{
			return mConnectionManager.press(key);
		}catch (IOException e) {
        	try{
				daemonSocket.close();
			}catch (IOException e1) {
			    e1.printStackTrace();
			}
			e.printStackTrace();
		}
		return false;
	}

	/**
	 * Take current screen snapshot.
	 */
	@Override
	public ISnapshot takeSnapshot() {
		try{
			return new TizenSnapshot(mConnectionManager.takeSnapshot("TSC"));
		}catch (IOException e) {
        	try{
				daemonSocket.close();
			}catch (IOException e1) {
				e1.printStackTrace();
			}
			e.printStackTrace();
			return null;
		}
	}
	
	/**
	 *notify the device daemon  one task finished and need to release all resource.
	 */
    @Override
    public void dispose() {
        try {
        	if(mConnectionManager!=null){
        	    mConnectionManager.done();
        	    mConnectionManager.quit();
        	}
        	if(executor!=null){
        		executor.shutdown();
        	}
        }catch(Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Start device daemon. Execute sdb forward via sdb connection.
     * @param addr
     */
    public void invokeDaemon(){
      	if(DEFAULT_DAEMON_ADDRESS.equals(this.mHost)){
            if(!forwardSdb()){
            	//if device offline. program exit.
            	System.out.println("Device offline or sdb server error. try to reconnect again...");
            }
      	}
      	startDeviceDaemon();
    }
    
    /**
     * sdb forward if use sdb.
     * @return true if process execute over.
     */
    private boolean forwardSdb(){
    	Process process = null;
        int status = -1;
        //
        String forwardCmd;
        if(".*".equals(this.mDeviceId)){
        	forwardCmd = "sdb forward tcp:" + this.mLocalPort + " tcp:"+this.mRemotePort;
        }else{
        	forwardCmd = "sdb -s " + this.mDeviceId + " forward " + "tcp:" + this.mLocalPort + " tcp:"+this.mRemotePort;
        }
        try {
            ProcessBuilder processBuilder = new ProcessBuilder(forwardCmd.split(" "));
			process = processBuilder.start();
			status = process.waitFor();
		} catch (Exception e) {
			e.printStackTrace();
		}finally{
        	if(process!=null){
        		process.destroy();
        	}
        	if(process.getErrorStream()!=null){
        		try {
					process.getErrorStream().close();
				} catch (IOException e) {
					e.printStackTrace();
				}
        	}
        	if(process.getInputStream()!=null){
        		try {
					process.getInputStream().close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
        	}
        	if(process.getOutputStream()!=null){
        		try {
					process.getOutputStream().close();
				} catch (IOException e) {
					e.printStackTrace();
				}
        	}
		}
		if(status != 0){
			return false;
		}
		return true;
    }
    
    /**
     * Get the device daemon pid.
     * @return pid if process execute over. null if failed.
     */
    private String getGASClientId(){
    	Process process = null;
    	String cmd;
    	if(".*".equals(this.mDeviceId)){
    		cmd = "sdb shell pgrep GASClient";
    	}else{
    		cmd = "sdb -s "+ this.mDeviceId + " shell pgrep GASClient";
    	}
        try {
			process = Runtime.getRuntime().exec(cmd);
		} catch (IOException e) {
			System.out.println("sdb pgrep error");
			e.printStackTrace();
		}
        InputStreamReader is = new InputStreamReader(process.getInputStream());
        BufferedReader errReader = new BufferedReader(is);
        StringBuffer sb = null;
        try {
        	sb = new StringBuffer();
            while (true) {
                String line = errReader.readLine();
                if (line != null) {
                    sb.append(line);
                } else {
                    break;
                }
            }
        } catch (IOException e) {
        	return "null";
        }finally{
        	if(process!=null){
        		process.destroy();
        	}
        	if(process.getErrorStream()!=null){
        		try {
					process.getErrorStream().close();
				} catch (IOException e) {
					e.printStackTrace();
				}
        	}
        	if(process.getInputStream()!=null){
        		try {
					process.getInputStream().close();
				} catch (IOException e) {
					e.printStackTrace();
				}
        	}
        	if(process.getOutputStream()!=null){
        		try {
					process.getOutputStream().close();
				} catch (IOException e) {
					e.printStackTrace();
				}
        	}
        	
        }
        if("".equals(sb.toString().trim())){
        	return "null";
        }else{
            return sb.toString();	
        }    
    }


    private void asyncGrabProcessOutput(final Process process)
            throws InterruptedException {
        Thread t1 = new Thread("erroStream") {
            @Override
            public void run() {
                // create a buffer to read the stderr output
            	InputStream error = process.getErrorStream();
                InputStreamReader errorStream = new InputStreamReader(error);
                BufferedReader errorReader = new BufferedReader(errorStream);

                try {
                    while (true) {
                        String line = errorReader.readLine();
                        if (line != null) {
                        	line = null;
                        } else {
                            break;
                        }
                    }
                } catch (Exception e) {
                	//ingore
                }finally{
                	if(process!=null){
                		process.destroy();
                	}
                	try {
						error.close();
					} catch (IOException e) {
						e.printStackTrace();
					}
                }
                
            }
        };

        Thread t2 = new Thread("inputStream") {
            @Override
            public void run() {
            	InputStream input = process.getInputStream();
                InputStreamReader inputStream = new InputStreamReader(input);
                BufferedReader inputStreamReader = new BufferedReader(inputStream);

                try {
                    while (true) {
                        String line = inputStreamReader.readLine();
                        if (line != null) {
                        	line = null;
                        } else {
                            break;
                        }
                    }
                } catch (Exception e) {
                }finally{
                	if(process!=null){
                		process.destroy();
                	}
                	try {
						input.close();
					} catch (IOException e) {
						e.printStackTrace();
					}
                }
            }
        };
        t1.start();
        t2.start();
    }

    /**
     * Kill the device daemon if exists and start the device daemon.
     * @param commands system commands
     */
    private void startDeviceDaemon(){
    	String pid = getGASClientId();
    	if(!"null".equals(pid)){
    		String killCmd;
        	if(".*".equals(this.mDeviceId)){
        		killCmd = "sdb shell kill -9 " + pid;
        	}else{
        		killCmd = "sdb -s "+ this.mDeviceId + " kill -9 " + pid;
        	}
    	    try {
				Runtime.getRuntime().exec(killCmd);
			} catch (IOException e) {
				e.printStackTrace();
			}
    	}

        Process process = null;
        String invokeCmd;
    	if(".*".equals(this.mDeviceId)){
    		invokeCmd = "sdb shell GASClient /dev/input/event0 /dev/input/event1";
    	}else{
    		invokeCmd = "sdb -s "+ this.mDeviceId + " shell GASClient /dev/input/event0 /dev/input/event1";
    	}

        try {
            ProcessBuilder processBuilder = new ProcessBuilder(invokeCmd.split(" "));
            process = processBuilder.start();
            asyncGrabProcessOutput(process);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    
    /**
     * Idle time.
     * @param ms idle time
     */
    private void sleep(long ms){
        try {
			Thread.sleep(ms);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
    }
}
