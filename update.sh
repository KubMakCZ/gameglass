#!/bin/bash
# GameGlass Updater - Stáhne nejnovější verzi a restartuje aplikaci

echo "🔄 Zahajuji aktualizaci GameGlass..."

# 1. Stáhnutí posledních změn z repozitáře (předpokládáme větev main)
echo "📥 Stahuji novou verzi z GitHubu..."
git fetch origin
git reset --hard origin/main

# 2. Rebuildování a restart Docker kontejneru
# Využije docker-compose, který aplikaci automaticky znovu sestaví
echo "🏗️ Kompiluji a restartuji servery..."
docker compose up -d --build

# 3. Vyčištění nepotřebných a starých obrazů pro ušetření místa
echo "🧹 Mažu staré, nepotřebné Docker obrazy..."
docker image prune -f

echo "✅ Aktualizace úspěšně dokončena! Nový GameGlass právě běží."
