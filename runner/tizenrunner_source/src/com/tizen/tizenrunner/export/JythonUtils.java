package com.tizen.tizenrunner.export;

import java.lang.reflect.AccessibleObject;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.text.BreakIterator;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import org.python.core.ArgParser;
import org.python.core.Py;
import org.python.core.PyBoolean;
import org.python.core.PyDictionary;
import org.python.core.PyFloat;
import org.python.core.PyInteger;
import org.python.core.PyList;
import org.python.core.PyNone;
import org.python.core.PyObject;
import org.python.core.PyReflectedField;
import org.python.core.PyReflectedFunction;
import org.python.core.PyString;
import org.python.core.PyStringMap;
import org.python.core.PyTuple;
import org.python.google.common.base.Preconditions;
import org.python.google.common.base.Predicate;
import org.python.google.common.base.Predicates;
import org.python.google.common.collect.Collections2;
import org.python.google.common.collect.ImmutableMap;
import org.python.google.common.collect.ImmutableMap.Builder;
import org.python.google.common.collect.Lists;
import org.python.google.common.collect.Maps;
import org.python.google.common.collect.Sets;
import com.tizen.tizenrunner.export.RunnerExported;

/**
 * Open Source class
 * Collection of useful utilities function for interacting with the Jython interpreter.
 */
public final class JythonUtils {
    private JythonUtils() { }
    private static final Map<Class<? extends PyObject>, Class<?>> PYOBJECT_TO_JAVA_OBJECT_MAP;
    static {
        Builder<Class<? extends PyObject>, Class<?>> builder = ImmutableMap.builder();
        builder.put(PyString.class, String.class);
        builder.put(PyFloat.class, Double.class);
        builder.put(PyInteger.class, Integer.class);
        builder.put(PyBoolean.class, Boolean.class);
        PYOBJECT_TO_JAVA_OBJECT_MAP = builder.build();
    }

    public static ArgParser createArgParser(PyObject[] args, String[] kws) {
        StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
        StackTraceElement element = stackTrace[2];

        String methodName = element.getMethodName();
        String className = element.getClassName();

        Class<?> clz;
        try {
            clz = Class.forName(className);
        } catch (ClassNotFoundException e) {
        	System.out.println("Got exception:");
        	e.printStackTrace();
            return null;
        }

        Method m;

        try {
            m = clz.getMethod(methodName, PyObject[].class, String[].class);
        } catch (SecurityException e) {
        	e.printStackTrace();
            return null;
        } catch (NoSuchMethodException e) {
        	e.printStackTrace();
            return null;
        }

        RunnerExported annotation = m.getAnnotation(RunnerExported.class);
        return new ArgParser(methodName, args, kws,
                annotation.args());
    }

    public static double getFloat(ArgParser ap, int position) {
        PyObject arg = ap.getPyObject(position);

        if (Py.isInstance(arg, PyFloat.TYPE)) {
            return ((PyFloat) arg).asDouble();
        }
        if (Py.isInstance(arg, PyInteger.TYPE)) {
            return ((PyInteger) arg).asDouble();
        }
        throw Py.TypeError("Unable to parse argument: " + position);
    }

    public static double getFloat(ArgParser ap, int position, double defaultValue) {
        PyObject arg = ap.getPyObject(position, new PyFloat(defaultValue));

        if (Py.isInstance(arg, PyFloat.TYPE)) {
            return ((PyFloat) arg).asDouble();
        }
        if (Py.isInstance(arg, PyInteger.TYPE)) {
            return ((PyInteger) arg).asDouble();
        }
        throw Py.TypeError("Unable to parse argument: " + position);
    }

    public static List<Object> getList(ArgParser ap, int position) {
        PyObject arg = ap.getPyObject(position, Py.None);
        if (Py.isInstance(arg, PyNone.TYPE)) {
            return Collections.emptyList();
        }

        List<Object> ret = Lists.newArrayList();
        PyList array = (PyList) arg;
        for (int x = 0; x < array.__len__(); x++) {
            PyObject item = array.__getitem__(x);

            Class<?> javaClass = PYOBJECT_TO_JAVA_OBJECT_MAP.get(item.getClass());
            if (javaClass != null) {
                ret.add(item.__tojava__(javaClass));
            }
        }
        return ret;
    }

    public static Map<String, Object> getMap(ArgParser ap, int position) {
        PyObject arg = ap.getPyObject(position, Py.None);
        if (Py.isInstance(arg, PyNone.TYPE)) {
            return Collections.emptyMap();
        }

        Map<String, Object> ret = Maps.newHashMap();

        PyDictionary dict = (PyDictionary) arg;
        PyList items = dict.items();
        for (int x = 0; x < items.__len__(); x++) {
            PyTuple item = (PyTuple) items.__getitem__(x);
            String key = (String) item.__getitem__(0).__str__().__tojava__(String.class);
            PyObject value = item.__getitem__(1);
            Class<?> javaClass = PYOBJECT_TO_JAVA_OBJECT_MAP.get(value.getClass());
            if (javaClass != null) {
                ret.put(key, value.__tojava__(javaClass));
            }
        }
        return ret;
    }

    private static PyObject convertObject(Object o) {
        if (o instanceof String) {
            return new PyString((String) o);
        } else if (o instanceof Double) {
            return new PyFloat((Double) o);
        } else if (o instanceof Integer) {
            return new PyInteger((Integer) o);
        } else if (o instanceof Float) {
            float f = (Float) o;
            return new PyFloat(f);
        } else if (o instanceof Boolean) {
            return new PyBoolean((Boolean) o);
        }
        return Py.None;
    }

    public static PyDictionary convertMapToDict(Map<String, Object> map) {
        Map<PyObject, PyObject> resultMap = Maps.newHashMap();

        for (Entry<String, Object> entry : map.entrySet()) {
            resultMap.put(new PyString(entry.getKey()),
                    convertObject(entry.getValue()));
        }
        return new PyDictionary(resultMap);
    }

    public static void convertDocAnnotationsForClass(Class<?> clz, PyObject dict) {
      Preconditions.checkNotNull(dict);
      Preconditions.checkArgument(dict instanceof PyStringMap);

      if (clz.isAnnotationPresent(RunnerExported.class)) {
    	RunnerExported doc = clz.getAnnotation(RunnerExported.class);
        String fullDoc = buildClassDoc(doc, clz);
        dict.__setitem__("__doc__", new PyString(fullDoc));
      }

      Collection<String> functions = Sets.newHashSet();
      for (PyObject item : dict.asIterable()) {
        functions.add(item.toString());
      }

      functions = Collections2.filter(functions, new Predicate<String>() {
        @Override
        public boolean apply(String value) {
          return !value.startsWith("__");
        }
      });

      for (Method m : clz.getMethods()) {
        if (m.isAnnotationPresent(RunnerExported.class)) {
          String methodName = m.getName();
          PyObject pyFunc = dict.__finditem__(methodName);
          if (pyFunc != null && pyFunc instanceof PyReflectedFunction) {
            PyReflectedFunction realPyFunc = (PyReflectedFunction) pyFunc;
            RunnerExported doc = m.getAnnotation(RunnerExported.class);
            realPyFunc.__doc__ = new PyString(buildDoc(doc));
            functions.remove(methodName);
          }
        }
      }

      for (Field f : clz.getFields()) {
          if (f.isAnnotationPresent(RunnerExported.class)) {
              String fieldName = f.getName();
              PyObject pyField = dict.__finditem__(fieldName);
              if (pyField != null && pyField instanceof PyReflectedField) {
                 functions.remove(fieldName);
              }
            }
      }

      for (String name : functions) {
          dict.__delitem__(name);
      }
    }

    private static final Predicate<AccessibleObject> SHOULD_BE_DOCUMENTED = new Predicate<AccessibleObject>() {
         @Override
         public boolean apply(AccessibleObject ao) {
             return ao.isAnnotationPresent(RunnerExported.class);
         }
    };
    private static final Predicate<Field> IS_FIELD_STATIC = new Predicate<Field>() {
        @Override
        public boolean apply(Field f) {
            return (f.getModifiers() & Modifier.STATIC) != 0;
        }
    };

    private static String buildClassDoc(RunnerExported doc, Class<?> clz) {
        Collection<Field> annotatedFields = Collections2.filter(Arrays.asList(clz.getFields()), SHOULD_BE_DOCUMENTED);
        Collection<Field> staticFields = Collections2.filter(annotatedFields, IS_FIELD_STATIC);
        Collection<Field> nonStaticFields = Collections2.filter(annotatedFields, Predicates.not(IS_FIELD_STATIC));

        StringBuilder sb = new StringBuilder();
        for (String line : splitString(doc.doc(), 80)) {
            sb.append(line).append("\n");
        }
        if (staticFields.size() > 0) {
            sb.append("\nClass Fields: \n");
            for (Field f : staticFields) {
                sb.append(buildFieldDoc(f));
            }
        }
        if (nonStaticFields.size() > 0) {
            sb.append("\n\nFields: \n");
            for (Field f : nonStaticFields) {
                sb.append(buildFieldDoc(f));
            }
        }
        return sb.toString();
    }

    private static String buildFieldDoc(Field f) {
    	RunnerExported annotation = f.getAnnotation(RunnerExported.class);
       StringBuilder sb = new StringBuilder();
       int indentOffset = 2 + 3 + f.getName().length();
       String indent = makeIndent(indentOffset);
       sb.append("  ").append(f.getName()).append(" - ");
       boolean first = true;
       for (String line : splitString(annotation.doc(), 80 - indentOffset)) {
           if (first) {
               first = false;
               sb.append(line).append("\n");
           } else {
               sb.append(indent).append(line).append("\n");
           }
       }
       return sb.toString();
    }

    private static String buildDoc(RunnerExported doc) {
        Collection<String> docs = splitString(doc.doc(), 80);
        StringBuilder sb = new StringBuilder();
        for (String d : docs) {
            sb.append(d).append("\n");
        }

        if (doc.args() != null && doc.args().length > 0) {
            String[] args = doc.args();
            String[] argDocs = doc.argDocs();
            sb.append("\n  Args:\n");
            for (int x = 0; x < doc.args().length; x++) {
                sb.append("    ").append(args[x]);
                if (argDocs != null && argDocs.length > x) {
                    sb.append(" - ");
                    int indentOffset = args[x].length() + 3 + 4;
                    Collection<String> lines = splitString(argDocs[x], 80 - indentOffset);
                    boolean first = true;
                    String indent = makeIndent(indentOffset);
                    for (String line : lines) {
                        if (first) {
                            first = false;
                            sb.append(line).append("\n");
                        } else {
                            sb.append(indent).append(line).append("\n");
                        }
                    }
                }
            }
        }
        return sb.toString();
    }

    private static String makeIndent(int indentOffset) {
        if (indentOffset == 0) {
            return "";
        }
        StringBuffer sb = new StringBuffer();
        while (indentOffset > 0) {
            sb.append(' ');
            indentOffset--;
        }
        return sb.toString();
    }

    private static Collection<String> splitString(String source, int offset) {
        BreakIterator boundary = BreakIterator.getLineInstance();
        boundary.setText(source);

        List<String> lines = Lists.newArrayList();
        StringBuilder currentLine = new StringBuilder();
        int start = boundary.first();

        for (int end = boundary.next();
                end != BreakIterator.DONE;
                start = end, end = boundary.next()) {
            String b = source.substring(start, end);
            if (currentLine.length() + b.length() < offset) {
                currentLine.append(b);
            } else {
                lines.add(currentLine.toString());
                currentLine = new StringBuilder(b);
            }
        }
        lines.add(currentLine.toString());
        return lines;
    }

    public static Set<String> getMethodNames(Class<?> clazz) {
        HashSet<String> methodNames = new HashSet<String>();
        for (Method m: clazz.getMethods()) {
            if (m.isAnnotationPresent(RunnerExported.class)) {
                methodNames.add(m.getName());
            }
        }
        return methodNames;
    }
}
