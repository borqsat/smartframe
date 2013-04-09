#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["v0"]


def __load_api_v0():
    from .v0.groupapis import appweb
    from .v0.liveapis import appws
    appweb.mount("/ws", appws)
    return appweb

v0 = __load_api_v0()
