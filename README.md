# Anchor Stats

Automatically retrieve episode stats using Selenium.

## Requirements

Download chromedriver from <https://chromedriver.chromium.org/downloads>.
For Ubuntu, [`install_chrome_and_driver_ubuntu.sh`](install_chrome_and_driver_ubuntu.sh) is available.

```sh
pip3 install requirements.txt
```

## Usage

Write your email and password in `.env`. See `.env.sample` for example.

```sh
python3 run.py
```

to get stats. This takes some time to fetech episode list depending on the number of episodes the podcast has.
Once you ran the program, `episodes.json` will be created. 

```sh
python3 run.py --json episodes.json
```

You can manually edit JSON file to save time.

If you want to run in headless mode, use

```sh
python run.py --headless
```

To analyze data, run

```sh
python3 analyze.py
```

CSV files must be placed in `data`.
