export default function RuntimeTrace({

    trace

}){


    if(!trace){

        return null;

    }



    const output =
    trace.output || {};




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
                        {
                            trace.engine
                            ||
                            "Unknown"
                        }
                    </strong>


                </p>









                <p>

                    <span>
                        Status
                    </span>


                    <strong

                    className={
                        output.status === "COMPLETED"
                        ?
                        "status-success"
                        :
                        "status-error"
                    }

                    >

                    {
                        output.status
                        ||
                        "UNKNOWN"
                    }


                    </strong>


                </p>









                <p>

                    <span>
                        Model
                    </span>


                    <strong>
                        {
                            output.model
                            ||
                            "N/A"
                        }
                    </strong>


                </p>









                <p>

                    <span>
                        Latency
                    </span>


                    <strong>
                        {
                        Number(
                            trace.latency_ms || 0
                        )
                        .toFixed(2)

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
                        trace.timestamp
                        ?
                        new Date(
                            trace.timestamp
                        )
                        .toLocaleString()

                        :

                        "N/A"

                    }


                    </strong>


                </p>






            </div>









            {/* Execution Pipeline */}


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








        </div>


    );


}