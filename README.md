# 🧬 Ap.S.S. (Apoptotic Security System) v17.0

> **A Biologically-Inspired Cryptographic Vault with Autonomous Self-Destruction.**
<img width="1165" height="900" alt="apss" src="https://github.com/user-attachments/assets/9789cf0c-6628-4a3d-a393-48d6c9584e81" />

Ap.S.S. is an experimental security enclave that treats data protection as a biological survival challenge. Unlike passive encryption tools, Ap.S.S. possesses a digital "metabolism" and an aggressive immune system designed to terminate the organism (and the data) before a breach occurs.

---

## ☣️ The Philosophy: "Security Through Death"

Most vaults are prey—they sit and wait to be cracked. **Ap.S.S.** is an apex predator. It uses a combination of neural entropy and cryptographic ratcheting to ensure that data doesn't just stay encrypted—it evolves.

### Key Features:
* **Neural Entropy Engine:** Uses a Bi-cameral LSTM Neural Network to harvest hardware telemetry (CPU/RAM) as biometric salt for key derivation.
* **HKDF Ratchet (Forward Secrecy):** Implements a one-way Hash-based Key Derivation Function. As the organism "ages," old keys are biologically purged, making past sessions mathematically unrecoverable.
* **Double AEAD Wrapping:** Replaces vulnerable XOR operations with a double-layered ChaCha20-Poly1305 envelope. Both the key and the payload are protected by individual MAC tags.
* **Anti-DoS Proof-of-Work:** To prevent brute-force "denial-of-service" against the immune system, every decryption request requires the client to solve a CPU-intensive SHA-256 challenge.

---

## 🛡️ The Immune System (Escalating Defense)

Ap.S.S. monitors every interaction. If the cryptographic integrity (MAC Tag) is compromised, the "Immune Response" is triggered:

1. **Cryo-Sleep:** Exponential backoff ($2^n$ seconds) freezes the system to kill automated brute-force scripts.
2. **Honeytoken Deployment:** At threat level 3, the system generates a decoy payload to mislead the attacker.
3. **APOPTOSIS:** At threat level 5, the organism executes a **Total Cell Death** protocol. It shreds its neural weights with chaotic noise, deletes the DNA (`organism.json`), and locks the vault permanently.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* `torch`, `pycryptodome`, `psutil`

```bash
pip install torch pycryptodome psutil

Installation
Clone this repository to your local machine.

Ensure all dependencies are installed.

Run the Organism
Bash
python apss.py<img width="1165" height="900" alt="apss" src="https://github.com/user-attachments/assets/d5ae9c1b-87e5-499b-ada3-4906e3f4dc02" />

⚠️ Security Disclaimer
EXPERIMENTAL SOFTWARE. This project is a cryptographic Proof-of-Concept. While it uses industry-standard primitives (ChaCha20, HKDF, SHA-256), the overall architecture is experimental. Do not use this for securing high-value assets, life savings, or production environments.
