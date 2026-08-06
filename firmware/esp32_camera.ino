#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// ---------------- WIFI ----------------
const char* ssid = "YourSSID...";
const char* password = "YourPassword...";

// ---------------- SERVER ----------------
String serverUrl = "http://YOUR_SERVER_IP:5000/upload";

// ---------------- CAMERA PINS (AI THINKER) ----------------
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(115200);
  Serial.println("\nESP32-CAM Starting...");

  // Camera config
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  // Init camera
  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("❌ Camera init failed");
    return;
  }

  Serial.println("✅ Camera ready");

  // WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi connected");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  Serial.println("\n👉 Press ENTER in Serial Monitor to capture image");
}

// ---------------- LOOP ----------------
void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      captureAndSend();
    }
  }
}

// ---------------- FUNCTION ----------------
void captureAndSend() {
  Serial.println("\n📸 Capturing image...");

  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("❌ Camera capture failed");
    return;
  }

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "image/jpeg");

  int httpResponseCode = http.POST(fb->buf, fb->len);

  if (httpResponseCode > 0) {
    Serial.print("✅ Image sent | HTTP ");
    Serial.println(httpResponseCode);
    Serial.println(http.getString());
  } else {
    Serial.print("❌ Send failed: ");
    Serial.println(httpResponseCode);
  }

  http.end();
  esp_camera_fb_return(fb);
}