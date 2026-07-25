export default function AgentOutputViewer({

    output

}) {


    if(!output){

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

            return {

                response:value

            };

        }


    }









    // =====================================
    // NORMALIZE OUTPUT
    // =====================================


    const parsedOutput =


        parse(

            output

        );








    const executionResult =


        parsedOutput.result

        ??

        parsedOutput;








    const finalOutput =


        executionResult.result

        ??

        executionResult;









    // =====================================
    // DATA EXTRACTION
    // =====================================


    const response =


        finalOutput.response

        ??

        finalOutput.output

        ??

        finalOutput.message

        ??

        finalOutput.result

        ??

        "No response generated";








    const model =


        finalOutput.model

        ??

        parsedOutput.model

        ??

        "unknown";








    const status =


        finalOutput.status

        ??

        parsedOutput.status

        ??

        "UNKNOWN";








    const decision =


        finalOutput.decision

        ??

        parsedOutput.decision

        ??

        "UNKNOWN";









    const trace =


        finalOutput.trace

        ??

        {};









    // =====================================
    // COPY JSON
    // =====================================


    function copyJSON(){


        navigator.clipboard.writeText(


            JSON.stringify(

                finalOutput,

                null,

                2

            )


        );


        alert(

            "JSON copied successfully"

        );


    }









    return (



        <div className="execution-card">







            <div className="output-header">





                <h2>

                    🤖 Agent Output

                </h2>







                <button


                    className="action-btn copy"


                    onClick={copyJSON}


                >

                    📋 Copy JSON


                </button>






            </div>













            {/* ============================
                EXECUTION SUMMARY
            ============================= */}



            <div className="output-summary">






                <div>


                    <span>

                        Model

                    </span>



                    <strong>

                        {model}

                    </strong>



                </div>







                <div>


                    <span>

                        Status

                    </span>



                    <strong>

                        {status}

                    </strong>



                </div>







                <div>


                    <span>

                        Decision

                    </span>



                    <strong>

                        {decision}

                    </strong>



                </div>






            </div>













            {/* ============================
                AI RESPONSE
            ============================= */}



            <div className="response-box">





                <h3>

                    AI Response

                </h3>







                <p>


                    {

                        typeof response === "object"

                        ?

                        JSON.stringify(

                            response,

                            null,

                            2

                        )

                        :

                        response


                    }



                </p>





            </div>













            {/* ============================
                TRACE INFO
            ============================= */}



            {

                Object.keys(trace).length > 0 &&



                <details

                    className="trace-container"

                >



                    <summary>

                        🔍 Runtime Trace

                    </summary>




                    <pre

                        className="json-viewer"

                    >


                        {

                            JSON.stringify(

                                trace,

                                null,

                                2

                            )

                        }


                    </pre>




                </details>


            }












            {/* ============================
                FULL JSON
            ============================= */}



            <details


                open


                className="json-container"


            >





                <summary>


                    🔍 Full Execution JSON


                </summary>







                <pre


                    className="json-viewer"


                >



{

JSON.stringify(

    finalOutput,

    null,

    2

)

}



                </pre>







            </details>








        </div>



    );


}