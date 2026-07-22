export default function AgentOutputViewer({

    output

}){


    if(!output){

        return null;

    }



    // ============================
    // Copy JSON
    // ============================


    function copyJSON(){


        navigator.clipboard.writeText(

            JSON.stringify(
                output,
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









            {/* AI RESPONSE */}


            <div className="response-box">


                <h3>
                    AI Response
                </h3>



                <p>

                {
                    output.response
                    ||
                    "No response generated"
                }

                </p>


            </div>









            {/* JSON TRACE */}


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

    output,

    null,

    2

)

}


                </pre>



            </details>





        </div>


    );


}