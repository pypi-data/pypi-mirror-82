# -*- coding: utf-8 -*-
"""
Module gathering errors relative to pv pumping system.

@author: Tanguy Lunel
"""


class HeadError(Exception):
    """Raised when the head of the pump and the total head of the system
    don't match together.
    """
    pass


class CurrentError(Exception):
    """Raised when the current of the pvarray and the acceptable current range
    of the pump don't match together.
    """
    pass


class VoltageError(Exception):
    """Raised when the voltage of the pvarray and the acceptable voltage range
    of the pump don't match together.
    """
    pass


class PowerError(Exception):
    """Raised when the electric power is not sufficient or is too important
    for the pump.
    """
    pass


class LocationError(Exception):
    """Raised when the location object lacks some informations.
    """
    pass


class InsufficientDataError(Exception):
    """Raised when the pump object lacks some informations.
    """
    pass


class NoConvergenceError(Exception):
    """Raised when the pump object lacks some informations.
    """
    pass
