# 📚 Study Assistant

An AI-powered PDF and text summarizer built with Streamlit and Hugging Face Transformers.

## 🚀 Features

- Upload `.pdf` or `.txt` files
- Automatically extracts and summarizes content
- Uses `distilbart-cnn-12-6` for fast and accurate summarization
- Clean UI powered by Streamlit

## 🧠 Model

This app uses [DistilBART](https://huggingface.co/sshleifer/distilbart-cnn-12-6), a smaller, faster version of BART trained on CNN/DailyMail data.

## 📦 Requirements

Dependencies are listed in `requirements.txt`:
- streamlit
- transformers
- pdfplumber
- torch

## 🔧 Running the App Locally

```bash
pip install -r requirements.txt
streamlit run pdf_summarizer_app.py
