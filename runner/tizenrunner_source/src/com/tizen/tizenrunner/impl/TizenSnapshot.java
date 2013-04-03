package com.tizen.tizenrunner.impl;

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.BufferedOutputStream;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.ref.WeakReference;
import java.util.Iterator;

import javax.imageio.ImageIO;
import javax.imageio.ImageWriter;
import javax.imageio.stream.ImageOutputStream;

import com.tizen.tizenrunner.api.ISnapshot;

/**
 * Class used to represent snapshot image from tizen device.
 * @author Bao Hongbin
 */
public class TizenSnapshot implements ISnapshot {
	private final byte[] image;

    /**
     * Create a new instance of TizenSnapshot.
     * @param image the image data from device daemon.
     */
	TizenSnapshot(byte[] data) {
        this.image = data;
    }

	/**
	 * Write the snapshot to a local file.
	 */
    @Override
    public boolean writeToFile(String path, String format) {
        File myfile = null;
        BufferedOutputStream fileOut = null;
        try {
            myfile = new File(path);
            myfile.delete();
            try{
                fileOut = new BufferedOutputStream(new FileOutputStream(myfile));
			    fileOut.write(this.image);
            }catch(Exception e){
            	e.printStackTrace();
            }finally{
	            fileOut.flush();
	        	if(fileOut != null){
				    fileOut.close();
	        	}
            }
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
        return true;
    }
    
    private BufferedImage createBufferedImage(){
    	InputStream in = new ByteArrayInputStream(this.image);
    	try {
			return ImageIO.read(in);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    	return null;
    }
    
    private WeakReference<BufferedImage> cachedBufferedImage = null;    
    public BufferedImage getBufferedImage() {
        // Check the cache first
        if (cachedBufferedImage != null) {
            BufferedImage img = cachedBufferedImage.get();
            if (img != null) {
                return img;
            }
        }

        // Not in the cache, so create it and cache it.
        BufferedImage img = createBufferedImage();
        cachedBufferedImage = new WeakReference<BufferedImage>(img);
        return img;
    }
    
    private BufferedImage convertSnapshot() {
        BufferedImage image = getBufferedImage();

        // Convert the image to ARGB so ImageIO writes it out nicely
        BufferedImage argb = new BufferedImage(image.getWidth(), image.getHeight(),
                BufferedImage.TYPE_INT_ARGB);
        Graphics g = argb.createGraphics();
        g.drawImage(image, 0, 0, null);
        g.dispose();
        return argb;
    }
    
    private boolean writeToFileHelper(String path, String format) {
        BufferedImage argb = convertSnapshot();

        try {
            ImageIO.write(argb, format, new File(path));
        } catch (IOException e) {
            return false;
        }
        return true;
    }
    
	/**
	 * Write the snapshot to a local file.
	 */
   // @Override
    public boolean writeToFile2(String path, String format) {
        long start = System.currentTimeMillis();
        Iterator<ImageWriter> writers = ImageIO.getImageWritersBySuffix("png");
        if (!writers.hasNext()) {
        	//System.out.println("into helper??????????????????");
            return writeToFileHelper(path, "png");
        }
        ImageWriter writer = writers.next();
        BufferedImage image = convertSnapshot();
        try {
            File f = new File(path);
            f.delete();

            ImageOutputStream outputStream = ImageIO.createImageOutputStream(f);
            writer.setOutput(outputStream);

            try {
                writer.write(image);
            } finally {
                writer.dispose();
                outputStream.flush();
            }
        } catch (IOException e) {
            return false;
        }
        long now = System.currentTimeMillis();
        long diff = now - start;
    	System.out.println("write cost time:" + diff);
        return true;
    }
}