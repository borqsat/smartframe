package com.tizen.tizenrunner.api;

/**
 * TizenSnapshot interface.
 * This interface defines an image representing a screen snapshot.
 * @author Bao Hongbin
 */
public interface ISnapshot {
    boolean writeToFile(String path, String format);
}
