# OLIB - object library
#
#

import ol

classes = ol.Object()
mods = ol.Object()
funcs = ol.Object()
names = ol.Object()

ol.update(classes, {"Bus": ["ol.bus"], "Cfg": ["gmod.udp"], "Console": ["ol.csl"], "DCC": ["gmod.irc"], "Event": ["gmod.irc"], "Feed": ["gmod.rss"], "Fetcher": ["gmod.rss"], "Getter": ["ol.prs"], "Handler": ["ol.hdl"], "IRC": ["gmod.irc"], "Kernel": ["ol.krn"], "Loader": ["ol.ldr"], "Log": ["gmod.ent"], "Option": ["ol.prs"], "Repeater": ["ol.tms"], "Rss": ["gmod.rss"], "Seen": ["gmod.rss"], "Setter": ["ol.prs"], "Skip": ["ol.prs"], "Timed": ["ol.prs"], "Timer": ["ol.tms"], "Todo": ["gmod.ent"], "Token": ["ol.prs"], "UDP": ["gmod.udp"], "User": ["gmod.irc"], "Users": ["gmod.irc"]})

ol.update(mods, {"cfg": "gmod.cfg", "cmd": "gmod.cmd", "dne": "gmod.ent", "dpl": "gmod.rss", "fed": "gmod.rss", "fnd": "gmod.fnd", "ftc": "gmod.rss", "log": "gmod.ent", "req": "gmod.req", "rm": "gmod.rss", "rss": "gmod.rss", "sts": "gmod.sts", "tdo": "gmod.ent", "trt": "gmod.trt", "tsk": "gmod.cmd", "upt": "gmod.cmd", "ver": "gmod.cmd", "wsd": "gmod.wsd"})

ol.update(funcs, {"cfg": "gmod.cfg.cfg", "cmd": "gmod.cmd.cmd", "dne": "gmod.ent.dne", "dpl": "gmod.rss.dpl", "fed": "gmod.rss.fed", "fnd": "gmod.fnd.fnd", "ftc": "gmod.rss.ftc", "log": "gmod.ent.log", "req": "gmod.req.req", "rm": "gmod.rss.rm", "rss": "gmod.rss.rss", "sts": "gmod.sts.sts", "tdo": "gmod.ent.tdo", "trt": "gmod.trt.trt", "tsk": "gmod.cmd.tsk", "upt": "gmod.cmd.upt", "ver": "gmod.cmd.ver", "wsd": "gmod.wsd.wsd"})

ol.update(names, {"bus": ["ol.bus.Bus"], "cfg": ["gmod.udp.Cfg"], "console": ["ol.csl.Console"], "dcc": ["gmod.irc.DCC"], "event": ["gmod.irc.Event"], "feed": ["gmod.rss.Feed"], "fetcher": ["gmod.rss.Fetcher"], "getter": ["ol.prs.Getter"], "handler": ["ol.hdl.Handler"], "irc": ["gmod.irc.IRC"], "kernel": ["ol.krn.Kernel"], "loader": ["ol.ldr.Loader"], "log": ["gmod.ent.Log"], "option": ["ol.prs.Option"], "repeater": ["ol.tms.Repeater"], "rss": ["gmod.rss.Rss"], "seen": ["gmod.rss.Seen"], "setter": ["ol.prs.Setter"], "skip": ["ol.prs.Skip"], "timed": ["ol.prs.Timed"], "timer": ["ol.tms.Timer"], "todo": ["gmod.ent.Todo"], "token": ["ol.prs.Token"], "udp": ["gmod.udp.UDP"], "user": ["gmod.irc.User"], "users": ["gmod.irc.Users"]})
