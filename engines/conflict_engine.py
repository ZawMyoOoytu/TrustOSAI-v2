from sqlalchemy.orm import Session
from typing import Dict, Any, Tuple


from database.repository import MetricsRepository



class ConflictEngine:


    def __init__(self):

        # Conflict detection window
        self.time_window_seconds = 5.0


        # Operations that may create state conflicts
        self.conflict_triggers = [

            "update",
            "delete",
            "write",
            "modify",
            "allocate",
            "create",
            "insert"

        ]



    def detect(
        self,
        task: str,
        policy_result: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """
        TrustOSAI Governance Conflict Detection Interface.

        Returns:
        {
            conflict_score: float,
            status: str,
            metadata: dict
        }

        """



        has_conflict, metadata = self.check_concurrency(

            {
                "task": task,

                "policy": policy_result

            },

            db

        )



        if has_conflict:


            return {

                "conflict_score": 1.0,

                "status": "CONFLICT_DETECTED",

                "metadata": metadata

            }



        return {

            "conflict_score": 0.0,

            "status": "NO_CONFLICT",

            "metadata": metadata

        }




    def check_concurrency(
        self,
        request_data: Dict[str, Any],
        db: Session
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Detect concurrent execution conflicts.

        Used for:
        - multi-agent race prevention
        - state mutation protection
        - execution isolation

        """



        task_content = (

            request_data
            .get(
                "task",
                ""
            )
            .lower()

        )



        # -----------------------------------------------------
        # 1. Mutation Detection
        # -----------------------------------------------------

        is_mutative_operation = any(

            trigger in task_content

            for trigger in self.conflict_triggers

        )



        if not is_mutative_operation:


            return (

                False,

                {

                    "status": "NO_CONFLICT",

                    "reason":
                    "Read-only task. No shared state mutation detected."

                }

            )



        # -----------------------------------------------------
        # 2. Database Conflict Scan
        # -----------------------------------------------------

        try:


            repo = MetricsRepository(db)



            recent_tasks = repo.get_duplicate_tasks_within_window(

                task_snippet=

                    task_content[:50],

                seconds_window=

                    self.time_window_seconds

            )


        except Exception as e:


            return (

                False,

                {

                    "status": "AUDIT_FAILED",

                    "reason":

                    str(e)

                }

            )




        # -----------------------------------------------------
        # 3. Conflict Decision
        # -----------------------------------------------------

        if recent_tasks:


            conflicts = []



            for record in recent_tasks:


                conflicts.append(

                    {

                        "id":
                        record.id,


                        "agent":
                        record.agent,


                        "created_at":
                        record.created_at

                    }

                )



            return (

                True,

                {


                    "status":
                    "CONFLICT_DETECTED",


                    "reason":

                    (
                        "Concurrent mutation detected. "
                        f"{len(conflicts)} overlapping execution(s) "
                        f"within {self.time_window_seconds}s."
                    ),


                    "conflicting_records":

                    conflicts

                }

            )



        # -----------------------------------------------------
        # 4. Clean Execution State
        # -----------------------------------------------------

        return (

            False,

            {


                "status":
                "CLEARED",


                "reason":

                "Execution isolation verified. No conflicting state found."

            }

        )