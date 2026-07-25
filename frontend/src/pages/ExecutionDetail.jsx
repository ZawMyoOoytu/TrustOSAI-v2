import {
    useParams,
    useNavigate
} from "react-router-dom";

import {
    useEffect,
    useState
} from "react";


// ======================================
// Components
// ======================================

import ExecutionHeader
from "../components/execution/ExecutionHeader";

import ExecutionOverview
from "../components/execution/ExecutionOverview";

import ExecutionActions
from "../components/execution/ExecutionActions";

import GovernanceTimeline
from "../components/execution/GovernanceTimeline";

import AgentOutputViewer
from "../components/execution/AgentOutputViewer";

import TokenTelemetry
from "../components/execution/TokenTelemetry";

import RuntimeTrace
from "../components/execution/RuntimeTrace";

import TrustGauge
from "../components/execution/TrustGauge";

import QualityCard
from "../components/execution/QualityCard";

import LatencyCard
from "../components/execution/LatencyCard";

import TrustExplanation
from "../components/execution/TrustExplanation";

import DecisionReasoning
from "../components/execution/DecisionReasoning";

import ExecutionComparison
from "../components/execution/ExecutionComparison";


import "../styles/ExecutionDetail.css";




// ======================================
// API
// ======================================

const API =
"http://localhost:8000/api";





export default function ExecutionDetail(){


    const {id} = useParams();


    const navigate = useNavigate();




    const [execution,setExecution] =
    useState(null);


    const [replayExecution,setReplayExecution] =
    useState(null);


    const [replayMode,setReplayMode] =
    useState(false);


    const [loading,setLoading] =
    useState(true);


    const [error,setError] =
    useState("");


    const [replayError,setReplayError] =
    useState("");



    const [trustExplanation,setTrustExplanation] =
    useState(null);


    const [decisionReasoning,setDecisionReasoning] =
    useState(null);


    const [replayTrustExplanation,setReplayTrustExplanation] =
    useState(null);


    const [replayDecisionReasoning,setReplayDecisionReasoning] =
    useState(null);







    // ======================================
    // JSON PARSER
    // ======================================


    function parseJSON(value){


        if(!value){

            return {};

        }


        if(typeof value==="object"){

            return value;

        }



        try{

            return JSON.parse(value);

        }

        catch{

            return {
                response:value
            };

        }

    }









    // ======================================
    // NORMALIZER
    // ======================================


    function normalizeExecution(data){


        if(!data){

            return null;

        }



        /*
        
        Normal:

        {
          execution_id:1,
          result:{}
        }


        Replay:

        {
          replay_result:{
              execution_id:166,
              result:{}
          }
        }

        */


        const payload =


            data.replay_result

            ??

            data.result?.execution_id

            ?

            data.result

            :

            data;







        const output =


            parseJSON(

                payload.result

            );







        return {


            ...payload,



            execution_id:


                payload.execution_id

                ??

                payload.id

                ??

                data.replay_execution_id

                ??

                null,







            task:


                payload.task

                ??

                output.task

                ??

                "No task provided",






            agent:


                payload.agent

                ??

                output.agent

                ??

                "unknown",








            model:


                payload.model

                ??

                output.model

                ??

                output.trace?.output?.model

                ??

                "unknown",








            provider:


                payload.provider

                ??

                output.provider

                ??

                "local",







            decision:


                payload.decision

                ??

                output.decision

                ??

                "UNKNOWN",







            trust_score:


                payload.trust_score

                ??

                output.trust_score

                ??

                0,







            risk_score:


                payload.risk_score

                ??

                output.risk_score

                ??

                0,







            result:output,







            token_telemetry:


                payload.token_telemetry

                ??

                output.token_telemetry

                ??

                {


                    prompt_tokens:0,

                    completion_tokens:0,

                    total_tokens:0


                },









            telemetry:


                payload.telemetry

                ??

                {


                    latency_ms:


                        payload.runtime_ms

                        ??

                        output.runtime_ms

                        ??

                        0,




                    quality_score:


                        payload.quality_score

                        ??

                        output.quality_score

                        ??

                        0


                }



        };


    }









    // ======================================
    // LOAD GOVERNANCE
    // ======================================


    async function loadGovernance(
        executionId,
        replay=false
    ){


        if(!executionId){

            return;

        }



        try{


            const res =
            await fetch(
                `${API}/trust/explanation/${executionId}`
            );


            if(res.ok){


                const data =
                await res.json();


                replay

                ?

                setReplayTrustExplanation(data)

                :

                setTrustExplanation(data);


            }


        }

        catch(err){

            console.log(err);

        }






        try{


            const res =
            await fetch(
                `${API}/reasoning/${executionId}`
            );


            if(res.ok){


                const data =
                await res.json();


                replay

                ?

                setReplayDecisionReasoning(data)

                :

                setDecisionReasoning(data);


            }


        }

        catch(err){

            console.log(err);

        }


    }









    // ======================================
    // LOAD EXECUTION
    // ======================================


    useEffect(()=>{


        async function load(){


            try{


                setLoading(true);



                const res =
                await fetch(
                    `${API}/executions/${id}`
                );



                if(!res.ok){

                    throw new Error(
                        "Execution not found"
                    );

                }



                const data =
                await res.json();



                const normalized =
                normalizeExecution(data);



                setExecution(
                    normalized
                );



                await loadGovernance(

                    normalized.execution_id,

                    false

                );



            }

            catch(err){


                setError(
                    err.message
                );


            }

            finally{


                setLoading(false);

            }


        }


        load();


    },[id]);









    // ======================================
    // REPLAY
    // ======================================


    async function handleReplayExecution(){


        try{


            setReplayError("");



            const res =
            await fetch(

                `${API}/replay/${id}`,

                {

                    method:"POST",

                    headers:{

                        "Content-Type":
                        "application/json"

                    }

                }

            );



            if(!res.ok){

                throw new Error(
                    await res.text()
                );

            }



            const data =
            await res.json();





            const replay =

            normalizeExecution({

                ...data.replay_result,

                replay_execution_id:
                data.replay_execution_id

            });





            setReplayExecution(
                replay
            );


            setReplayMode(true);





            await loadGovernance(

                replay.execution_id,

                true

            );



        }

        catch(err){


            console.error(err);


            setReplayError(
                err.message
            );


        }


    }








    const activeExecution =


        replayMode && replayExecution

        ?

        replayExecution

        :

        execution;









    if(loading){

        return (

            <div className="execution-page">

                <h2>
                    Loading Execution Trace...
                </h2>

            </div>

        );

    }







    if(error){

        return (

            <div className="execution-page">

                <h2>
                    ❌ {error}
                </h2>

            </div>

        );

    }






    if(!activeExecution){

        return null;

    }






    const output =

        activeExecution.result

        ??

        {};






    const qualityScore =


        output.quality_score_qt

        ??

        output.quality_score

        ??

        activeExecution.telemetry?.quality_score

        ??

        0;






    const latency =


        output.latency_ms

        ??

        output.runtime_ms

        ??

        activeExecution.telemetry?.latency_ms

        ??

        0;






    const tokens =


        activeExecution.token_telemetry

        ??

        {


            prompt_tokens:0,

            completion_tokens:0,

            total_tokens:0


        };






    return (

        <div className="execution-page">



            <button

                className="back-btn"

                onClick={()=>navigate("/executions")}

            >

                ← Back

            </button>







            {
                replayMode && replayExecution &&

                <div className="replay-banner">

                    🔁 Replay Mode

                    <br/>

                    Original Execution #

                    {execution.execution_id}

                    <br/>

                    Replay Execution #

                    {replayExecution.execution_id}


                </div>

            }






            {
                replayError &&

                <div className="error-box">

                    ❌ {replayError}

                </div>

            }





            <button

                className="replay-btn"

                onClick={handleReplayExecution}

            >

                🔁 Replay Execution

            </button>







            {
                replayMode && replayExecution &&

                <ExecutionComparison

                    original={execution}

                    replay={replayExecution}

                />

            }







            <ExecutionHeader

                execution={activeExecution}

            />





            <ExecutionOverview

                execution={activeExecution}

            />





            <TrustExplanation

                data={
                    replayMode
                    ?
                    replayTrustExplanation
                    :
                    trustExplanation
                }

            />





            <DecisionReasoning

                data={
                    replayMode
                    ?
                    replayDecisionReasoning
                    :
                    decisionReasoning
                }

            />







            <ExecutionActions

                execution={activeExecution}

            />








            <div className="advanced-grid">


                <TrustGauge

                    score={
                        activeExecution.trust_score
                        ??
                        0
                    }

                />



                <QualityCard

                    score={qualityScore}

                />



                <LatencyCard

                    latency={latency}

                />


            </div>








            <GovernanceTimeline

                execution={activeExecution}

            />







            <AgentOutputViewer

                output={output}

            />








            <TokenTelemetry

                data={tokens}

            />








            <RuntimeTrace

                trace={output.trace}

                execution={activeExecution}

            />






        </div>

    );


}