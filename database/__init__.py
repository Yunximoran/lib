try: from .redis import Workbench as Redis
except Exception: pass

try: from .mysql import WorkBench as MySQL
except Exception: pass

try: from .mongo import WorkBench as MonGO
except Exception: pass