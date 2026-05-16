"""Minimal shim for pydantic_settings used only in test runs.
Provides BaseSettings which reads environment variables via os.environ and sets attributes.
This is intentionally minimal and only for tests where full pydantic_settings is unavailable.
"""
import os
from typing import Any


class BaseSettings:
    def __init__(self, **overrides: Any):
        # For each annotated attribute in subclass, try to take from env or default
        for k, v in self.__class__.__dict__.items():
            if k.startswith('__'):
                continue
            if callable(v):
                continue
            # try to get from env
            env_key = k.upper()
            if env_key in os.environ:
                setattr(self, k, os.environ[env_key])
            else:
                # fallback to the default defined on the class if present
                if hasattr(self.__class__, k):
                    setattr(self, k, getattr(self.__class__, k))
        # apply overrides
        for k, v in overrides.items():
            setattr(self, k, v)
