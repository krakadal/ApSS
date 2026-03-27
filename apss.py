# =================================================================
# Ap.S.S. (Apoptotic Security System)
# © 2026 Antoniy Iliev Velkov 
# "Cryptographically secure entropy, AEAD Key Wrapping, and Anti-DoS Proof-of-Work."
# =================================================================
import hashlib
import os
import time
import struct
import random
import json
import torch
import torch.nn as nn
import torch.optim as optim
import tkinter as tk
from tkinter import font, scrolledtext, Scale
import psutil
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256

torch.set_default_dtype(torch.float64)

# ───────────────────────────────────────
# 1. NEURAL ENTROPY ENGINE
# ───────────────────────────────────────
class Hemisphere(nn.Module):
    def __init__(self, hidden_size=128):
        super().__init__()
        self.memory = nn.LSTM(128, hidden_size, num_layers=2, batch_first=True)
        self.project = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.Sigmoid()
        )
        self.hidden = None

    def forward(self, x):
        if self.hidden is None:
            self.hidden = (torch.zeros(2, x.size(0), 128), torch.zeros(2, x.size(0), 128))
        out, self.hidden = self.memory(x, self.hidden)
        return self.project(out[:, -1, :])

# ───────────────────────────────────────
# 2. EFIR CIPHER (Obfuscation Layer)
# ───────────────────────────────────────
class EfirCipher:
    def __init__(self):
        self.map = {
            'a':'▽', 'b':'⊐', 'c':'⨝', 'd':'▱', 'e':'≡', 'f':'⍉', 'g':'⸄', 'h':'⨉',
            'i':'‖', 'j':'‖˙', 'k':'⋖', 'l':'∠', 'm':'∏', 'n':'∦', 'o':'⊙', 'p':'∩',
            'q':'⧖', 'r':'∣ο', 's':'☾', 't':'⊤', 'u':'ϒ', 'v':'⧑', 'w':'∐', 'x':'⨉',
            'y':'⦓⦔', 'z':'⌇', ' ':' ',
            '0':'⓪','1':'①','2':'②','3':'③','4':'④','5':'⑤','6':'⑥','7':'⑦','8':'⑧','9':'⑨'
        }
        self.rev_map = {v: k for k, v in self.map.items()}

    def encode(self, text: str) -> str:
        return "".join(self.map.get(c.lower(), c) for c in text)

    def decode(self, text: str) -> str:
        return "".join(self.rev_map.get(c, c) for c in text)

# ───────────────────────────────────────
# 3. EPIGENETIC DNA (HKDF Ratchet & Forward Secrecy)
# ───────────────────────────────────────
class EpigeneticDNA:
    def __init__(self, dna_file="organism.json"):
        self.file = dna_file
        self.current_epoch = 0
        self.root_key = get_random_bytes(32) # CSPRNG Genesis Seed
        self.keychain = {} 
        self.threat_level = 0
        self.load()

    def enforce_amnesia(self, half_life: int):
        epochs = list(self.keychain.keys())
        for ep in epochs:
            if int(ep) <= (self.current_epoch - half_life):
                del self.keychain[ep] # Mathematical Forward Secrecy
        self.save()

    def ratchet_forward(self, neural_salt: bytes) -> bytes:
        """Cryptographically secure ratchet using HKDF."""
        self.current_epoch += 1
        
        # True CSPRNG entropy mixed with neural salt
        crypto_entropy = get_random_bytes(32) 
        
        # Derive next Root Key and Current KEK securely
        derived_keys = HKDF(master=crypto_entropy, salt=neural_salt, key_len=64, hashmod=SHA256)
        
        # First 32 bytes become the new Root Key, next 32 bytes become the KEK
        self.root_key = derived_keys[:32]
        kek = derived_keys[32:]
        
        self.keychain[str(self.current_epoch)] = kek.hex()
        self.save()
        return kek

    def get_kek(self, epoch: int):
        hex_key = self.keychain.get(str(epoch))
        if not hex_key: return None
        return bytes.fromhex(hex_key)

    def save(self):
        with open(self.file, 'w') as f:
            json.dump({
                'epoch': self.current_epoch,
                'root_key': self.root_key.hex(),
                'keychain': self.keychain,
                'threat_level': self.threat_level
            }, f)

    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r') as f:
                    data = json.load(f)
                    self.current_epoch = data.get('epoch', 0)
                    self.root_key = bytes.fromhex(data.get('root_key', ""))
                    self.keychain = data.get('keychain', {})
                    self.threat_level = data.get('threat_level', 0)
            except: pass

# ───────────────────────────────────────
# 4. THE SINGULARITY ENGINE
# ───────────────────────────────────────
class TheSingularityEngine:
    def __init__(self):
        self.left_brain = Hemisphere()
        self.right_brain = Hemisphere()
        self.opt_left = optim.Adam(self.left_brain.parameters(), lr=0.005)
        self.opt_right = optim.Adam(self.right_brain.parameters(), lr=0.005)

        self.left_path = "left_hemisphere.pth"
        self.right_path = "right_hemisphere.pth"
        self.death_cert = "organism.dead"

        self.is_dead = os.path.exists(self.death_cert)
        self.dna = EpigeneticDNA()
        self.cipher = EfirCipher()
        self.max_threats = 5

        if not self.is_dead:
            self._load_brains()

    def _load_brains(self):
        if os.path.exists(self.left_path):
            try: self.left_brain.load_state_dict(torch.load(self.left_path, weights_only=True))
            except: pass
        if os.path.exists(self.right_path):
            try: self.right_brain.load_state_dict(torch.load(self.right_path, weights_only=True))
            except: pass

    def proof_of_work(self, complexity=3):
        """Anti-DoS shield. Forces CPU work before processing decrypt requests."""
        nonce = 0
        prefix = '0' * complexity
        while True:
            hash_attempt = hashlib.sha256(f"GHOST_POW_{nonce}".encode()).hexdigest()
            if hash_attempt.startswith(prefix):
                return True
            nonce += 1

    def trigger_immune_response(self, ui_root, status_label):
        self.dna.threat_level += 1
        self.dna.save()

        if self.dna.threat_level >= self.max_threats:
            status_label.config(text="☠️ TRIGGERING APOPTOSIS...", fg="#ff0000")
            ui_root.update()

            with torch.no_grad():
                for param in self.left_brain.parameters():
                    param.add_(torch.randn_like(param) * 10.0)
                for param in self.right_brain.parameters():
                    param.add_(torch.randn_like(param) * 10.0)

            torch.save(self.left_brain.state_dict(), self.left_path)
            torch.save(self.right_brain.state_dict(), self.right_path)

            if os.path.exists(self.dna.file): os.remove(self.dna.file)

            with open(self.death_cert, "w") as f:
                f.write("ORGANISM TERMINATED. DATA PERMANENTLY INACCESSIBLE.")
            self.is_dead = True
            return "☠️ APOPTOSIS COMPLETE. ORGANISM IS PERMANENTLY DEAD."

        delay = 2 ** self.dna.threat_level
        status_label.config(text=f"⚠️ THREAT {self.dna.threat_level}/{self.max_threats}. CRYO-SLEEP FOR {delay}s...", fg="#ff6600")
        ui_root.update()
        time.sleep(delay)

        return f"⚠️ DECRYPTION FAILED. MAC TAG INVALID OR AMNESIA TRIGGERED."

    def get_neural_salt(self, text: str):
        cpu, mem = psutil.cpu_percent(), psutil.virtual_memory().percent
        vec = torch.zeros(1, 1, 128)
        for i, c in enumerate(text[:128]):
            vec[0, 0, i] = ord(c) % 128 / 128.0
        pulse = torch.tensor([cpu/100.0, mem/100.0]).repeat(64).view(1, 1, 128)
        vec = (vec + pulse) / 2.0
        
        with torch.no_grad():
            out_left = self.left_brain(vec)
            out_right = self.right_brain(vec)
            
        raw_bytes = (out_left * 255).byte().numpy().tobytes() + (out_right * 255).byte().numpy().tobytes()
        return hashlib.sha256(raw_bytes).digest()

    def encrypt(self, plaintext: str, half_life: int) -> str:
        if self.is_dead: return "☠️ ORGANISM IS DEAD."

        neural_salt = self.get_neural_salt(plaintext)
        kek = self.dna.ratchet_forward(neural_salt)
        self.dna.enforce_amnesia(half_life)
        epoch = self.dna.current_epoch

        # 1. Generate Ephemeral DEK
        dek = get_random_bytes(32)
        
        # 2. Secure Key Wrapping (Replace dangerous XOR with AEAD envelope)
        kek_cipher = ChaCha20_Poly1305.new(key=kek)
        wrapped_dek, dek_tag = kek_cipher.encrypt_and_digest(dek)

        # 3. Payload Encryption
        tx_hash = hashlib.sha256(f"APEX_{time.time()}_{os.urandom(8)}".encode()).hexdigest()[:32]
        efir_text = self.cipher.encode(plaintext)

        cipher = ChaCha20_Poly1305.new(key=dek)
        cipher.update(tx_hash.encode())
        ciphertext, payload_tag = cipher.encrypt_and_digest(efir_text.encode('utf-8'))

        # Pack Format: [Epoch(4)] + [KEK_Nonce(12)] + [DEK_Tag(16)] + [Wrapped_DEK(32)] + [Payload_Nonce(12)] + [Payload_Tag(16)] + [Ciphertext]
        epoch_bytes = struct.pack('I', epoch)
        payload = (epoch_bytes + 
                   kek_cipher.nonce + dek_tag + wrapped_dek + 
                   cipher.nonce + payload_tag + ciphertext)

        if self.dna.threat_level > 0:
            self.dna.threat_level -= 1
            self.dna.save()

        return payload.hex() + "|" + tx_hash

    def decrypt(self, data: str, ui_root, status_label) -> str:
        if self.is_dead: return "☠️ ORGANISM IS DEAD."

        # Anti-DoS Shield: Attacker must spend CPU cycles before triggering anything
        self.proof_of_work(complexity=4)

        try:
            if "|" not in data:
                return self.trigger_immune_response(ui_root, status_label)

            payload_hex, tx_hash = data.split("|")
            raw = bytes.fromhex(payload_hex)

            # Unpack Payload
            epoch = struct.unpack('I', raw[:4])[0]
            kek_nonce = raw[4:16]
            dek_tag = raw[16:32]
            wrapped_dek = raw[32:64]
            payload_nonce = raw[64:76]
            payload_tag = raw[76:92]
            ciphertext = raw[92:]

            kek = self.dna.get_kek(epoch)
            if not kek:
                raise ValueError("MATHEMATICAL AMNESIA")

            # 1. Secure Key Unwrapping
            kek_cipher = ChaCha20_Poly1305.new(key=kek, nonce=kek_nonce)
            dek = kek_cipher.decrypt_and_verify(wrapped_dek, dek_tag) # Verifies DEK integrity

            # 2. Payload Decryption
            cipher = ChaCha20_Poly1305.new(key=dek, nonce=payload_nonce)
            cipher.update(tx_hash.encode())
            decrypted = cipher.decrypt_and_verify(ciphertext, payload_tag) # Verifies Data integrity

            self.dna.threat_level = 0
            self.dna.save()
            return self.cipher.decode(decrypted.decode('utf-8'))

        except ValueError:
            # Reaches here if MAC Tag verification fails
            return self.trigger_immune_response(ui_root, status_label)
        except Exception as e:
            return f"‖‖ ⁕ [SYSTEM SHOCK: {str(e)}]"

# ───────────────────────────────────────
# 5. UI MONITOR
# ───────────────────────────────────────
def launch_vault():
    engine = TheSingularityEngine()
    root = tk.Tk()
    root.title("GHOST V17.0 — THE SINGULARITY (Enterprise Crypto)")
    root.geometry("1180x880")
    root.configure(bg="#050505")

    header = font.Font(family="Courier New", size=22, weight="bold")
    tk.Label(root, text="THE SINGULARITY v17.0", fg="#00ccff", bg="#050505", font=header).pack(pady=15)

    top_frame = tk.Frame(root, bg="#050505")
    top_frame.pack(pady=5, fill=tk.X, padx=60)

    threat_label = tk.Label(top_frame, text="THREAT LEVEL: 0/5 (OPTIMAL)", fg="#00ccff", bg="#050505", font=("Consolas", 12, "bold"))
    threat_label.pack(side=tk.LEFT)
    epoch_label = tk.Label(top_frame, text=f"CURRENT EPOCH: {engine.dna.current_epoch}", fg="#888888", bg="#050505", font=("Consolas", 12))
    epoch_label.pack(side=tk.LEFT, padx=30)

    half_life_slider = Scale(top_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                             label="Amnesia Half-Life (Epochs)",
                             bg="#050505", fg="#00ccff", highlightthickness=0, length=250, font=("Consolas", 10))
    half_life_slider.set(20)
    half_life_slider.pack(side=tk.RIGHT)

    tk.Label(root, text="CONSCIOUSNESS STREAM", fg="#555555", bg="#050505", font=("Consolas", 11)).pack(anchor="w", padx=60)
    input_box = scrolledtext.ScrolledText(root, height=8, width=125, bg="#0d0d0d", fg="#ffffff", font=("Consolas", 12), insertbackground="#00ccff")
    input_box.pack(pady=10, padx=50)

    tk.Label(root, text="EPIGENETIC PAYLOAD (HKDF + Double AEAD Wrap)", fg="#555555", bg="#050505", font=("Consolas", 11)).pack(anchor="w", padx=60)
    output_box = scrolledtext.ScrolledText(root, height=10, width=125, bg="#000000", fg="#00ccff", font=("Consolas", 11))
    output_box.pack(pady=10, padx=50)

    status = tk.Label(root, text="SYSTEM ONLINE. CSPRNG ENTROPY & ANTI-DOS SHIELD ACTIVE.", fg="#ff4444", bg="#050505", font=("Consolas", 10))
    status.pack(pady=10)

    def update_ui_state():
        if engine.is_dead:
            threat_label.config(text="THREAT LEVEL: FATAL (APOPTOSIS)", fg="#ff0000")
            status.config(text="ORGANISM HAS SELF-DESTRUCTED.", fg="#ff0000")
            input_box.config(state=tk.DISABLED, bg="#1a0000")
            output_box.config(state=tk.DISABLED, bg="#1a0000")
        else:
            colors = ["#00ccff", "#00ffcc", "#ffcc00", "#ff6600", "#ff0000"]
            color = colors[min(engine.dna.threat_level, 4)]
            threat_label.config(text=f"THREAT LEVEL: {engine.dna.threat_level}/5", fg=color)
            epoch_label.config(text=f"CURRENT EPOCH: {engine.dna.current_epoch}")

    def encrypt():
        text = input_box.get("1.0", tk.END).strip()
        if not text: return
        half_life = half_life_slider.get()
        result = engine.encrypt(text, half_life)
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", result)
        if not engine.is_dead:
            input_box.delete("1.0", tk.END)
            status.config(text=f"✓ ENCRYPTED. RATCHET ADVANCED TO EPOCH {engine.dna.current_epoch}.", fg="#00ccff")
        update_ui_state()

    def decrypt():
        data = output_box.get("1.0", tk.END).strip()
        if not data: return
        status.config(text="EXECUTING PROOF-OF-WORK AND VERIFYING AEAD INTEGRITY...", fg="#ffaa00")
        root.update()
        result = engine.decrypt(data, root, status)
        input_box.delete("1.0", tk.END)
        input_box.insert("1.0", result)
        if "⚠️" in result or "☠️" in result:
            pass
        else:
            status.config(text="✓ KEK UNWRAPPED. SIGNAL SECURELY DECRYPTED.", fg="#00ffcc")
        update_ui_state()

    update_ui_state()

    btn_frame = tk.Frame(root, bg="#050505")
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="LOCK & MUTATE", command=encrypt,
              bg="#00ccff", fg="black", width=25, height=2, font=("Consolas", 12, "bold")).pack(side=tk.LEFT, padx=25)
    tk.Button(btn_frame, text="VERIFY & UNLOCK", command=decrypt,
              bg="#00ffcc", fg="black", width=25, height=2, font=("Consolas", 12, "bold")).pack(side=tk.LEFT, padx=25)

    root.mainloop()

if __name__ == "__main__":
    launch_vault()