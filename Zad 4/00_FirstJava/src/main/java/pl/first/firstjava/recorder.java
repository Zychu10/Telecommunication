package pl.first.firstjava;

import javax.sound.sampled.*;
import java.io.File;

public class recorder {

    private AudioFormat audioFormat;
    private TargetDataLine targetDataLine;

    class CaptureThread extends Thread {

        public void run() {
            AudioFileFormat.Type fileType = AudioFileFormat.Type.WAVE;
            File audioFile = new File("record");
            try {
                targetDataLine.open(audioFormat);
                targetDataLine.start();
                AudioSystem.write(new AudioInputStream(targetDataLine), fileType, audioFile);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public void click() {
        try {
            System.in.read();
        } catch (Exception e) {
        }
    }

    public void captureAudio() {
        try {
            audioFormat = new AudioFormat(2000.0F, 8, 1, true, false);
            // sampleRate, sampleSizeInBits, channels, signed, bigEndian)
            DataLine.Info dataLineInfo = new DataLine.Info(TargetDataLine.class, audioFormat);
            targetDataLine = (TargetDataLine) AudioSystem.getLine(dataLineInfo);
            CaptureThread captureThread = new CaptureThread();
            captureThread.start();
        } catch (NullPointerException e) {
            System.out.println("error");
        } catch (IllegalArgumentException | LineUnavailableException e) {
            System.out.println("error");
            System.exit(0);
        }
    }

    public void stopAudio() {
        targetDataLine.stop();
        targetDataLine.close();
    }

    public void playRecord() {
        try {
            Clip clip = AudioSystem.getClip();
            File record = new File("record");
            clip.open(AudioSystem.getAudioInputStream(record));
            clip.start();
            Thread.sleep(clip.getMicrosecondLength() / 1000);
        } catch (Exception exc) {
            System.out.println("error");
        }
    }
}
