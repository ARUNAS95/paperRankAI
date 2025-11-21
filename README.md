# 📘 PaperRank AI --- Research Discovery Tool

*A user-friendly, explainable AI interface for ranking academic papers*

## 🔍 Overview

PaperRank AI is an intelligent research discovery tool that ranks
academic papers using explainable AI scoring. This Streamlit-based
interface makes the Madison agent accessible to non-technical users,
providing clean inputs, clear instructions, and professionally formatted
results.

This tool is designed as part of the Madison Framework assignment and
integrates directly with my portfolio.

## 🎯 Features

### ✅ User-Friendly Interface

-   Clean, intuitive design accessible to any user
-   Text input for research topics
-   Dropdown selector for ranking style
-   Large, accessible search button

### 🎨 Branding-Aligned UI

-   Custom dark theme inspired by PaperRank AI brand
-   Accent colors (#5BC0EB, #1C82FF, #A259FF)
-   Responsive layout with centered header and logo

### 🤖 AI-Powered Ranking

-   Sends query to n8n workflow
-   Retrieves AI-ranked papers
-   Displays results in card-style UI
-   CSV download support

### 🌐 Portfolio Integration

A direct link to the portfolio is included in the footer:\
https://arunasrtc.wixsite.com/paperrank-ai

## 🚀 Tech Stack

-   Python
-   Streamlit
-   Pandas
-   Requests
-   n8n Webhook backend

## 📥 Installation & Setup

### 1. Clone repository

    git clone https://github.com/yourusername/paperrank-ai.git
    cd paperrank-ai

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Run the app

    streamlit run app.py

## 🧠 How It Works

1.  User enters a research topic\
2.  AI backend processes & ranks papers\
3.  Results are displayed cleanly\
4.  User can export as CSV


