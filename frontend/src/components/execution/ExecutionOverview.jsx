export default function ExecutionOverview({

    execution

}) {


    if(!execution){

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
    // NORMALIZE RESULT
    // =====================================


    const result =


        parse(

            execution.result

        );








    const replayResult =


        execution.replay_result

        ??

        {};








    const output =


        result.result

        ??

        result

        ??

        replayResult;









    // =====================================
    // TRUST LEVEL
    // =====================================


    function getTrustLevel(score){


        const value =


            Number(

                score ?? 0

            );




        if(value >= 80){

            return "HIGH";

        }




        if(value >= 60){

            return "MEDIUM";

        }



        return "LOW";


    }









    // =====================================
    // DECISION STYLE
    // =====================================


    function decisionClass(decision){



        switch(decision){



            case "ALLOW":

            case "APPROVED":

            case "ALLOW_WITH_MONITORING":

                return "approved";




            case "BLOCK":

                return "block";




            case "REVIEW":

                return "review";




            default:

                return "review";


        }


    }









    // =====================================
    // DATA MAPPING
    // =====================================


    const task =


        execution.task

        ??

        output.task

        ??

        replayResult.task

        ??

        "No task provided";








    const agent =


        execution.agent

        ??

        output.agent

        ??

        replayResult.agent

        ??

        "Unknown Agent";








    const trustScore =


        execution.trust_score

        ??

        output.trust_score

        ??

        replayResult.trust_score

        ??

        0;








    const riskScore =


        execution.risk_score

        ??

        output.risk_score

        ??

        replayResult.risk_score

        ??

        0;








    const decision =


        execution.decision

        ??

        output.decision

        ??

        replayResult.decision

        ??

        "UNKNOWN";








    const createdAt =


        execution.created_at

        ??

        execution.updated_at

        ??

        output.timestamp

        ??

        null;









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

                    {task}

                </strong>


            </div>









            {/* AGENT */}


            <div className="info-row">


                <span>

                    Agent

                </span>



                <strong>

                    {agent}

                </strong>


            </div>









            {/* TRUST SCORE */}


            <div className="info-row">


                <span>

                    Trust Score

                </span>



                <strong>


                    {

                        Number(

                            trustScore

                        )

                        .toFixed(2)

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

                            trustScore

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

                        Number(riskScore) > 50

                        ?

                        "risk-high"

                        :

                        "risk-low"

                    }

                >


                    {

                        Number(

                            riskScore

                        )

                        .toFixed(2)

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

                        `decision-badge ${
                            decisionClass(
                                decision
                            )
                        }`

                    }

                >


                    {decision}


                </strong>


            </div>









            {/* CREATED */}


            <div className="info-row">


                <span>

                    Created

                </span>



                <strong>


                {


                    createdAt


                    ?


                    new Date(

                        createdAt

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