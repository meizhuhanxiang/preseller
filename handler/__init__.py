import os

__author__ = 'guoguangchuan'
web_handlers = os.listdir(os.path.join(os.getcwd(), 'handler'))
__all__ = []
for k in web_handlers:
    if k != 'base' and os.path.isdir(os.path.join(os.getcwd(), 'handler', k)):
        __all__.append(k)


