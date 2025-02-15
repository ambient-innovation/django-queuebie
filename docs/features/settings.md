# Settings

## QUEUEBIE_STRICT_MODE

Queuebie enforces by default that commands are not used outside its domain (aka Django app). If you want to skip that
restriction for whatever reason, you can do so.

```python
QUEUEBIE_STRICT_MODE = False
```
