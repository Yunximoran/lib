try: from .redis import Workbench as Redis
except ImportError: pass

try: from .mysql import WorkBench as MySQL
except ImportError: pass

try: from .mongo import WorkBench as MonGO
except ImportError: pass