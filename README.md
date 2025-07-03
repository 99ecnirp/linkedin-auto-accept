````markdown
# 🤖 LinkedIn Auto-Accept Bot

Automatically accept all pending LinkedIn connection requests using Selenium 🧠⚙️

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Selenium](https://img.shields.io/badge/selenium-automation-brightgreen)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## 📌 Features

- ✅ Automatically logs into LinkedIn (secure via `.env`)
- ✅ Scrolls or clicks "Load more" to fetch all pending invites
- ✅ Accepts all visible connection requests
- ✅ Retry logic on failed clicks
- ✅ Headless mode support

---

## 🚀 Demo

```bash
$ python main.py
````

```
[*] Clicking 'Load more' buttons to load all invites...
[+] Clicked 'Load more'
...
[+] All invitations loaded.
[*] Accepting connection requests...
[1] Accepted on attempt 1
[2] Accepted on attempt 1
...
Script complete.
```

---

## 🛠 Requirements

* Python 3.8+
* Chrome Browser (latest)
* ChromeDriver (matching your Chrome version)

Install dependencies:

```bash
pip install selenium python-dotenv
```

---

## 📁 Setup

1. **Clone the repo**

```bash
git clone https://github.com/YOUR_USERNAME/linkedin-auto-accept.git
cd linkedin-auto-accept
```

2. **Create a `.env` file** in the root folder:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_linkedIn_password
HEADLESS=false
RETRY_ATTEMPTS=3
```

3. **Download `chromedriver.exe`**

* Match version from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
* Place it under:

  ```
  chrome-win64/chromedriver.exe
  ```

4. **Run the bot**

```bash
python main.py
```

---

## 🔐 Security Note

* Your credentials are stored in `.env`. **Never commit this file.**
* Consider using **app-specific passwords** or secure vaults if you're concerned about safety.

---

## 📦 Project Structure

```
linkedin-auto-accept/
│
├── main.py              # Main script to auto-accept invites
├── .env                 # Your private credentials (not committed)
├── .gitignore           # Prevents pushing sensitive files
├── chrome-win64/
│   └── chromedriver.exe # Required WebDriver for Selenium
└── README.md            # You’re reading this
```

---

## ❗ Common Issues

**🔺 `stale element reference`**

> This happens when LinkedIn DOM updates. The script has retry logic built-in. You can ignore occasional logs.

**🔺 `NoSuchElementException`**

> Usually means LinkedIn layout changed. Inspect and update XPath or CSS selectors in `main.py`.

---

## 🧠 To-Do Ideas

* [ ] Auto-refresh every X minutes
* [ ] Accept based on filters (e.g. keywords, location, mutuals)
* [ ] Email/Telegram notification after acceptance

---

## 📜 License

MIT License © [Your Name](https://github.com/YOUR_USERNAME)

---

## ❤️ Support

If this helped you:

* ⭐ Star the repo
* 🐛 Open an issue for bugs
* 🙌 Suggest improvements via PR

````

---

### ✅ Next Step

Save this as `README.md` in your project root, then commit and push:

```bash
git add README.md
git commit -m "Add complete project README"
git push origin main

