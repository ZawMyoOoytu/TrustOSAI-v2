from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session, joinedload

from database.session import get_db

from database.models import (
    Agent,
    Execution,
    AgentMemoryConfig
)

from schemas.agent import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentStatsResponse
)



# =====================================================
# ROUTER
# =====================================================

router = APIRouter(
    prefix="/api/agents",
    tags=[
        "Agents"
    ]
)



# =====================================================
# HELPER
# =====================================================

def load_agent(
    db: Session,
    agent_id: int
):

    return (

        db.query(Agent)

        .options(
            joinedload(
                Agent.memory_config
            )
        )

        .filter(
            Agent.id == agent_id
        )

        .first()

    )



# =====================================================
# CREATE AGENT
# =====================================================

@router.post(
    "/",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_agent(
    data: AgentCreate,
    db: Session = Depends(get_db)
):

    try:

        existing = (

            db.query(Agent)

            .filter(
                Agent.name == data.name
            )

            .first()

        )


        if existing:

            raise HTTPException(

                status_code=400,

                detail="Agent already exists"

            )



        agent = Agent(

            name=data.name,

            description=data.description,

            agent_type=data.agent_type,

            model=data.model,

            provider=data.provider,

            trust_threshold=data.trust_threshold,

            risk_level=data.risk_level,

            status=data.status,

            metadata_json=data.metadata_json or {}

        )


        db.add(agent)

        db.flush()



        memory_data = data.memory



        memory = AgentMemoryConfig(

            agent_id=agent.id,

            enabled=(

                memory_data.enabled

                if memory_data

                else True

            ),

            memory_type=(

                memory_data.memory_type

                if memory_data

                else "LONG_TERM"

            ),

            max_context_tokens=(

                memory_data.max_context_tokens

                if memory_data

                else 8000

            ),

            retention_days=(

                memory_data.retention_days

                if memory_data

                else 365

            )

        )


        db.add(memory)



        db.commit()



        # IMPORTANT
        # Reload with memory relationship

        agent = load_agent(
            db,
            agent.id
        )


        return agent



    except HTTPException:

        raise



    except Exception as e:

        db.rollback()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )





# =====================================================
# GET ALL AGENTS
# =====================================================

@router.get(
    "/",
    response_model=list[AgentResponse]
)
def get_agents(
    db: Session = Depends(get_db)
):


    agents = (

        db.query(Agent)

        .options(

            joinedload(
                Agent.memory_config
            )

        )

        .order_by(

            Agent.created_at.desc()

        )

        .all()

    )


    return agents





# =====================================================
# GET SINGLE AGENT
# =====================================================

@router.get(
    "/{agent_id}",
    response_model=AgentResponse
)
def get_agent(
    agent_id:int,
    db:Session=Depends(get_db)
):


    agent = load_agent(
        db,
        agent_id
    )


    if not agent:

        raise HTTPException(

            status_code=404,

            detail="Agent not found"

        )


    return agent





# =====================================================
# UPDATE AGENT
# =====================================================

@router.patch(
    "/{agent_id}",
    response_model=AgentResponse
)
def update_agent(
    agent_id:int,
    data:AgentUpdate,
    db:Session=Depends(get_db)
):


    agent = load_agent(
        db,
        agent_id
    )


    if not agent:

        raise HTTPException(

            status_code=404,

            detail="Agent not found"

        )



    payload = data.model_dump(
        exclude_unset=True
    )



    memory_data = payload.pop(
        "memory",
        None
    )



    for key,value in payload.items():

        setattr(

            agent,

            key,

            value

        )




    if memory_data:


        if agent.memory_config:


            for key,value in memory_data.items():

                setattr(

                    agent.memory_config,

                    key,

                    value

                )


        else:


            memory = AgentMemoryConfig(

                agent_id=agent.id,

                **memory_data

            )


            db.add(memory)



    db.commit()



    return load_agent(
        db,
        agent_id
    )





# =====================================================
# AGENT STATISTICS
# =====================================================

@router.get(
    "/{agent_id}/stats",
    response_model=AgentStatsResponse
)
def agent_stats(
    agent_id:int,
    db:Session=Depends(get_db)
):


    agent = (

        db.query(Agent)

        .filter(

            Agent.id == agent_id

        )

        .first()

    )


    if not agent:

        raise HTTPException(

            status_code=404,

            detail="Agent not found"

        )



    executions = (

        db.query(Execution)

        .filter(

            Execution.agent_id == agent_id

        )

        .all()

    )


    total = len(executions)



    blocked = sum(

        1

        for e in executions

        if e.decision=="BLOCK"

    )



    average_trust = (

        round(

            sum(

                e.trust_score or 0

                for e in executions

            )

            / total,

            2

        )

        if total

        else 0

    )



    average_latency = (

        round(

            sum(

                e.latency_ms or 0

                for e in executions

            )

            / total,

            2

        )

        if total

        else 0

    )



    total_cost = sum(

        e.cost_usd or 0

        for e in executions

    )



    success_rate = (

        round(

            ((total-blocked)/total)*100,

            2

        )

        if total

        else 0

    )



    agent.total_executions = total

    agent.average_trust = average_trust


    db.commit()



    return {

        "agent_id":agent.id,

        "agent_name":agent.name,

        "model":agent.model,

        "provider":agent.provider,

        "status":agent.status,

        "total_executions":total,

        "average_trust":average_trust,

        "success_rate":success_rate,

        "blocked_count":blocked,

        "average_latency_ms":average_latency,

        "total_cost_usd":total_cost

    }





# =====================================================
# DISABLE AGENT
# =====================================================

@router.patch(
    "/{agent_id}/disable"
)
def disable_agent(
    agent_id:int,
    db:Session=Depends(get_db)
):


    agent = db.query(Agent).filter(
        Agent.id==agent_id
    ).first()


    if not agent:

        raise HTTPException(

            status_code=404,

            detail="Agent not found"

        )


    agent.status="DISABLED"

    db.commit()


    return {

        "message":"Agent disabled",

        "agent_id":agent.id,

        "status":agent.status

    }





# =====================================================
# ENABLE AGENT
# =====================================================

@router.patch(
    "/{agent_id}/enable"
)
def enable_agent(
    agent_id:int,
    db:Session=Depends(get_db)
):


    agent = db.query(Agent).filter(
        Agent.id==agent_id
    ).first()



    if not agent:

        raise HTTPException(

            status_code=404,

            detail="Agent not found"

        )


    agent.status="ACTIVE"


    db.commit()


    return {

        "message":"Agent enabled",

        "agent_id":agent.id,

        "status":agent.status

    }