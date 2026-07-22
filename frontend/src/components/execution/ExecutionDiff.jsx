export default function ExecutionDiff({

    original,

    replay

}){


    if(!original || !replay){

        return null;

    }




    const trustChange =

        (
            replay.trust_score ?? 0
        )

        -

        (
            original.trust_score ?? 0
        );





    const qualityChange =


        (
            replay.telemetry?.quality_score
            ??
            replay.result?.quality_score_qt
            ??
            0
        )

        -

        (
            original.telemetry?.quality_score
            ??
            0
        );






    const decisionChanged =

        original.decision !== replay.decision;






    return (

        <div className="execution-diff-card">


            <h3>

                📊 Execution Difference Analysis

            </h3>





            <div className="diff-row">


                <span>

                    Trust Score Change

                </span>


                <strong>

                {

                    trustChange >=0

                    ?

                    `+${trustChange.toFixed(2)} ↑`

                    :

                    `${trustChange.toFixed(2)} ↓`

                }

                </strong>


            </div>







            <div className="diff-row">


                <span>

                    Decision Change

                </span>



                <strong>

                {

                    decisionChanged

                    ?

                    `${original.decision} → ${replay.decision}`

                    :

                    "No Change"

                }

                </strong>



            </div>









            <div className="diff-row">


                <span>

                    Quality Change

                </span>



                <strong>


                {

                    qualityChange >=0

                    ?

                    `+${qualityChange.toFixed(2)}`

                    :

                    qualityChange.toFixed(2)

                }


                </strong>


            </div>









            <div className="diff-row">


                <span>

                    Model Routing

                </span>


                <strong>


                {

                    `${original.model ?? original.agent}`

                }


                {" → "}


                {

                    `${replay.model ?? replay.agent}`

                }


                </strong>


            </div>







            {


            trustChange < 0 &&


            <div className="diff-warning">


                ⚠ Replay trust decreased


            </div>


            }






            {


            decisionChanged &&


            <div className="diff-success">


                🔄 Governance decision changed after replay


            </div>


            }



        </div>

    );


}