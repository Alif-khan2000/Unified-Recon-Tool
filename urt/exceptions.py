class URTError(Exception):
    """Base exception for Unified Recon Tool"""
    pass

class ModuleDependencyMissing(URTError):
    pass

class InvalidTarget(URTError):
    pass
