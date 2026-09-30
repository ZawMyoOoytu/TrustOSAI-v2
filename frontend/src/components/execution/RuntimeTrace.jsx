export default function RuntimeTrace({

    trace,
    execution

}) {


    if(!trace && !execution){

        return null;

    }







    // =====================================
    // SAFE PARSER
    // =====================================


    function parse(value){


        if(!value){

            return {};

        }



        if(typeof value === "object"){

            return value;

        }



        try{

            return JSON.parse(value);

        }

        catch{

            return {};

        }


    }









    // =====================================
    // NORMALIZE TRACE DATA
    // =====================================


    const parsedTrace =


        parse(

            trace

        );








    const executionResult =


        parse(

            execution?.result

        );









    const normalizedTrace =


        parsedTrace.trace

        ??

        parsedTrace.result?.trace

        ??

        parsedTrace.result?.result?.trace

        ??

        executionResult.trace

        ??

        executionResult.result?.trace

        ??

        {};









    const traceOutput =


        normalizedTrace.output

        ??

        executionResult.output

        ??

        executionResult.result

        ??

        {};









    // =====================================
    // VALUES
    // =====================================


    const engine =


        normalizedTrace.engine

        ??

        "ExecutionEngine";








    const status =


        traceOutput.status

        ??

        executionResult.status

        ??

        execution?.status

        ??

        "UNKNOWN";








    const model =


        traceOutput.model

        ??

        executionResult.model

        ??

        execution?.model

        ??

        "N/A";








    const latency =


        normalizedTrace.latency_ms

        ??

        traceOutput.latency_ms

        ??

        executionResult.runtime_ms

        ??

        execution?.runtime_ms

        ??

        0;








    const timestamp =


        normalizedTrace.timestamp

        ??

        execution?.created_at

        ??

        null;









    return (



        <div className="trace-card">







            <h2>

                🔍 Runtime Trace

            </h2>









            <div className="runtime-list">







                <p>


                    <span>

                        Engine

                    </span>




                    <strong>

                        {engine}

                    </strong>



                </p>









                <p>


                    <span>

                        Status

                    </span>





                    <strong


                        className={


                            status === "COMPLETED"

                            ||

                            status === "SUCCESS"


                            ?


                            "status-success"


                            :


                            "status-error"


                        }


                    >


                        {status}


                    </strong>



                </p>












                <p>


                    <span>

                        Model

                    </span>





                    <strong>

                        {model}

                    </strong>



                </p>












                <p>


                    <span>

                        Latency

                    </span>





                    <strong>


                        {

                            Number(

                                latency

                            )

                            .toFixed(3)


                        }

                        ms


                    </strong>



                </p>












                <p>


                    <span>

                        Timestamp

                    </span>





                    <strong>


                    {


                        timestamp


                        ?


                        new Date(

                            timestamp

                        )

                        .toLocaleString()



                        :



                        "N/A"



                    }


                    </strong>



                </p>








            </div>












            {/* =========================
                EXECUTION PIPELINE
            ========================== */}





            <div className="execution-pipeline">







                <div className="pipeline-node">

                    Request

                </div>





                <div className="pipeline-arrow">

                    ↓

                </div>







                <div className="pipeline-node">

                    Policy Engine

                </div>






                <div className="pipeline-arrow">

                    ↓

                </div>







                <div className="pipeline-node">

                    Trust Engine

                </div>






                <div className="pipeline-arrow">

                    ↓

                </div>







                <div className="pipeline-node active">

                    ExecutionEngine

                </div>






                <div className="pipeline-arrow">

                    ↓

                </div>







                <div className="pipeline-node">

                    Audit Storage

                </div>







            </div>












            {/* DEBUG TRACE JSON */}


            {


                Object.keys(normalizedTrace).length > 0 &&



                <details

                    className="json-container"

                >



                    <summary>

                        🔎 Raw Trace Data

                    </summary>





                    <pre

                        className="json-viewer"

                    >


                    {

                        JSON.stringify(

                            normalizedTrace,

                            null,

                            2

                        )

                    }


                    </pre>



                </details>


            }







        </div>



    );


}