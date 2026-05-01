# Kana Learning App

Interactive Streamlit app for studying Japanese kana: hiragana, katakana, pronunciation patterns, and basic practice exercises.

## Project overview

This project is a small learning tool designed to organize and practise the Japanese writing systems hiragana and katakana.

The app includes:

- a structured kana table;
- filters by layer, row and script;
- a kana matrix;
- special pronunciation cases;
- practice quizzes for characters;
- practice quizzes for pronunciation patterns.

The goal is to transform study notes into structured, searchable and interactive learning material.

## Contents

The current version focuses on:

- hiragana;
- katakana;
- dakuten;
- handakuten;
- yōon combinations;
- special signs;
- long vowels;
- small tsu;
- final nasal sound;
- interactive practice.

## Project structure

```text
NIHONGO/
├── app/
│   └── app.py
├── data/
│   ├── kana.csv
│   └── kana_pronunciation_examples.csv
├── notebooks/
│   └── gambatte/
│       └── 01_build_kana_dataset.ipynb
├── requirements.txt
└── README.md

How to run locally

From the project root folder, run:

streamlit run app/app.py

If app.py is moved to the root folder, run:

streamlit run app.py
Requirements

Install the required Python packages with:

pip install -r requirements.txt
Technologies used
Python
pandas
Streamlit
CSV
Jupyter Notebook
Visual Studio Code
Current status

The kana module is complete as a first functional version.

Future development may include:

grammar modules;
vocabulary tables;
verb conjugation tables;
lesson-based navigation;
SQL database integration;
more advanced quizzes.
Author

Ana Rita Trindade