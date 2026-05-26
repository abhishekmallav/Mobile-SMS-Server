# Mobile SMS Server

An Android application built with Python that turns your smartphone into a local area network HTTP gateway. Connect to your phone via REST API from your computer to programmatically send SMS messages over WiFi.

## The Intuition Behind the Project

**Why pay for cloud SMS APIs when you already have a phone plan?**

During feature development, developers often need a way to test and send automated SMS messages (like OTPs or server alerts) locally. Cloud services like Twilio or Plivo charge per message. Nowadays, we barely use the SMS quota provided with our mobile recharges. This project was born out of the idea to utilize that unused SMS quota to act as a free, local SMS microservice substitute to cloud services for local development. 

By running a lightweight Flask server on the Android device (packaged via Kivy and Buildozer), and bridging Python to native Android Java APIs using `pyjnius`, it converts your phone into a powerful programmable hardware node. All communication operates entirely locally on your device and network, ensuring maximum privacy.

## Features

- **100% Local and Private**: The app operates entirely on your local network. No external servers or cloud services are involved.
- **RESTful API**: Simple HTTP POST endpoints to trigger mobile functions.
- **SMS Gateway**: Send text messages programmatically via `android.telephony.SmsManager`.
- **Simple UI**: A Kivy-built dashboard on the phone displaying the local network IP and real-time HTTP request logs.
- **Background Execution**: Flask runs cleanly in a daemonized background thread with Native Android Persistent Notifications.

*Note on Camera Permission: The app requests Camera permission solely for a test endpoint that toggles the device flashlight. This endpoint exists purely to verify the Python-to-Java JNI hardware connection is functioning properly, independent of carrier SMS statuses.*

## Project Structure

```text
Mobile-SMS-Server
 |-- main.py          # Kivy application, UI layout, and Android permission requests
 |-- server.py        # Flask HTTP server and log management (runs in background)
 |-- sms.py           # PyJNIus bridge for Android native SMS sending
 |-- flashlight.py    # PyJNIus bridge for Android Camera2 API (Torch mode)
 |-- notification.py  # PyJNIus bridge for Android persistent notifications
 |-- buildozer.spec   # Buildozer packaging configuration for the Android APK
 |-- README.md        # Project documentation
```

## Setup & Installation

### Option 1: Download the APK
You can download the pre-built APK directly from the **Releases** tab of this repository and install it directly onto your Android device.

### Option 2: Build from Source
Ensure you have Python installed along with the required system dependencies for Android compilation (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libffi-dev libssl-dev cmake
```

Use `uv` (recommended) or `pip` to set up your environment:
```bash
uv venv
source .venv/bin/activate
uv pip install kivy flask pyjnius buildozer cython
```

Connect your Android phone via USB (with Developer Options & USB Debugging enabled) and run:
```bash
buildozer android debug deploy run logcat
```
*Note: The first build pulls the Android SDK/NDK and will take quite a while (60 - 90 minutes). Subsequent builds only take a few minutes.*

## Usage

1. Open the **SMS Server** app on your Android device.
2. Tap **Start Server**. It will display the phone's IP address (e.g., `Server IP: 192.168.1.100 : 5000`).
3. Send requests from any computer on the same WiFi network.

**Test Connection:**
```bash
curl http://<PHONE_IP>:5000/api/test
```

**Send an SMS:**
```bash
curl -X POST http://<PHONE_IP>:5000/api/sms \
  -H "Content-Type: application/json" \
  -d '{"number": "+1234567890", "message": "123456 is your verification code."}'
```

**Toggle Flashlight (Server Connection Test):**
```bash
curl -X POST http://<PHONE_IP>:5000/api/flashlight \
  -H "Content-Type: application/json" \
  -d '{"state": true}'
```

## Author

* Developed by **Abhishek**
* GitHub: [@abhishekmallav](https://github.com/abhishekmallav)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abhishekmallav)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:abhimallav1439@gmail.com?subject=Hello%20There&body=Just%20wanted%20to%20say%20hi!)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/abhishekmallav)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://www.x.com/abhishekmallav)
