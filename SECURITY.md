# Security Policy

## Reporting Security Vulnerabilities

**Do not open public GitHub issues for security vulnerabilities.**

If you discover a security vulnerability, please email:

📧 **security@telegram-listener.dev** (or contact: irvaniali79@gmail.com)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Response Timeline

- **Initial Response**: Within 24 hours
- **Investigation**: 2-3 days
- **Patch Release**: Within 7 days (critical) or next regular release (non-critical)
- **Public Disclosure**: After patch is available

## Security Considerations

### IPC Communication

✅ **What we do:**
- Localhost-only communication (127.0.0.1)
- JSON message validation
- Connection limiting
- Thread-safe operations

⚠️ **What you should do:**
- Never expose IPC ports to the network
- Use firewalls to restrict localhost access
- Run on trusted machines only
- Keep Telegram Desktop updated
- Monitor logs for suspicious activity

### Chat Access

✅ **What's protected:**
- Only chats accessible in current Telegram Desktop session
- User's Telegram account authentication
- End-to-end encrypted chats (if enabled)

❌ **What's not protected:**
- Messages are logged in plaintext to callback functions
- Python scripts have full access to event data
- No encryption for IPC messages

### Recommended Practices

1. **Run in Isolated Environment**
   ```bash
   # Use containers
   docker run --network host telegram-listener
   
   # Or VM for critical applications
   ```

2. **Minimal Permissions**
   - Run Python scripts as unprivileged user
   - Restrict file access permissions
   - Use separate accounts for different listeners

3. **Logging and Monitoring**
   ```python
   import logging
   logging.basicConfig(filename='listener.log', level=logging.INFO)
   ```

4. **Input Validation**
   ```python
   @listener.on_message
   def handle_msg(event):
       # Validate message content
       if validate_message(event.text):
           process_message(event)
   ```

5. **Error Handling**
   ```python
   @listener.on_message
   def handle_msg(event):
       try:
           # Process message
           pass
       except Exception as e:
           logger.error(f"Error: {e}", exc_info=True)
   ```

## Known Limitations

### Current

1. **No Authentication**: IPC assumes trusted localhost
2. **Plaintext Logging**: Messages logged to Python callbacks unencrypted
3. **No Rate Limiting**: High-volume chats can overwhelm listeners
4. **Single Process**: Cannot scale to multiple Python processes per chat

### Mitigations

1. Use firewall rules
2. Sanitize logged data
3. Implement application-level rate limiting
4. Use message queues for high volume

## Future Security Improvements

- [ ] Message authentication (HMAC)
- [ ] TLS for IPC (if network access needed)
- [ ] Rate limiting per callback
- [ ] Permission system for chats
- [ ] Audit logging
- [ ] Message encryption at rest

## Dependencies

We monitor dependencies for security issues:

```bash
# Check for vulnerable dependencies
pip check

# Generate requirements with hashes
pip freeze > requirements.txt
```

## Supported Versions

Security patches are applied to:

| Version | Status | Until |
|---------|--------|-------|
| 0.2.x   | Active | Latest release + 12 months |
| 0.1.x   | EOL    | 2024-12-31 |

Older versions do not receive security updates.

## Security Checklist for Users

- [ ] Running on trusted machine
- [ ] Telegram Desktop fully updated
- [ ] Python listeners enabled in settings
- [ ] Firewall blocks external IPC access
- [ ] Python script runs as limited user
- [ ] Secrets not in code (use environment variables)
- [ ] Error logs don't expose sensitive data
- [ ] Regular backups of listener configuration

## Compliance

- **GDPR**: Messages from EU users are handled according to GDPR
- **Data Retention**: You control data retention in callbacks
- **Third Parties**: No data is sent to third parties
- **License**: See LICENSE for terms

## Questions?

For security questions (non-vulnerability):
- Open a GitHub discussion
- Email: irvaniali79@gmail.com

For vulnerability reports:
- Email only: (See top of this policy)

---

**Last Updated**: 2024
**Version**: 1.0
