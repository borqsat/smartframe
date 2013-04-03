package com.tizen.tizenrunner;

import java.io.File;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * The entry of Program.
 * It holds a StubManager instance which control the target stub.
 * @author Bao Hongbin
 */
public class Runner {
    private final StubManager mStubManager;
    private final TizenRunnerOptions mOptions;

    /**
     * Constructor of Runner.
     * @param option object represent user input from command-line.
     */
    public Runner(TizenRunnerOptions option) {
    	mOptions = option;
        mStubManager = StubManager.getInstance(option);
        TizenRunner.setManager(mStubManager);
    }

    /**
     * The entry of Program.
     * @param args array represent user input content.
     */
    public static void main(String[] args) {
    	//parse user input
        TizenRunnerOptions options = TizenRunnerOptions.processOptions(args);
        if (options == null) {
            return;
        }

        try {
        	//check sdb exists.
			findSdb();
		} catch (Exception e) {
			e.printStackTrace();
		}
        
        Runner runner = new Runner(options);
        //start to execute script file
        int error = runner.run();
        System.exit(error);
    }

    /**
     * Start host-side loop.
     */
    private int run() {
        String tizenRunnerPath = System.getProperty("com.tizen.tizenrunner.bindir") +
                File.separator + "tizenrunner";
        if (mOptions.getScriptFile() == null) {
        	mStubManager.shutdown();
            return 0;
        } else {
            int error = ScriptRunner.run(tizenRunnerPath, mOptions.getScriptFile().getAbsolutePath(),
            		mOptions.getArguments());
            mStubManager.shutdown();
            //exit code
            return error;
        }
    }
    

    /**
     * Used to check the host-side environment. like sdb...
     */
    private static String findSdb() throws Exception {
    	Process process = null;
        try {
			process = Runtime.getRuntime().exec("which sdb");
		} catch (IOException e) {
			System.out.println("cant find sdb in $PATH");
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
        	System.out.println("read which sdb output exception");
        }finally{
        	if(is!=null){
        	    is.close();
        	}
        	if(errReader!=null){
        	    errReader.close();
        	}
        	if(process!=null){
        	    process.destroy();
        	}
        }

        if("".equals(sb.toString().trim())){
        	throw new Exception("sdb not found on system $path");
        }
        if(!sb.toString().contains("sdb")){
        	throw new Exception("sdb not found on system $path");        
        }
        return sb.toString();
    }
}