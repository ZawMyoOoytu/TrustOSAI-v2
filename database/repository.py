from database.models import Execution



def create_execution(
    db,
    task,
    agent,
    trust_score,
    risk_score,
    decision,
    result
):


    execution = Execution(

        task=task,

        agent=agent,

        trust_score=trust_score,

        risk_score=risk_score,

        decision=decision,

        result=result

    )


    db.add(execution)

    db.commit()

    db.refresh(execution)


    return execution