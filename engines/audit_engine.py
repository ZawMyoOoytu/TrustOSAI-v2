from datetime import datetime



class AuditEngine:


    def __init__(self):

        self.audit_logs=[]




    def record(
        self,
        task,
        trust,
        risk,
        governance,
        result,
        execution_id=None
    ):


        event={


            "execution_id":
                execution_id,


            "task":
                task,


            "trust_score":
                trust,


            "risk_score":
                risk,


            "governance":
                governance,


            "result":
                result,


            "timestamp":
                datetime.utcnow()

        }



        self.audit_logs.append(

            event

        )


        return event




    def get_logs(
        self,
        limit=50
    ):


        return self.audit_logs[-limit:]