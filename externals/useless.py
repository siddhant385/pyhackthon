import platform


def basic_systeminfo():
    info = f"""Online🟢  and Ready
Platform: {platform.platform()}
Python Version: {platform.python_version()}
Machine: {platform.machine()}
Processor: {platform.processor()}
Hostname: {platform.node()}
System: {platform.system()}

"""
    return info
