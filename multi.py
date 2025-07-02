import json, base64, time, asyncio, aiohttp
from nacl.signing import SigningKey

RPC = 'https://octra.network'
μ = 1_000_000
AMOUNT = 1.0  # dalam OCT
RECIPIENT_FILE = "p.txt"
WALLET_FILE = "wallets.txt"
DELAY = 30  # detik antar TX

def build_tx(sender, priv_b64, amount, nonce, to_):
    sk = SigningKey(base64.b64decode(priv_b64))
    pub = base64.b64encode(sk.verify_key.encode()).decode()
    tx = {
        "from": sender,
        "to_": to_,
        "amount": str(int(amount * μ)),
        "nonce": nonce,
        "ou": "1" if amount < 1000 else "3",
        "timestamp": time.time()
    }
    bl = json.dumps(tx, separators=(",", ":"))
    sig = base64.b64encode(sk.sign(bl.encode()).signature).decode()
    tx.update(signature=sig, public_key=pub)
    return tx

async def fetch_nonce(session, addr):
    url = f"{RPC}/balance/{addr}"
    try:
        async with session.get(url) as resp:
            text = await resp.text()
            data = json.loads(text)
            return int(data['nonce'])
    except Exception as e:
        print(f"[ERROR] Gagal ambil nonce: {e}")
        return None

async def send_tx(session, tx):
    try:
        async with session.post(f"{RPC}/send-tx", json=tx) as resp:
            text = await resp.text()
            try:
                return json.loads(text)
            except:
                print(f"[ERROR] Respon bukan JSON: {text}")
                return None
    except Exception as e:
        print(f"[ERROR] Gagal kirim TX: {e}")
        return None

async def main():
    # Baca penerima
    try:
        with open(RECIPIENT_FILE) as f:
            recipients = [line.strip() for line in f if line.strip().startswith("oct")]
    except Exception as e:
        print(f"❌ Gagal baca p.txt: {e}")
        return

    if not recipients:
        print("❌ Tidak ada address valid di p.txt")
        return

    # Baca wallet sender
    try:
        with open(WALLET_FILE) as f:
            senders = [line.strip().split("|||") for line in f if "|||" in line]
    except Exception as e:
        print(f"❌ Gagal baca wallets.txt: {e}")
        return

    if not senders:
        print("❌ Tidak ada wallet valid di wallets.txt")
        return

    async with aiohttp.ClientSession() as session:
        for sender_addr, priv_b64 in senders:
            print(f"\n===== MENGIRIM DARI WALLET: {sender_addr} =====")

            nonce_awal = await fetch_nonce(session, sender_addr)
            if nonce_awal is None:
                print(f"[SKIP] Gagal ambil nonce untuk {sender_addr}")
                continue

            current_nonce = nonce_awal

            for to_addr in recipients:
                while True:
                    print(f"[INFO] Coba nonce {current_nonce} → TX ke {to_addr}")
                    tx = build_tx(sender_addr, priv_b64, AMOUNT, current_nonce, to_addr)
                    res = await send_tx(session, tx)

                    if res and res.get("status") == "accepted":
                        print(f"[✓] {sender_addr} → {to_addr} | {AMOUNT} OCT (nonce={current_nonce})")
                        current_nonce += 1
                        await asyncio.sleep(DELAY)
                        break
                    else:
                        print(f"[✗] TX gagal dengan nonce {current_nonce}: {res}")
                        current_nonce += 1
                        await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⛔️ Dibatalkan.")
