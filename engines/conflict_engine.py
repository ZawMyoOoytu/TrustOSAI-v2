from sqlalchemy.orm import Session
from typing import Dict, Any, Tuple
import time

from database.repository import MetricsRepository



class ConflictEngine:

    """
    TrustOSAI Conflict Detection Engine

    Functions:

    - Concurrent execution protection
    - Multi-agent race detection
    - State mutation analysis
    - Governance conflict scoring
    - Runtime trace generation

    """



    def __init__(self):

        self.time_window_seconds = 5.0


        self.conflict_triggers = [

            "update",
            "delete",
            "write",
            "modify",
            "allocate",
            "create",
            "insert"

        ]



    # =====================================================
    # Main Conflict Interface
    # =====================================================

    def detect(
        self,
        task: str,
        policy_result: Dict[str, Any],
        db: Session,
        execution_id=None
    ) -> Dict[str, Any]:


        start = time.time()



        has_conflict, metadata = self.check_concurrency(

            {
                "task": task,

                "policy": policy_result

            },

            db

        )



        latency = round(

            (time.time()-start)*1000,

            3

        )



        response = {


            "conflict_score":

                1.0 if has_conflict else 0.0,


            "status":

                (
                    "CONFLICT_DETECTED"
                    if has_conflict
                    else
                    "NO_CONFLICT"
                ),


            "metadata":

                metadata,


            "trace":

            {

                "engine":
                    "ConflictEngine",


                "execution_id":
                    execution_id,


                "latency_ms":
                    latency

            }

        }



        return response





    # =====================================================
    # Concurrency Scanner
    # =====================================================

    def check_concurrency(

        self,

        request_data: Dict[str, Any],

        db: Session

    ) -> Tuple[bool, Dict[str, Any]]:



        task_content = (

            request_data
            .get(
                "task",
                ""
            )
            .lower()

        )



        # ---------------------------------------------
        # 1. Detect state mutation
        # ---------------------------------------------


        is_mutation = any(

            trigger in task_content

            for trigger in self.conflict_triggers

        )



        if not is_mutation:


            return False, {


                "status":
                    "NO_CONFLICT",


                "reason":
                    "Read-only execution. No state mutation detected."

            }




        # ---------------------------------------------
        # 2. Search recent executions
        # ---------------------------------------------


        try:


            repo = MetricsRepository(db)



            recent_tasks = repo.get_duplicate_tasks_within_window(

                task_snippet=

                    task_content[:50],


                seconds_window=

                    self.time_window_seconds

            )



        except Exception as error:



            return False, {


                "status":

                    "AUDIT_FAILED",


                "reason":

                    str(error)

            }




        # ---------------------------------------------
        # 3. Conflict Found
        # ---------------------------------------------


        if recent_tasks:


            conflicts=[]


            for item in recent_tasks:


                conflicts.append({

                    "id":

                        item.id,


                    "agent":

                        item.agent,


                    "created_at":

                        item.created_at

                })



            return True, {


                "status":

                    "CONFLICT_DETECTED",



                "reason":

                    (
                        "Concurrent mutation detected. "
                        f"{len(conflicts)} execution(s) "
                        f"within {self.time_window_seconds}s."
                    ),



                "conflicting_records":

                    conflicts

            }




        # ---------------------------------------------
        # 4. Safe execution
        # ---------------------------------------------


        return False, {


            "status":

                "CLEARED",



            "reason":

                "Execution isolation verified."

        }