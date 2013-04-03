package com.tizen.tizenrunner;

import java.io.File;
import java.util.Collection;
import org.python.google.common.collect.ImmutableList;

/**
 * This class represent user input content from command-line.
 * @author Bao Hongbin
 */
public class TizenRunnerOptions {
	//local host address
    private static String DEFAULT_DAEMON_ADDRESS = "127.0.0.1";
    //default port of local forward needed
    private static int DEFAULT_LOCAL_PORT = 3490;
    private final String mHost;
    private final int mHostPort;
    private final File mScriptFile;
    private final Collection<String> mArguments;

    /**
     * Constructor
     * @param host the device daemon host address.
     * @param port the device daemon port.
     * @param scriptFile the test case script file.
     * @param arguments user input from command-line.
     */
    private TizenRunnerOptions(String host, int port, File scriptFile, Collection<String> arguments) {
        mHost = host;
        mHostPort = port;
        mScriptFile = scriptFile;
        mArguments = arguments;
    }

    /**
     * Get the device daemon host address.
     * @return 
     */
    public String getHost() {
        return mHost;
    }
    
    /**
     * Get the device daemon port.
     * @return the device daemon port.
     */
    public int getPort() {
        return mHostPort;
    }


    /**
     * Get the test case script file.
     * @return
     */
    public File getScriptFile() {
        return mScriptFile;
    }

    /**
     * Get the Option arguments
     * @return option arguments
     */
	public Collection<String> getArguments() {
		return mArguments;
	}
	
    /**
     * Process the user input from command-line.
     * @param args user input from command-line.
     * @return Object of TizenRunnerOption.
     */
    public static TizenRunnerOptions processOptions(String[] args) {
        String hostName = DEFAULT_DAEMON_ADDRESS;
        int port = DEFAULT_LOCAL_PORT;
        File scriptFile = null;
        int index = 0;
        ImmutableList.Builder<String> argumentBuilder = ImmutableList.builder();
        while (index < args.length) {
            String arg = args[index++];
            if ("-s".equals(arg)) {
                if (index == args.length) {
                    showUsage("No daemon address after -s");
                    return null;
                }
                hostName = args[index++];
            }else if ("-p".equals(arg)) {
                    // quick check on the next argument.
                    if (index == args.length) {
                        showUsage("Missing local port after -p");
                        return null;
                    }
                    port = Integer.parseInt(args[index++]);
            }else {
                if (scriptFile == null) {
                    scriptFile = new File(arg);
                    if (!scriptFile.exists()) {
                        showUsage("Fail to  open the specified script file");
                        return null;
                    }
                    if (!scriptFile.canRead()) {
                        showUsage("Fail to read the specified script file");
                        return null;
                    }
                } else {
                    argumentBuilder.add(arg);
                }
            }
        };

        return new TizenRunnerOptions(hostName, port, scriptFile,argumentBuilder.build());
    }
    
    /**
     * Print usage.
     * @param message error information
     */
    private static void showUsage(String message) {
        System.out.println(message);
        System.out.println("Usage: tizenrunner [options] SCRIPT_FILE");
        System.out.println("");
        System.out.println("    -s      Tizen Device IP Address.");
        System.out.println("");
        System.out.println("");
    }

}
