# Anchor Stats

Automatically retrieve episode stats using Selenium.

## Requirements

Download chromedriver from <https://chromedriver.chromium.org/downloads>

```sh
pip3 install requirements.txt
```

## Usage

Write your email and password in `.env`. See `.env.sample` for example.

```sh
python3 run.py
```

to get stats.

```sh
python3 analyze.py
```

to analyze data. CSV files must be placed in `data`.
