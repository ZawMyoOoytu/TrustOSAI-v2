from fastapi import APIRouter

from sqlalchemy.orm import Session

from fastapi import Depends


from database import get_db

from models import Execution


from schemas import (
    ExecutionRequest,
    ExecutionResponse
)


from engines.trust_engine import TrustEngine
from engines.risk_engine import RiskEngine
from engines.policy_engine import PolicyEngine
from engines.governance_engine import GovernanceEngine
from engines.router_engine import RouterEngine
from engines.execution_engine import ExecutionEngine
from engines.audit_engine import AuditEngine



router=APIRouter()



trust=TrustEngine()

risk=RiskEngine()

policy=PolicyEngine()

governance=GovernanceEngine()

router_engine=RouterEngine()

executor=ExecutionEngine()

audit=AuditEngine()



@router.post(
    "/execute",
    response_model=ExecutionResponse
)
def execute(

    request:ExecutionRequest,

    db:Session=Depends(get_db)

):


    trust_score = trust.calculate(
        request.agent
    )


    risk_score = risk.evaluate(
        request.task
    )


    policy_result = policy.check(
        request.task
    )


    decision = governance.decide(

        trust_score,

        risk_score,

        policy_result

    )


    route = router_engine.route(
        decision
    )


    if decision=="REJECTED":

        result="Blocked"


    else:

        result=executor.run(
            request.task
        )



    record=Execution(

        task=request.task,

        agent=request.agent,

        trust_score=trust_score,

        risk_score=risk_score,

        decision=decision,

        result=result

    )


    db.add(record)

    db.commit()



    audit.log({

        "task":request.task,

        "decision":decision,

        "route":route

    })


    return {


        "decision":decision,

        "trust_score":trust_score,

        "risk_score":risk_score,

        "result":result

    }