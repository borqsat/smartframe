#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["v1"]


def __load_api_v1():
    from .v1.groupapis import appweb
    from .v1.liveapis import appws
    from .v1.fileapis import appfs
    appweb.mount("/ws", appws)
    appweb.mount("/fs", appfs)
    return appweb

v1 = __load_api_v1()
