# Questo file si occupa do aggiornare i moduli imoprtati in "__init__.py",
# che altrimenti userà una versione salvata nella cache e non aggiornata

from importlib import reload
import sys
import bpy
from . import *  # all the modules contained in the current package


def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return
    reload(sys.modules[__name__])
    reload(preferences)
    reload(operators)
    reload(panel)
