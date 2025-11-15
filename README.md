# InSync – AI-Powered Accessibility Tool  
_Built in under **48 hours** as part of the **1M1B Workplace Experience Program** (4-day sprint)._

InSync is an accessibility-focused application designed to bridge communication gaps between hearing, speech, and sign-language users.  
It provides **real-time speech-to-text** and **sign-language recognition** through an AI-driven pipeline.

---

## 🚀 Overview

**InSync** includes:

- **Real-Time Speech-to-Text** (Web Speech API)
- **Camera-based Sign Language to Text Recognition**
- **ISL model support planned**
- Flask backend + HTML/CSS/JS frontend

InSync aims to democratize accessible communication tools using open-source technologies.

---

## 🎯 Problem Statement

Millions rely on sign language, yet:

- ISL (Indian Sign Language) datasets are scarce  
- Existing tools are expensive or require paid APIs  
- Real-time communication support is limited in public systems  

**InSync solves this by implementing a free, open-source, browser-compatible solution for both speech-to-text and sign recognition.**

---

## ✨ Features

### 🔊 1. Real-Time Speech to Text
- Powered by the **Web Speech API**
- Live transcription (updates continuously)
- Captures full conversation history
- Completely free (browser-based)

### 🤟 2. Sign Language to Text (Prototype)
- Uses **MediaPipe Hands** for landmark extraction
- LSTM model (trained on ASL subset)
- Frame-by-frame detection via webcam
- Modular design → ready to plug in ISL model later

### 🎥 3. Live Camera-Based Detection
- Real-time frame capture from webcam
- Sent to Flask backend for model inference
- Outputs predicted sign + confidence

## 🛠️ Tech Stack

### Frontend  
- HTML  
- CSS  
- JavaScript  
- Web Speech API  
- MediaDevices Camera API  

### Backend  
- Python  
- Flask  
- OpenCV  
- MediaPipe  
- TensorFlow / Keras  
- NumPy  
---

## 📁 Project Structure

> This is a high-level overview based on the current repo layout.

```bash
Greenie-chat/
├─ app.py               # Main Flask application
├─ requirements.txt     # Python dependencies
├─ index.html
├─ visibility.html
├─ hearing.html
├─ style.css
└─ README.md            # You are here :)
