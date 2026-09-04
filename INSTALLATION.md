# Installation and Setup Guide

## System Requirements

- **Python**: 3.8 or higher
- **Telegram Desktop**: Latest version with Python listener support enabled
- **Operating System**: Windows, macOS, or Linux
- **Network**: Access to localhost (127.0.0.1)

## Step-by-Step Installation

### 1. Install Python Package

#### Option A: From PyPI (Recommended)

```bash
pip install telegram-listener
```

#### Option B: From Source

```bash
# Clone repository
git clone https://github.com/irvaniali79/telegram-listener-py.git
cd telegram-listener-py

# Install in development mode
pip install -e .
```

### 2. Configure Telegram Desktop

You need to build Telegram Desktop with Python listener support.

#### Build from Source (Advanced)

1. Clone Telegram Desktop repository:
   ```bash
   git clone https://github.com/telegramdesktop/tdesktop.git
   cd tdesktop
   ```

2. Apply Python listener patches (see DESIGN.md for C++ implementation)

3. Build according to platform:
   - **Windows**: See `docs/building-win.md`
   - **macOS**: See `docs/building-mac.md`
   - **Linux**: See `docs/building-linux.md`

4. Enable Python listeners in Telegram Desktop settings:
   - Settings → Advanced → Enable Python Event Listeners (checkbox)

### 3. Verify Installation

```bash
# Test imports
python -c "from telegram_listener import ChatListener; print('✓ Installation successful')"

# Run example
python -m examples.basic_listener
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'telegram_listener'"

**Solution**: Reinstall the package
```bash
pip install --force-reinstall telegram-listener
```

### "ConnectionError: Failed to connect to Telegram Desktop"

**Causes**:
- Telegram Desktop is not running
- Python listener feature not enabled
- Incorrect IPC port

**Solutions**:
1. Ensure Telegram Desktop is running
2. Check Settings → Advanced → Python Event Listeners is enabled
3. Try restarting Telegram Desktop
4. Check firewall settings

### "RegistrationError: Registration failed"

**Causes**:
- Chat ID doesn't exist or not accessible
- Insufficient permissions
- Chat archived or deleted

**Solutions**:
1. Verify chat_id is correct
2. Ensure you're logged into Telegram Desktop
3. Try accessing the chat manually in Telegram Desktop
4. Check that Python listeners are allowed for this chat type

### No Events Received

**Causes**:
- Listener not properly registered
- Chat ID mismatch
- Callback not decorated properly
- Telegram Desktop restarted

**Solutions**:
1. Enable logging: `logging.basicConfig(level=logging.DEBUG)`
2. Verify chat_id matches the open chat
3. Test by sending a message in the monitored chat
4. Restart both Telegram Desktop and Python script
5. Check network connectivity to localhost

## Virtual Environment Setup

### Using venv (Built-in)

```bash
# Create virtual environment
python -m venv telegram_listener_env

# Activate
# On Linux/macOS:
source telegram_listener_env/bin/activate
# On Windows:
telegrasponsiveam_listener_env\Scripts\activate

# Install package
pip install telegram-listener

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create environment
conda create -n telegram_listener python=3.10

# Activate
conda activate telegram_listener

# Install package
pip install telegram-listener

# Deactivate when done
conda deactivate
```

## Docker Setup (Optional)

For isolated environment:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install telegram-listener
RUN pip install telegram-listener

# Your script
COPY my_listener.py .

CMD ["python", "my_listener.py"]
```

Build and run:
```bash
docker build -t telegram-listener .
docker run --network host telegram-listener
```

## Next Steps

1. **Read Quick Start**: See README.md for basic usage
2. **Explore Examples**: Check `examples/` directory
3. **API Reference**: Review `DESIGN.md` for architecture
4. **Contributing**: See `CONTRIBUTING.md` to contribute

## Getting Help

- 📖 [Documentation](https://github.com/irvaniali79/telegram-listener-py/wiki)
- 🐛 [Report Issues](https://github.com/irvaniali79/telegram-listener-py/issues)
- 💬 [Discussions](https://github.com/irvaniali79/telegram-listener-py/discussions)
- 📧 Email: irvaniali79@gmail.com

## Platform-Specific Notes

### Windows

- Uses named pipes for IPC
- Requires Visual Studio Build Tools for building Telegram Desktop
- Python 3.8+ available from Microsoft Store or python.org

### macOS

- Uses Unix sockets for IPC
- Requires Xcode Command Line Tools: `xcode-select --install`
- Supports both Intel and Apple Silicon

### Linux

- Uses Unix sockets for IPC
- Install dev packages: `sudo apt-get install python3-dev`
- Telegram Desktop available via Snap, Flatpak, or source

## Upgrading

```bash
# Upgrade to latest version
pip install --upgrade telegram-listener

# Upgrade to specific version
pip install telegram-listener==0.2.0

# Show installed version
pip show telegram-listener
```

## Uninstalling

```bash
# Remove package
pip uninstall telegram-listener

# Remove with dependencies
pip uninstall telegram-listener -y
```

## Development Installation

For contributing to the project:

```bash
# Clone repository
git clone https://github.com/irvaniali79/telegram-listener-py.git
cd telegram-listener-py

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode with dev tools
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Check code style
black telegram_listener/ --check
flake8 telegram_listener/
mypy telegram_listener/
```

## License

MIT License - See LICENSE file for details
