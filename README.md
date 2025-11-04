---

## 🔐 Cybersecurity Project — Secret Sharing (Shamir-Style)
### 🧩 Overview
This project demonstrates a **threshold-based secret sharing scheme** inspired by *Shamir’s Secret Sharing*. It securely splits a secret into multiple parts (shares) so that **any _t_ of _n_ shares** can reconstruct the original secret — but fewer than _t_ reveal nothing.  
> 💡 **Goal:** Showcase secure key management principles for cryptographic research and education.

---

### ⚙️ Features
- 🔢 Split secrets into `n` shares with a chosen threshold `t`.  
- 🧮 Reconstruct the secret using **Lagrange interpolation**.  
- 🧰 Pure Python — no external libraries required.  
- 🧑‍💻 Clear, commented, and safe for educational demonstration.  
- 📁 Outputs example shares to a local folder (`shares/`).

---

### 🧠 Conceptual Flow
1. Represent the secret as a number.  
2. Randomly generate a polynomial of degree `t-1` with the secret as its constant term.  
3. Evaluate the polynomial at distinct `x` values to produce the shares.  
4. Use Lagrange interpolation to reconstruct the polynomial’s constant term (the secret).  

---

### 🧰 Repository Structure
secret_sharing_project/
├── secret_sharing.py # Main implementation
├── README.md # Documentation and usage
├── shares/ # Example generated shares (safe)
└── report.pdf # Coursework write-up
