package com.tizen.tizenrunner;

import java.io.File;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.core.PySystemState;
import org.python.google.common.collect.ImmutableMap;
import org.python.google.common.collect.ImmutableMap.Builder;
import org.python.google.common.collect.Lists;
import org.python.util.PythonInterpreter;

/**
 * Class for executing test case script.
 * @author Bao Hongbin
 */
public class ScriptRunner {
    private final Object scope;
    private final String variable;

    private ScriptRunner(Object scope, String variable) {
        this.scope = scope;
        this.variable = variable;
    }

    public static ScriptRunner newInstance(Object scope, String variable) {
        return new ScriptRunner(scope, variable);
    }

    public static int run(String executablePath, String scriptfilename,Collection<String> args) {
        File f = new File(scriptfilename);
        Collection<String> classpath = Lists.newArrayList(f.getParent());
        String[] argv = new String[args.size() + 1];
        argv[0] = f.getAbsolutePath();
        int x = 1;
        for (String arg : args) {
            argv[x++] = arg;
        }
        initPython(executablePath, classpath, argv);
        PythonInterpreter python = new PythonInterpreter();
        python.set("__name__", "__main__");
        python.set("__file__", scriptfilename);
        try {
          python.execfile(scriptfilename);
        } catch (PyException e) {
          if (Py.SystemExit.equals(e.type)) {
            return (Integer) e.value.__tojava__(Integer.class);
          }
          e.printStackTrace();
          return 1;
        }
        return 0;
    }
    
    
    public static void runString(String executablePath, String script) {
        initPython(executablePath);
        PythonInterpreter python = new PythonInterpreter();
        python.exec(script);
    }

    public static Map<String, PyObject> runStringAndGet(String executablePath,
            String script, String... names) {
        return runStringAndGet(executablePath, script, Arrays.asList(names));
    }

    public static Map<String, PyObject> runStringAndGet(String executablePath,
            String script, Collection<String> names) {
        initPython(executablePath);
        final PythonInterpreter python = new PythonInterpreter();
        python.exec(script);

        Builder<String, PyObject> builder = ImmutableMap.builder();
        for (String name : names) {
            builder.put(name, python.get(name));
        }
        return builder.build();
    }

    private static void initPython(String executablePath) {
        List<String> arg = Collections.emptyList();
        initPython(executablePath, arg, new String[] {""});
    }

    private static void initPython(String executablePath,
            Collection<String> pythonPath, String[] argv) {
        Properties props = new Properties();
        StringBuilder sb = new StringBuilder();
        sb.append(System.getProperty("java.class.path"));
        for (String p : pythonPath) {
            sb.append(":").append(p);
        }
        props.setProperty("python.path", sb.toString());
        props.setProperty("python.verbose", "error");
        props.setProperty("python.executable", executablePath);
        //props.setProperty("python.options.internalTablesImpl","weak");
        PythonInterpreter.initialize(System.getProperties(), props, argv);
        //if depend library not included in the release package.need to specify java.ext.dirs
        String frameworkDir = System.getProperty("java.ext.dirs");
        File tizenRunnerJar = new File(frameworkDir, "tizenrunner.jar");
        if (tizenRunnerJar.canRead()) {
            PySystemState.packageManager.addJar(tizenRunnerJar.getAbsolutePath(), false);
        }
    }

}
