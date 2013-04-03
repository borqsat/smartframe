package com.tizen.tizenrunner;

import org.python.core.ArgParser;
import org.python.core.ClassDictInit;
import org.python.core.PyObject;
import org.python.google.common.base.Preconditions;
import com.tizen.tizenrunner.api.IDevice;
import com.tizen.tizenrunner.api.ISnapshot;
import com.tizen.tizenrunner.export.JythonUtils;
import com.tizen.tizenrunner.export.RunnerExported;

/**
 * A jython moudle written as a java class to provide the ability to call IDevice API from script.
 * Controlling a java class method visibility in jython.
 * @author Bao Hongbin
 */
@RunnerExported(doc = "Represents a tizen device.")
public class TizenDevice extends PyObject implements ClassDictInit {
	private static final long serialVersionUID = 1L;

	//The method will be called when the class is initialized. 
	//The method control a java class method visibility in jython.
	public static void classDictInit(PyObject dict) {
        JythonUtils.convertDocAnnotationsForClass(TizenDevice.class, dict);
    }

    private IDevice device;

    public TizenDevice(IDevice device) {
       this.device = device;
    }

    public IDevice getDevice() {
        return device;
    }

    @RunnerExported(doc ="Grab the device snapshot")
    public TizenImage takeSnapshot() {
        ISnapshot image = device.takeSnapshot();
        return new TizenImage(image);
    }

    @RunnerExported(doc = "Sends a touch event at the specified location")
    public void touch(PyObject[] args, String[] kws) {
        ArgParser ap = JythonUtils.createArgParser(args, kws);
        Preconditions.checkNotNull(ap);
        int x = ap.getInt(0);
        int y = ap.getInt(1);
        device.touch(x, y);
    }

    @RunnerExported(doc = "Send a hard key event to the specified key. Like HOME BACK MENU UP")
    public void press(PyObject[] args, String[] kws) {
        ArgParser ap = JythonUtils.createArgParser(args, kws);
        Preconditions.checkNotNull(ap);
        String name = ap.getString(0);
        device.press(name);
    }
    
    @RunnerExported(doc = "Wake up the screen on the device")
    public void wake(PyObject[] args, String[] kws) {
        ArgParser ap = JythonUtils.createArgParser(args, kws);
        Preconditions.checkNotNull(ap);
        //not support yet on tizen.
        //device.wake();
    }
}
