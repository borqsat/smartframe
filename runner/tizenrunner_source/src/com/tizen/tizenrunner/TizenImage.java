package com.tizen.tizenrunner;

import org.python.core.ArgParser;
import org.python.core.ClassDictInit;
import org.python.core.PyObject;
import org.python.google.common.base.Preconditions;
import com.tizen.tizenrunner.api.ISnapshot;
import com.tizen.tizenrunner.export.JythonUtils;
import com.tizen.tizenrunner.export.RunnerExported;

/**
 * This class provide the ability to use ISnapshot API from python script.
 * @author Bao Hongbin
 */
@RunnerExported(doc = "Tizen image object")
public class TizenImage extends PyObject implements ClassDictInit {
	private static final long serialVersionUID = 1L;

	//The method will be called when the class is initialized. 
	//The method control a java class method visibility in jython.
	public static void classDictInit(PyObject dict) {
        JythonUtils.convertDocAnnotationsForClass(TizenImage.class, dict);
    }

    private final ISnapshot mSnapshot;

    public TizenImage(ISnapshot snapshot) {
        this.mSnapshot = snapshot;
    }

    public ISnapshot getImpl() {
        return  mSnapshot;
    }

    @RunnerExported(doc = "Write a 'png' image to a file.")
    public boolean writeToFile(PyObject[] args, String[] kws) {
        ArgParser ap = JythonUtils.createArgParser(args, kws);
        Preconditions.checkNotNull(ap);
        String path = ap.getString(0);
        String format = ap.getString(1, null);
        return  mSnapshot.writeToFile(path, format);
    }

}
