# whatsapp_mass_dm

Unofficial WhatsApp bulk messaging tool. Simple setup, easy to use.
Built on the WaSender API — no WhatsApp Business account needed.

---

## How It Works

```
1. Clone the repo
2. Add your phone numbers to numbers.txt (one per line)
3. Write your message in comment.txt
4. Get your API key from wasenderapi.com
5. Add the API key to .env
6. Run the script — it sends to every number automatically
```

---

## Setup

```bash
git clone https://github.com/Yahks/whatsapp_mass_dm
cd whatsapp_mass_dm
pip install -r requirements.txt
```

Create a `.env` file:
```
API_KEY=your_wasenderapi_key_here
```

Add numbers to `numbers.txt`:
```
2348012345678
2348087654321
2341234567890
```

Write your message in `comment.txt`, then run:
```bash
python main.py
```

---

## Requirements

- Python 3.x
- WaSender API key — get one at [wasenderapi.com](https://www.wasenderapi.com)
- Active WhatsApp number connected to WaSender

---

## Built With

Python · WaSender API · WhatsApp Web (unofficial)

---

## Disclaimer

For educational and marketing purposes only.
Use responsibly — mass messaging may trigger WhatsApp's spam detection.
