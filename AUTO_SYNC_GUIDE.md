# 🤖 AEGIS Autonomous GitHub Sync

Complete guide to automatically sync your AEGIS project to GitHub while keeping secrets encrypted and secure.

---

## 🎯 Features

✅ **Automatic Git Commits & Pushes**
- Auto-commits changes every 5 minutes (configurable)
- Generates descriptive commit messages
- Pushes to GitHub automatically

✅ **Secret Encryption**
- Encrypts `.env` file before committing
- Uses strong AES-256 encryption
- Master password protected

✅ **Smart .gitignore**
- Prevents accidental secret commits
- Excludes logs, reports, temp files
- Allows encrypted secrets in git

✅ **Safe by Default**
- Secrets never committed in plaintext
- Encrypted files safe to share
- Easy decrypt for team members

---

## 🚀 Quick Start

### 1. Set Master Password

```bash
# Set your encryption password (KEEP THIS SAFE!)
export AEGIS_MASTER_PASSWORD="your-super-secure-password-here"

# Add to your ~/.bashrc or ~/.zshrc to persist:
echo 'export AEGIS_MASTER_PASSWORD="your-super-secure-password"' >> ~/.bashrc
```

### 2. Encrypt Your Secrets

```bash
# Encrypt .env file
python3 tools/secrets_manager.py encrypt-env

# This creates .env.encrypted (safe to commit to git)
```

### 3. Run Auto-Sync

```bash
# One-time sync
./tools/auto_sync.sh once

# Continuous sync (every 5 minutes)
./tools/auto_sync.sh continuous

# Or use the alias
./tools/auto_sync.sh watch
```

---

## 📖 Detailed Usage

### Secrets Manager

The `secrets_manager.py` tool handles encryption/decryption of sensitive files.

#### Encrypt .env File

```bash
python3 tools/secrets_manager.py encrypt-env
```

Output:
```
✓ Encrypted: .env → .env.encrypted
✓ .env encrypted successfully!
  You can now safely commit .env.encrypted to git
```

#### Decrypt .env File

```bash
python3 tools/secrets_manager.py decrypt-env
```

Output:
```
✓ Decrypted: .env.encrypted → .env
✓ .env decrypted successfully!
  Remember: .env is in .gitignore and won't be committed
```

#### Encrypt Any File

```bash
python3 tools/secrets_manager.py encrypt --file secrets.txt --output secrets.txt.encrypted
```

#### Decrypt Any File

```bash
python3 tools/secrets_manager.py decrypt --file secrets.txt.encrypted --output secrets.txt
```

---

### Auto-Sync Modes

#### Mode 1: One-Time Sync

Perfect for manual commits:

```bash
./tools/auto_sync.sh once
```

What it does:
1. Checks for changes
2. Encrypts `.env` → `.env.encrypted`
3. Commits all changes
4. Pushes to GitHub
5. Exits

#### Mode 2: Continuous Sync

Perfect for autonomous operation:

```bash
./tools/auto_sync.sh continuous
```

What it does:
1. Runs forever in the background
2. Checks for changes every 5 minutes
3. Auto-commits and pushes if changes detected
4. Press CTRL+C to stop

#### Mode 3: Custom Interval

```bash
# Sync every 10 minutes
SYNC_INTERVAL=600 ./tools/auto_sync.sh continuous

# Sync every 1 minute (for active development)
SYNC_INTERVAL=60 ./tools/auto_sync.sh continuous
```

---

## 🔒 Security Best Practices

### ✅ DO:

1. **Set Strong Master Password**
   ```bash
   # Use a strong, unique password
   export AEGIS_MASTER_PASSWORD="$(openssl rand -base64 32)"
   ```

2. **Store Password Securely**
   - Use a password manager
   - Don't commit the password to git
   - Share with team via secure channel (1Password, LastPass)

3. **Encrypt Before Committing**
   ```bash
   # Always run before manual commits
   python3 tools/secrets_manager.py encrypt-env
   git add .env.encrypted
   ```

4. **Verify .gitignore**
   ```bash
   # Make sure .env is excluded
   grep "^.env$" .gitignore
   ```

### ❌ DON'T:

1. **Never commit `.env` directly**
   ```bash
   # This is blocked by .gitignore, but double-check:
   git status | grep "\.env$"
   # Should show nothing
   ```

2. **Never share master password in plaintext**
   - Don't email it
   - Don't post in Slack
   - Don't commit to git

3. **Never skip encryption**
   ```bash
   # DON'T DO THIS:
   git add .env  # ❌ DANGEROUS!

   # DO THIS INSTEAD:
   python3 tools/secrets_manager.py encrypt-env
   git add .env.encrypted  # ✅ SAFE
   ```

---

## 🛠️ Advanced Configuration

### Environment Variables

```bash
# Master password for encryption/decryption
export AEGIS_MASTER_PASSWORD="your-password"

# Git branch to push to (default: main)
export GIT_BRANCH="develop"

# Sync interval in seconds (default: 300 = 5 minutes)
export SYNC_INTERVAL=600

# Git user (for commits)
export GIT_AUTHOR_NAME="AEGIS Bot"
export GIT_AUTHOR_EMAIL="aegis@zyberpol.io"
```

### Run as Background Service

#### Using nohup:

```bash
nohup ./tools/auto_sync.sh continuous > auto_sync.log 2>&1 &
echo $! > auto_sync.pid
```

Stop it:
```bash
kill $(cat auto_sync.pid)
```

#### Using screen:

```bash
screen -S aegis-sync
./tools/auto_sync.sh continuous
# Press CTRL+A then D to detach
```

Reattach:
```bash
screen -r aegis-sync
```

---

## 👥 Team Collaboration

### For New Team Members

1. **Clone the repository**
   ```bash
   git clone https://github.com/taazbro/dayton_AEGIS.git
   cd dayton_AEGIS
   ```

2. **Get master password from team**
   - Ask team lead for `AEGIS_MASTER_PASSWORD`
   - Store in password manager

3. **Decrypt secrets**
   ```bash
   export AEGIS_MASTER_PASSWORD="password-from-team"
   python3 tools/secrets_manager.py decrypt-env
   ```

4. **Start development**
   ```bash
   source venv/bin/activate
   python main.py
   ```

### For Team Lead

1. **Share password securely**
   - Use 1Password shared vault
   - Or use encrypted messaging (Signal, Wire)

2. **Rotate password if needed**
   ```bash
   # 1. Decrypt with old password
   AEGIS_MASTER_PASSWORD="old-password" python3 tools/secrets_manager.py decrypt-env

   # 2. Re-encrypt with new password
   AEGIS_MASTER_PASSWORD="new-password" python3 tools/secrets_manager.py encrypt-env

   # 3. Commit new encrypted file
   git add .env.encrypted
   git commit -m "🔒 Rotated encryption password"
   git push
   ```

---

## 🔍 Troubleshooting

### "Decryption failed. Wrong password?"

**Solution:** Check your master password

```bash
# Verify password is set
echo $AEGIS_MASTER_PASSWORD

# Try decrypting with explicit password
python3 tools/secrets_manager.py decrypt-env --password "your-password"
```

### ".env file not found"

**Solution:** Decrypt the encrypted version

```bash
python3 tools/secrets_manager.py decrypt-env
```

### "Push failed"

**Solution:** Check git credentials

```bash
# Configure git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Check remote
git remote -v

# Try manual push
git push origin main
```

### Auto-sync not running

**Solution:** Check permissions and background processes

```bash
# Make executable
chmod +x tools/auto_sync.sh

# Check if already running
ps aux | grep auto_sync

# Check logs
tail -f auto_sync.log
```

---

## 📋 File Reference

### Files That Are Encrypted

✅ Safe to commit after encryption:
- `.env.encrypted` - Encrypted environment variables
- `*.encrypted` - Any encrypted file

### Files That Are NEVER Committed

❌ Blocked by .gitignore:
- `.env` - Environment variables (PLAINTEXT!)
- `*.key`, `*.pem` - Private keys
- `secrets/` - Secrets directory
- `logs/` - Log files
- `reports/` - Report files
- `venv/` - Virtual environment

### Files That Are Always Committed

✅ Safe to commit:
- `*.py` - Python source code
- `requirements.txt` - Dependencies
- `README.md` - Documentation
- `.gitignore` - Git exclusions
- `tools/` - Automation scripts

---

## 🎉 Summary

**Setup (one-time):**
```bash
# 1. Set master password
export AEGIS_MASTER_PASSWORD="your-secure-password"

# 2. Encrypt secrets
python3 tools/secrets_manager.py encrypt-env

# 3. Start auto-sync
./tools/auto_sync.sh continuous
```

**Daily workflow:**
```bash
# Just code normally!
# Auto-sync handles everything:
# - Encrypts secrets automatically
# - Commits changes every 5 minutes
# - Pushes to GitHub
# - You stay focused on coding! 🚀
```

**Your secrets are safe, your code is synced, and you're free to build! 🔥**
