import {
    useState
} from "react";



export default function ExecutionActions({

    execution

}) {


    const [
        replayResult,
        setReplayResult
    ] = useState(null);



    const [
        loading,
        setLoading
    ] = useState(false);



    const [
        error,
        setError
    ] = useState("");






    // =====================================
    // Replay Execution
    // =====================================

    async function replayExecution(){


        if(!execution?.execution_id){

            setError(
                "Missing execution id"
            );

            return;

        }



        try{


            setLoading(true);

            setError("");



            const response = await fetch(

                `http://localhost:8000/replay/${execution.execution_id}`,

                {
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json"
                    }
                }

            );





            if(!response.ok){


                throw new Error(
                    "Replay request failed"
                );


            }





            const data =
            await response.json();





            console.log(
                "Replay Result:",
                data
            );





            setReplayResult(data);



        }


        catch(err){


            console.error(
                err
            );


            setError(
                err.message
            );


        }


        finally{


            setLoading(false);


        }


    }









    // =====================================
    // Copy JSON
    // =====================================


    function copyJSON(){


        navigator.clipboard.writeText(

            JSON.stringify(

                execution,

                null,

                2

            )

        );


    }









    // =====================================
    // Export JSON
    // =====================================


    function exportJSON(){


        const blob = new Blob(

            [

                JSON.stringify(

                    execution,

                    null,

                    2

                )

            ],

            {
                type:
                "application/json"
            }

        );




        const url =
        URL.createObjectURL(blob);




        const link =
        document.createElement("a");



        link.href=url;



        link.download =

        `execution-${execution.execution_id}.json`;



        document.body.appendChild(link);



        link.click();



        document.body.removeChild(link);



        URL.revokeObjectURL(url);


    }








    // =====================================
    // Replay Response Mapping
    // =====================================


    const replay =

        replayResult?.replay_result;








    return (


        <div className="execution-actions">







            {
                error &&

                <div className="error-message">

                    ❌ {error}

                </div>

            }








            <button

                onClick={copyJSON}

            >

                📋 Copy JSON

            </button>









            <button

                onClick={replayExecution}

                disabled={loading}

            >

                {

                    loading

                    ?

                    "⏳ Running Replay..."

                    :

                    "▶ Replay Execution"

                }

            </button>









            <button

                onClick={exportJSON}

            >

                📥 Export JSON

            </button>












            {

                replayResult &&


                <div className="replay-panel">






                    <h3>

                        🔁 Replay Result

                    </h3>









                    <p>

                        Original ID:

                        {" "}

                        {

                            replayResult.original_execution_id

                        }

                    </p>









                    <p>

                        Task:

                        {" "}

                        {

                            replayResult.original_task

                            ??

                            "N/A"

                        }

                    </p>









                    <p>

                        Decision:

                        {" "}

                        {

                            replay?.decision

                            ??

                            "N/A"

                        }

                    </p>









                    <p>

                        Trust Score:

                        {" "}

                        {

                            replay?.trust_score

                            ??

                            "N/A"

                        }

                    </p>









                    <p>

                        Risk Score:

                        {" "}

                        {

                            replay?.risk_score

                            ??

                            "N/A"

                        }

                    </p>









                    <p>

                        Runtime:

                        {" "}

                        {

                            replay?.telemetry?.latency_ms

                            ??

                            "N/A"

                        }

                        ms

                    </p>









                    <pre>

                        {

                            JSON.stringify(

                                replayResult,

                                null,

                                2

                            )

                        }

                    </pre>







                </div>

            }








        </div>

    );


}