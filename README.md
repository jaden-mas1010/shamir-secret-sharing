# 🔐 Shamir’s Secret Sharing System (SSS)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Security](https://img.shields.io/badge/Focus-Cryptography%20%26%20Key%20Management-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

## 🧠 Overview

This project demonstrates an implementation of **Shamir’s Secret Sharing Scheme (SSS)** — a cryptographic algorithm designed to **split a secret (such as a password, key, or message)** into multiple parts (called *shares*).  
A subset of these shares (meeting a defined **threshold**) can later be combined to reconstruct the original secret.  

> 💡 This system enhances secure key management by ensuring that no single entity can access the secret independently.

---

## ⚙️ Features

✅ Self-contained Python implementation — no external dependencies  
✅ Supports any custom secret (text or key)  
✅ Adjustable threshold *(t)* and total shares *(n)*  
✅ Uses modular arithmetic and polynomial interpolation  
✅ Reconstructs secret from any valid subset of shares  
✅ File-based share storage system  

---

## 🧩 How It Works

1. The **secret** is converted into an integer.
2. A random polynomial of degree *(t–1)* is generated, where the constant term represents the secret.
3. Multiple **shares** are computed using that polynomial at unique x-values.
4. Any **t or more shares** can reconstruct the original secret using **Lagrange interpolation**.

---

## 🚀 Getting Started

### 🧰 Requirements
- Python **3.9+**
- Works cross-platform (Windows, macOS, Linux)

---

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/jaden-mas1010/shamir-secret-sharing.git

# Navigate to the folder
cd shamir-secret-sharing

# Run the program
python keysplit.py

