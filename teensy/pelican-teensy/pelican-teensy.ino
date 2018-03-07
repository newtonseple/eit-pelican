#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>

// Audio processing from GUI
// GUItool: begin automatically generated code
  AudioInputAnalog         adc1;           //xy=233.3333282470703,183.33334350585938
  AudioAnalyzeFFT256       fft256_1;       //xy=384.33331298828125,183.33334350585938
  AudioConnection          patchCord1(adc1, fft256_1);
// GUItool: end automatically generated code

void setup() {
  
  AudioMemory(20); // Allocate memory for Audio
  
  fft256_1.averageTogether(8); // Set number of consecutive averaged ffts (~300 per second with no averaging)
  Serial.begin(115200); //USB always 12 Mbit/sec
  Serial.println("Started");
}

void loop() {
  // Audio debug lines
  //Serial.println(fft256_1.available());
  //Serial.println(AudioProcessorUsage()); 
  //Serial.println(AudioMemoryUsage());

  // Read each bin
  for (int i=0; i<128;i++){
    Serial.print(fft256_1.read(i));
    Serial.print(" ");
  }
  
  Serial.println(); //Finish spectrum line
  
  delay(20); // Run everything at this approximate period

}
