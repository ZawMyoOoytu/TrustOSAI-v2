from database.models import Execution


class ReplayComparisonService:


    def compare(
        self,
        db,
        original_id,
        replay_id
    ):


        original = (
            db.query(Execution)
            .filter(
                Execution.id == original_id
            )
            .first()
        )


        replay = (
            db.query(Execution)
            .filter(
                Execution.id == replay_id
            )
            .first()
        )


        if not original or not replay:

            raise Exception(
                "Execution not found"
            )


        return {


            "original_execution": {

                "id": original.id,

                "decision": original.decision,

                "trust_score": original.trust_score,

                "risk_score": original.risk_score,

                "model": original.model

            },


            "replay_execution": {

                "id": replay.id,

                "decision": replay.decision,

                "trust_score": replay.trust_score,

                "risk_score": replay.risk_score,

                "model": replay.model

            },


            "comparison": {


                "trust_delta":

                    replay.trust_score
                    -
                    original.trust_score,


                "risk_delta":

                    replay.risk_score
                    -
                    original.risk_score,


                "decision_changed":

                    replay.decision
                    !=
                    original.decision,


                "model_changed":

                    replay.model
                    !=
                    original.model

            }

        }