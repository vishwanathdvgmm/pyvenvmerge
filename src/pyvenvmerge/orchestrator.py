from pyvenvmerge.core.executor import execute_plan
from pyvenvmerge.core.planner import create_merge_plan

def merge_environments(env_paths: list[str], output_path: str, strategy="highest"):
    """
    Full pipeline:
    Planner → Executor
    """

    plan = create_merge_plan(env_paths, strategy)
    
    execute_plan(plan, output_path)

    return output_path
