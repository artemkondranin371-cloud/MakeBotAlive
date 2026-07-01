# 🔥 Keeps bot alive  

### 🛠️ **Keep Your Bots Alive Without a Server!**  

This repository is designed for **anyone who wants to keep their Telegram bot active daily** without paying for a server or knowing how to code.  

GitHub Actions will **automatically check your bots every day** and ensure they are working. If any bot has an issue, you'll be notified through your **primary bot**.

---

Why am I not relying on a solution like forwarding the BotToken to [@LaylaBot](https://t.me/LaylaBot) and letting it handle everything? Because it only runs when you send the /start command. It responds to your message, but otherwise, it remains inactive until you send something or a new update arrives. Instead, it's better to make API calls daily, such as getMe, getUpdates, and sendMessage, ensuring the bot stays active and performs tasks regularly.

---

If you don’t have a GitHub account, you should create one to manage your bot’s automation. Having your own account ensures that you keep your API tokens safe and in your control.

However, I plan to add a bot like [@MakeAliveBot](https://t.me/MakeAliveBot), which will automatically perform these tasks daily for all registered bots and send updates to their owners. Unfortunately, it’s offline right now, but I’ll update it when it’s available.

Until then, the best option is to fork this repository and run your own instance on GitHub.


---

## **🌟 Why Use This?**  
✅ **No Server Needed** – Runs on GitHub for free!  
✅ **Easy Setup** – Just fork, add variables, and enable workflows.  
✅ **Supports Multiple Bots** – Simply list multiple bot tokens.  
✅ **Error Notifications** – Get alerts if a bot stops working.  
✅ **Flexible Scheduling** – Adjust the workflow schedule anytime.  
✅ **Preserve Your Favorite Bot** – Don’t let your username taken by @BotSupport or [@Durov!](https://t.me/durov/195)

---

## **📌 How It Works**
1️⃣ **Fetches bot details** via `getMe` API  
2️⃣ **Gets bot updates** using `getUpdates` API  
3️⃣ **Saves bot info** in `Bot<id>.txt`  
4️⃣ **Sends the status** to your **Telegram channel (`CHAT_ID`)**  
5️⃣ **Notifies you** (`OWNER_ID`) if any bot has issues  

Each bot works independently, and **if a bot fails, the primary bot alerts you!** 🚨  

---

## **🛠️ Setup Guide**  

### **1️⃣ Fork & Clone**
Click the **"Fork"** button at the top-right of this repository to create your own copy.

If you want to edit locally, use:
```sh
git clone https://github.com/ankit-chaubey/MakeBotAlive.git
````


---

### 2️⃣ Add Required Variables
After forking the repository, go to **Settings > Secrets and Variables > Actions** and add the following variables:

### **🔑 Required Variables**
| Variable Name | Example Value | Description |
|--------------|--------------|-------------|
| `CHAT_ID` | `-1001234567890` | The Telegram **channel ID** where bot updates will be sent. |
| `OWNER_ID` | `93602376` | Your **Telegram user ID** for receiving error notifications. |
| `BOT_TOKENS` | `123456:ABCDEF 789012:GHIJKL 345678:MNOPQR` | Space-separated **list of bot tokens** (first bot is used for notifications). |

---

### **📌 How to Get These Values?**

1️⃣ **Find `CHAT_ID`**  
   - If it's a **private channel**, use [@WhichIdBot](https://t.me/WhichIdBot) and send `/start` and then select your channel to get the `chat_id`.  

2️⃣ **Find `OWNER_ID`**  
   - Similarly use [@WhichIdBot](https://t.me/WhichIdBot) and send `/start` again and then select your account to get the `owner_id`.   and it will show your **Telegram user ID**.  

3️⃣ **Get `BOT_TOKENS`**  
   - Create bots via [@BotFather](https://t.me/BotFather).  
   - Copy each bot’s **token** and add them in the list separated by spaces.  
   - The **first bot** will be used to notify you of errors.  

---

### ✅ **Example Setup**
If you have **three bots**, add this in **BOT_TOKENS**: `123456:ABCDEF 789012:GHIJKL 345678:MNOPQR`

- `123456:ABCDEF` → **Primary bot** (for error notifications).  
- `789012:GHIJKL` → Second bot.  
- `345678:MNOPQR` → Third bot.  

🔹 The first bot in BOT_TOKENS acts as the primary bot for sending error alerts.


---

### 3️⃣ Enable GitHub Actions

After forking:
- 1️⃣ Go to Actions tab
- 2️⃣ Click "Enable Workflows" (only needed for the first time)

This will automatically run at 00:00 UTC daily.


---

### 4️⃣ (Optional) Modify Run Time

To change the scheduled time, edit .github/workflows/bot.yml under:

schedule:
```
  - cron: "0 0 * * *"
```

🔹 Adjust the cron time (UTC) as needed.


---

🚀 Running the Script Manually

You can manually check bots anytime:
- 1️⃣ Go to Actions
- 2️⃣ Select "Run Bot Status Check"
- 3️⃣ Click "Run workflow"


---

### 📜 What It Sends?

- ✅ Success Message

- #Bot8116593190 is online ✅

- 📄 Bot Status File (Bot<id>.txt)

```
BotID: 12355689  
BotUsername: @YourBot  
Name: Bot Name  
Updates: {...}
```

- ⚠️ Error Alert (Sent to OWNER_ID)

```
⚠️ Error Detected!
Request: getMe
Bot Token Used: 123456:ABCDEF
Error Details: {JSON response}
```


---

### ⚙️ GitHub Actions Workflow (bot.yml)

```
name: Run Bot Status Check

on:
  schedule:
    - cron: "*/5 * * *"
  workflow_dispatch:

jobs:
  check-bots:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install requests

      - name: Run bot script
        env:
          CHAT_ID: ${{ secrets.CHAT_ID }}
          OWNER_ID: ${{ secrets.OWNER_ID }}
          BOT_TOKENS: ${{ secrets.BOT_TOKENS }}
        run: python bot.py
```


---

### 💡 Notes

- 🛠️ Works for unlimited bots (just list multiple tokens in BOT_TOKENS).

- 🚀 Runs automatically every day at 00:00 UTC.

- 🔔 Primary bot alerts you if any bot fails.

- 🎯 Modify workflow anytime to change the schedule or improve logic.



---

## **👨‍💻 Creator**  
This project is built by **[Ankit Chaubey](https://github.com/ankit-chaubey)**
- 📬 **Telegram:** [@ankify](https://t.me/ankify)
- 📧 **Email:** [📨📨📨📨](mailto:m.ankitchaubey@gmail.com)

---

💬 Need Help?

If you have any issues, open an issue in the repository.

🚀 Enjoy Free Automation! 🚀



