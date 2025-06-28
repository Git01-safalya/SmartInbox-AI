# 📬 SmartInbox AI – Local Gmail Summarizer using IBM Granite

SmartInbox AI is an offline assistant that fetches **unread Gmail messages** and uses **IBM Granite 3.2 models** (via Ollama) to summarize them and extract key action items.

It is built for the **AI & Automation Unpacked Hackathon (June 2025)** and prioritizes **privacy, simplicity, and enterprise usability**.

---

## 🚀 Features

* 🧠 Runs locally using **Granite 3.2 8B** via Ollama
* 📧 Connects to Gmail using IMAP and App Password
* ✍️ Summarizes **unread emails**
* ✅ Automatically marks fetched emails as read
* 🖥️ Interactive UI built with **Streamlit**
* 🔒 No cloud API needed – works fully offline

---

## 🛠️ Tech Stack

* [x] Python 3.10+
* [x] Streamlit
* [x] IMAP (via `imaplib`)
* [x] IBM Granite on [Ollama](https://ollama.com)

---

## 📦 Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Install [Ollama](https://ollama.com/download)

```bash
ollama pull granite3.2:8b
```

### 3. Enable Gmail IMAP

* [Turn on IMAP](https://mail.google.com/mail/u/0/#settings/fwdandpop)
* Create a [Gmail App Password](https://myaccount.google.com/apppasswords)

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🧪 Demo Use Case

> You paste your Gmail + App Password → SmartInbox fetches your unread emails → summarizes them → shows actions like "reply by tomorrow" or "schedule meeting" → powered by **IBM Granite**.

---

## 🧠 IBM Granite Usage

We use IBM’s `granite3.2:8b` model locally via **Ollama**. Prompt text is piped to the model using `subprocess.Popen`. The AI:

* Understands plain email text
* Summarizes and structures content
* Returns output directly to the UI

IBM Granite gives us trusted, open-source LLM capabilities **without requiring cloud calls** – ideal for sensitive emails.

---


## 📹 Demo Video

🎬 [Watch the 3-minute demo] (https://youtu.be/UI1gd6UXJfw)

---

## 📂 Folder Structure

```
smartinbox-ai/
├── app.py                # Streamlit app
├── email_reader.py       # Gmail fetch logic
├── requirements.txt
├── README.md            
```
