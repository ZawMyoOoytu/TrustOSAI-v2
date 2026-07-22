export default function ExecutionOverview({
    execution
}){


    if(!execution){

        return null;

    }



    // ===============================
    // Trust Level
    // ===============================

    function getTrustLevel(score){


        const value =
        Number(score || 0);



        if(value >= 80){

            return "HIGH";

        }


        if(value >= 60){

            return "MEDIUM";

        }


        return "LOW";


    }





    // ===============================
    // Decision Style
    // ===============================


    function decisionClass(decision){


        if(decision === "APPROVED"){

            return "approved";

        }


        if(decision === "BLOCK"){

            return "block";

        }


        return "review";


    }







    return (


        <div className="execution-card">





            <h2>
                📌 Execution Overview
            </h2>







            {/* TASK */}


            <div className="info-row">


                <span>
                    Task
                </span>



                <strong>

                {
                    execution.task
                    ||
                    "No task provided"
                }

                </strong>



            </div>








            {/* AGENT */}


            <div className="info-row">


                <span>
                    Agent
                </span>



                <strong>

                {
                    execution.agent
                    ||
                    "Unknown Agent"
                }

                </strong>



            </div>









            {/* TRUST SCORE */}


            <div className="info-row">


                <span>
                    Trust Score
                </span>



                <strong>


                {
                    execution.trust_score !== null
                    &&
                    execution.trust_score !== undefined

                    ?

                    Number(
                        execution.trust_score
                    )
                    .toFixed(2)


                    :

                    "N/A"

                }


                </strong>



            </div>








            {/* TRUST LEVEL */}


            <div className="info-row">


                <span>
                    Trust Level
                </span>



                <strong
                className="trust-label"
                >

                {
                    getTrustLevel(
                        execution.trust_score
                    )
                }


                </strong>



            </div>









            {/* RISK SCORE */}


            <div className="info-row">


                <span>
                    Risk Score
                </span>



                <strong
                className={
                    execution.risk_score > 50
                    ?
                    "risk-high"
                    :
                    "risk-low"
                }
                >

                {
                    execution.risk_score
                    ??
                    0
                }


                </strong>



            </div>









            {/* DECISION */}


            <div className="info-row">


                <span>
                    Decision
                </span>



                <strong

                className={

                    `
                    decision-badge
                    ${
                        decisionClass(
                            execution.decision
                        )
                    }
                    `

                }

                >

                {
                    execution.decision
                    ||
                    "UNKNOWN"
                }


                </strong>



            </div>









            {/* CREATED TIME */}


            <div className="info-row">


                <span>
                    Created
                </span>



                <strong>


                {

                    execution.created_at


                    ?


                    new Date(
                        execution.created_at
                    )
                    .toLocaleString()



                    :


                    "N/A"

                }



                </strong>



            </div>







        </div>


    );


}