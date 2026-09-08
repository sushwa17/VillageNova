from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "village_hub"))
from domain_runtime import run

if __name__ == "__main__":
    run("health", Path(__file__).parent)
