from datetime import datetime



class TelemetryEngine:


    def __init__(self):

        self.events=[]




    def collect(
        self,
        task:str,
        result:dict
    ):


        telemetry={


            "task_preview":
                task[:80],


            "agent":
                result.get(
                    "agent",
                    "unknown"
                ),


            "trust_score":
                result.get(
                    "trust_score",
                    0
                ),


            "risk_score":
                result.get(
                    "risk_score",
                    0
                ),


            "decision":
                result.get(
                    "decision",
                    "UNKNOWN"
                ),


            "quality_score":
                result.get(
                    "quality_score",
                    0.0
                ),


            "timestamp":
                datetime.utcnow()

        }



        self.events.append(

            telemetry

        )


        return telemetry




    def get_events(
        self,
        limit=50
    ):

        return self.events[-limit:]