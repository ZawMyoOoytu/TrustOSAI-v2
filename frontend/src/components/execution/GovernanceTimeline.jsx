export default function GovernanceTimeline({

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
    // NORMALIZE DATA
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
    // VALUES
    // =====================================


    const decision =


        execution.decision

        ??

        output.decision

        ??

        replayResult.decision

        ??

        "UNKNOWN";








    const status =


        execution.status

        ??

        output.status

        ??

        "COMPLETED";








    const executionType =


        execution.execution_type

        ??

        replayResult.execution_type

        ??

        "NORMAL";









    const completed =


        status === "COMPLETED"

        ||

        status === "SUCCESS";









    // =====================================
    // TIMELINE STEPS
    // =====================================


    const steps = [



        {

            title:
            "Request Received",

            done:true

        },




        {

            title:
            "Policy Evaluation Completed",

            done:true

        },




        {

            title:
            "Trust Score Generated",

            done:true

        },




        {

            title:
            `Decision: ${decision}`,

            done:

                decision !== "UNKNOWN"

        },





        {

            title:
            "Agent Execution Completed",

            done:

                completed

        },





        {

            title:
            "Audit Stored",

            done:true

        }


    ];









    return (



        <div className="timeline">







            <h2>

                🧠 Governance Timeline

            </h2>








            <div className="timeline-type">


                Mode:

                {" "}


                <strong>

                    {executionType}

                </strong>


            </div>









            {

                steps.map(

                    (step,index)=>(



                        <div

                            className={

                                `timeline-item ${
                                    step.done
                                    ?
                                    "completed"
                                    :
                                    "pending"
                                }`

                            }


                            key={index}

                        >




                            <span>


                                {

                                    step.done

                                    ?

                                    "✓"

                                    :

                                    "○"

                                }


                            </span>





                            <p>


                                {step.title}


                            </p>






                        </div>



                    )

                )

            }








        </div>



    );


}