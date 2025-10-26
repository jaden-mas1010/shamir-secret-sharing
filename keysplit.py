# ...existing code...
import builtins
if not hasattr(builtins, 'long'):
    builtins.long = int

# If secretsharing package exists, don't import it here anymore — this script is self-contained.
import os
import secrets
import argparse
from typing import List, Tuple

share_dir = 'shares'
os.makedirs(share_dir, exist_ok=True)

def eval_poly(coeffs, x, p):
    res = 0
    for a in reversed(coeffs):
        res = (res * x + a) % p
    return res

def lagrange_zero(points, p):
    total = 0
    for i, (xi, yi) in enumerate(points):
        num = 1
        den = 1
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            num = (num * (-xj)) % p
            den = (den * (xi - xj)) % p
        total = (total + yi * num * pow(den, -1, p)) % p
    return total

def secret_to_int(s: str) -> int:
    return int.from_bytes(s.encode('utf-8'), 'big')

def int_to_secret(i: int) -> str:
    if i == 0:
        return ''
    b = i.to_bytes((i.bit_length() + 7)//8, 'big')
    return b.decode('utf-8', errors='replace')

def next_prime(n: int) -> int:
    if n <= 2:
        return 2
    cand = n | 1
    def is_probable_prime(x):
        if x % 2 == 0:
            return x == 2
        for a in (2,3,5,7,11):
            if a >= x:
                break
            if pow(a, x-1, x) != 1:
                return False
        return True
    while not is_probable_prime(cand):
        cand += 2
    return cand

def split_secret(threshold: int, secret: str, total: int):
    if not (1 < threshold <= total):
        print("Require 1 < threshold <= total")
        return
    s_int = secret_to_int(secret)
    p = next_prime(s_int + 1)
    coeffs = [s_int] + [secrets.randbelow(p) for _ in range(threshold - 1)]
    for x in range(1, total+1):
        y = eval_poly(coeffs, x, p)
        path = os.path.join(share_dir, f"share_{x}.txt")
        with open(path, "w") as f:
            # keep x in file for clarity but reconstruction can use number input
            f.write(f"{x} {y} {p}")
    print(f"Saved {total} shares in '{share_dir}' (threshold {threshold}).")

def reconstruct_from_files(paths: List[str]):
    points = []
    p = None
    for path in paths:
        try:
            with open(path, "r") as f:
                parts = f.read().strip().split()
        except FileNotFoundError:
            print("File not found:", path); return
        if len(parts) < 3:
            print("Bad share format:", path); return
        x, y, pp = map(int, parts[:3])
        if p is None:
            p = pp
        elif p != pp:
            print("Mismatched primes in shares"); return
        points.append((x, y))
    if len(points) == 0:
        print("No shares provided"); return
    secret_int = lagrange_zero(points, p)
    print("Reconstructed secret:", int_to_secret(secret_int))

def reconstruct_from_indices(indices: List[int]):
    # read share files by small numeric keys (e.g. 1 2 3)
    paths = []
    for i in indices:
        if i <= 0:
            print("Share numbers must be positive:", i); return
        paths.append(os.path.join(share_dir, f"share_{i}.txt"))
    reconstruct_from_files(paths)

def interactive():
    while True:
        print("\n1) Split secret   2) Reconstruct by share numbers   q) Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            s = input("Enter secret: ").rstrip("\n")
            if not s:
                print("Empty secret"); continue
            try:
                t = int(input("Threshold [2]: ").strip() or "2")
                n = int(input("Total shares [3]: ").strip() or "3")
            except ValueError:
                print("Threshold and total must be integers"); continue
            split_secret(t, s, n)
        elif choice == "2":
            # ask for small numeric keys instead of file paths
            print("Enter share numbers separated by spaces (e.g. 1 2):")
            line = input("Shares: ").strip()
            if not line:
                print("No shares entered"); continue
            try:
                indices = [int(x) for x in line.split()]
            except ValueError:
                print("Enter numbers only"); continue
            reconstruct_from_indices(indices)
        elif choice.lower() in ("q", "quit"):
            break
        else:
            print("Unknown option")

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("cmd", nargs="?", help="'split' or 'recon' (optional)")
parser.add_argument("args", nargs="*", help="arguments for the command")
ns = parser.parse_args()

if ns.cmd is None:
    interactive()
elif ns.cmd == "split":
    # usage: python keysplit.py split "secret" threshold total
    if len(ns.args) < 3:
        print("Usage: split \"secret\" threshold total")
    else:
        split_secret(int(ns.args[1]), ns.args[0], int(ns.args[2]))
elif ns.cmd == "recon":
    # if all args are digits, treat them as share numbers
    if not ns.args:
        print("Usage: recon share1 share2 ...  (you can pass numbers or file paths)")
    else:
        if all(a.isdigit() for a in ns.args):
            indices = [int(a) for a in ns.args]
            reconstruct_from_indices(indices)
        else:
            reconstruct_from_files(ns.args)
else:
    print("Unknown command")
# ...existing code...