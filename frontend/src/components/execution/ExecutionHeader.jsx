export default function ExecutionHeader({

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
    // NORMALIZE
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
    // DATA MAPPING
    // =====================================


    const executionId =


        execution.execution_id

        ??

        execution.id

        ??

        replayResult.execution_id

        ??

        "N/A";








    const executionType =


        execution.execution_type

        ??

        replayResult.execution_type

        ??

        "NORMAL";








    const decision =


        execution.decision

        ??

        replayResult.decision

        ??

        output.decision

        ??

        "UNKNOWN";








    const created =


        execution.created_at

        ??

        execution.timestamp

        ??

        output.timestamp

        ??

        "Replay Execution";








    const model =


        execution.model

        ??

        replayResult.model

        ??

        output.model

        ??

        "unknown";








    const agent =


        execution.agent

        ??

        replayResult.agent

        ??

        "unknown";









    return (



        <div className="execution-header">







            <h1>

                ⚡ Execution Trace #{executionId}

            </h1>









            <p>

                Enterprise AI Governance Runtime Trace

            </p>









            <div className="header-meta">





                <p>

                    <span>

                        Type:

                    </span>


                    <strong>

                        {executionType}

                    </strong>


                </p>







                <p>

                    <span>

                        Created:

                    </span>


                    <strong>

                        {

                            typeof created === "string"

                            ?

                            created

                            :

                            new Date(created)

                            .toLocaleString()

                        }

                    </strong>


                </p>







                <p>

                    <span>

                        Decision:

                    </span>


                    <strong>

                        {decision}

                    </strong>


                </p>







                <p>

                    <span>

                        Model:

                    </span>


                    <strong>

                        {model}

                    </strong>


                </p>







                <p>

                    <span>

                        Agent:

                    </span>


                    <strong>

                        {agent}

                    </strong>


                </p>







            </div>







        </div>



    );


}