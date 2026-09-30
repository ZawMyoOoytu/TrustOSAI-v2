from typing import Dict, Any, List
from datetime import datetime


class MemoryEngine:
    """
    TrustOSAI Persistent Memory Fabric

    Layers:

    L1:
        Runtime Context Memory

    L2:
        Semantic Retrieval Memory

    L3:
        Execution Experience Memory


    Responsibilities:

    - Retrieve previous execution context
    - Store execution experience
    - Feed quality feedback to Trust Engine
    """



    def __init__(self):

        # Temporary runtime memory cache
        # PostgreSQL vector memory can replace later

        self.memory_store = []



    # =====================================================
    # Context Retrieval
    # =====================================================

    def retrieve_context(
        self,
        task: str,
        db=None
    ) -> Dict[str, Any]:


        matches = []


        task_lower = task.lower()


        for item in self.memory_store:


            if any(

                word in item["task"].lower()

                for word in task_lower.split()

            ):

                matches.append(item)



        return {


            "memory_hits":
                len(matches),


            "context":

                matches[-5:],


            "retrieved_at":

                datetime.utcnow()

        }



    # =====================================================
    # Memory Update
    # =====================================================

    def update_memory(
        self,
        db,
        task: str,
        response: Any,
        quality_score: float = 0.0
    ):


        memory_item = {


            "task":

                task,


            "response":

                response,


            "quality_score":

                quality_score
                if quality_score
                else 0.0,


            "timestamp":

                datetime.utcnow()

        }



        self.memory_store.append(

            memory_item

        )


        return memory_item



    # =====================================================
    # History
    # =====================================================

    def get_recent_memory(
        self,
        limit=10
    ) -> List[Dict[str,Any]]:


        return self.memory_store[-limit:]