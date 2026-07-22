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







export default function ExecutionDetail(){


    const {id}=useParams();

    const navigate=useNavigate();



    const [execution,setExecution]=useState(null);


    const [replayData,setReplayData]=useState(null);


    const [replayMode,setReplayMode]=useState(false);



    const [
        trustExplanation,
        setTrustExplanation
    ] = useState(null);



    const [
        decisionReasoning,
        setDecisionReasoning
    ] = useState(null);





    const [
        replayTrustExplanation,
        setReplayTrustExplanation
    ] = useState(null);



    const [
        replayDecisionReasoning,
        setReplayDecisionReasoning
    ] = useState(null);





    const [
        loading,
        setLoading
    ] = useState(true);



    const [
        error,
        setError
    ] = useState("");








    // ======================================
    // SAFE JSON
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


        const result =
            parseJSON(data.result);



        return {


            ...data,



            execution_id:

                data.execution_id
                ??
                data.id,



            model:

                data.model
                ??
                result.model
                ??
                result.trace?.output?.model
                ??
                data.agent
                ??
                "unknown",




            agent:

                data.agent
                ??
                "unknown",




            provider:

                data.provider
                ??
                result.trace?.output?.provider
                ??
                "local",




            telemetry:


                data.telemetry
                ??
                {


                    latency_ms:

                        data.runtime_ms
                        ??
                        result.latency_ms
                        ??
                        0,



                    quality_score:

                        data.quality_score
                        ??
                        result.quality_score_qt
                        ??
                        result.trace?.output?.quality_score
                        ??
                        0


                },




            governance:

                data.governance
                ??
                {}

        };


    }









    // ======================================
    // LOAD GOVERNANCE DATA
    // ======================================

    async function loadGovernance(
        executionId,
        replay=false
    ){


        try{


            const trust =
            await fetch(

                `http://localhost:8000/trust/explanation/${executionId}`

            );



            if(trust.ok){


                const data =
                await trust.json();



                replay
                ?
                setReplayTrustExplanation(data)
                :
                setTrustExplanation(data);


            }


        }

        catch{

            replay
            ?
            setReplayTrustExplanation(null)
            :
            setTrustExplanation(null);

        }






        try{


            const reasoning =
            await fetch(

                `http://localhost:8000/reasoning/${executionId}`

            );



            if(reasoning.ok){


                const data =
                await reasoning.json();



                replay
                ?
                setReplayDecisionReasoning(data)
                :
                setDecisionReasoning(data);


            }


        }

        catch{

            replay
            ?
            setReplayDecisionReasoning(null)
            :
            setDecisionReasoning(null);

        }


    }









    // ======================================
    // LOAD ORIGINAL
    // ======================================

    useEffect(()=>{


        async function load(){


            try{


                setLoading(true);



                const response =
                await fetch(

                    `http://localhost:8000/executions/${id}`

                );



                if(!response.ok){

                    throw new Error(
                        "Execution not found"
                    );

                }



                const data =
                await response.json();



                const normalized =
                normalizeExecution(data);



                setExecution(normalized);



                await loadGovernance(
                    normalized.execution_id,
                    false
                );


            }


            catch(err){


                console.error(err);


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


            const response =
            await fetch(

                `http://localhost:8000/replay/${id}`,

                {

                    method:"POST"

                }

            );



            if(!response.ok){

                throw new Error(
                    "Replay failed"
                );

            }




            const data =
            await response.json();



            setReplayData(data);



            setReplayMode(true);



            const replayId =
                data.replay_result.execution_id;



            await loadGovernance(
                replayId,
                true
            );



        }


        catch(err){


            console.error(
                "Replay Error",
                err
            );


        }


    }









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








    // ======================================
    // ACTIVE EXECUTION
    // ======================================


    const replayExecutionData =


        replayData?.replay_result

        ?

        normalizeExecution(
            replayData.replay_result
        )

        :

        null;






    const activeExecution =


        replayMode && replayExecutionData

        ?

        replayExecutionData

        :

        execution;







    const output =

        parseJSON(
            activeExecution.result
        );







    const activeTrustExplanation =


        replayMode

        ?

        replayTrustExplanation

        :

        trustExplanation;





    const activeDecisionReasoning =


        replayMode

        ?

        replayDecisionReasoning

        :

        decisionReasoning;









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

        activeExecution.telemetry?.latency_ms

        ??

        activeExecution.runtime_ms

        ??

        0;







    const tokens =


        output.token_telemetry

        ??

        activeExecution.token_telemetry

        ??

        {


            prompt_tokens:0,

            completion_tokens:0

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
                replayMode &&


                <div className="replay-banner">


                    🔁 Replay Mode


                    <br/>


                    Original Execution #

                    {
                        replayData.original_execution_id
                    }



                    <br/>


                    Replay Execution #

                    {
                        replayExecutionData.execution_id
                    }



                </div>

            }









            <button

                className="replay-btn"

                onClick={handleReplayExecution}

            >

                🔁 Replay Execution

            </button>









            {
                replayMode &&
                replayExecutionData &&


                <ExecutionComparison

                    original={execution}

                    replay={replayExecutionData}

                />

            }










            <ExecutionHeader

                execution={activeExecution}

            />







            <ExecutionOverview

                execution={activeExecution}

            />








            <TrustExplanation

                data={activeTrustExplanation}

            />







            <DecisionReasoning

                data={activeDecisionReasoning}

            />








            <ExecutionActions

                execution={activeExecution}

            />








            <div className="advanced-grid">


                <TrustGauge

                    score={
                        activeExecution.trust_score ?? 0
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

                trace={
                    output.trace ?? {}
                }

            />





        </div>

    );


}