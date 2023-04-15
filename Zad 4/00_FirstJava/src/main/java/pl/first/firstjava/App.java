package pl.first.firstjava;


import javax.sound.sampled.*;
import java.io.File;
import java.io.IOException;

public class App {

    public static void main(String[] args) {
        recorder record = new recorder();
        System.out.println("Nacisnij aby rozpoczac nagrywanie");
        record.click();
        record.captureAudio();

        System.out.println("Nacisnij aby zakonczyc nagrywanie");
        record.click();
        record.stopAudio();
        record.click();
        System.out.println("Nagrywanie zakonczone, nacisnij aby odtworzyc nagrywanie");

        record.playRecord();
    }
}
