#!/bin/sh

echo "[+] running db_create.py"
python3 db_create.py
echo "[+] running db_populate.py"
python3 db_populate.py

exec "$@