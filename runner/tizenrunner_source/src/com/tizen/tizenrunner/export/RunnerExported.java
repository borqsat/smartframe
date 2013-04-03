package com.tizen.tizenrunner.export;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Provide the ability to call public API from script.
 * Indicates that the annotated method is a public API to expose to the scripting interface.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target({ ElementType.METHOD, ElementType.CONSTRUCTOR,
          ElementType.TYPE, ElementType.FIELD })
public @interface RunnerExported {
    String doc();
    String[] args() default {};
    String[] argDocs() default {};
    String returns() default "";
}