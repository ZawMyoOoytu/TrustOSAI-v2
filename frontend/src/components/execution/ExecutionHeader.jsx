export default function ExecutionHeader({
    execution
}) {


    if (!execution) {

        return null;

    }



    const executionId =
        execution.execution_id
        ||
        execution.id
        ||
        "N/A";



    const decision =
        execution.decision
        ||
        execution.replay_result?.decision
        ||
        "UNKNOWN";



    const created =
        execution.created_at
        ||
        "Replay Execution";





    return (

        <div className="execution-header">



            <h1>

                ⚡ Execution Trace #{executionId}

            </h1>





            <p>

                Enterprise AI Governance Runtime Trace

            </p>





            <p>

                Created:

                {" "}

                {created}

            </p>





            <p>

                Decision:

                {" "}

                <strong>

                    {decision}

                </strong>


            </p>



        </div>

    );


}