package com.tizen.tizenrunner;

import org.python.core.ArgParser;
import org.python.core.ClassDictInit;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.google.common.base.Preconditions;
import com.tizen.tizenrunner.StubManager;
import com.tizen.tizenrunner.api.IDevice;
import com.tizen.tizenrunner.export.JythonUtils;
import com.tizen.tizenrunner.export.RunnerExported;

/**
 * The class provides the ability to call test runner API from python script.
 * @author Bao Hongbin
 */
@RunnerExported(doc = "runner for tizen")
public class TizenRunner extends PyObject implements ClassDictInit {
    private static StubManager manager;

	//The method will be called when the class is initialized. 
	//The method control a java class method visibility in jython.
    public static void classDictInit(PyObject dict) {
        JythonUtils.convertDocAnnotationsForClass(TizenRunner.class, dict);
    }

    public static void setManager(StubManager bm){
        manager = bm;
    }

    @RunnerExported(doc = "Wait for device connected to host-side",
    		args = {"timeout", "deviceId","localport","remoteport"})
    public static TizenDevice waitForConnection(PyObject[] args, String[] kws) {
        ArgParser ap = JythonUtils.createArgParser(args, kws);
        Preconditions.checkNotNull(ap);
        long timeout;
        try {
            double time = JythonUtils.getFloat(ap, 0);
            timeout = (long) (time * 1000.0);
        } catch (PyException e) {
            timeout = Long.MAX_VALUE;
        }
        //get tizen device implement
        IDevice device = manager.waitForConnection(timeout,ap.getString(1, ".*"),ap.getInt(2,3490),ap.getInt(3,3490));
        TizenDevice tizenDevice = new TizenDevice(device);
        return tizenDevice;
    }

    @RunnerExported(doc = "Pause the currently running program for the specified time")
    public static void sleep(PyObject[] args, String[] kws) {
        ArgParser ap = JythonUtils.createArgParser(args, kws);
        Preconditions.checkNotNull(ap);
        double seconds = JythonUtils.getFloat(ap, 0);
        long ms = (long) (seconds * 1000.0);
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
        	e.printStackTrace();
        }
    }

}
