# Copyright (c) 1994-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

from ._platform import DLL_PATH, DLL

try:
    dll = DLL(DLL_PATH)
except OSError as exc:  # pragma: no cover
    raise exc
except Exception as exc:  # pragma: no cover
    raise OSError("{}".format(exc))
