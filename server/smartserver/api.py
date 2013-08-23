#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["v0", "v2"]


def __load_api_v0():
    from .v0.groupapis import appweb
    from .v0.liveapis import appws
    from .v0.fileapis import appfs
    appweb.mount("/ws", appws)
    appweb.mount("/fs", appfs)
    return appweb

def __load_api_v2():
    from .v2.groupapis import appweb
    #from .v2.liveapis import appws
    #from .v2.fileapis import appfs
    #appweb.mount("/ws", appws)
    #appweb.mount("/fs", appfs)
    return appweb

v0 = __load_api_v0()

v2 = __load_api_v2()
