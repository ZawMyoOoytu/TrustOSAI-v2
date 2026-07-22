export default function ExecutionComparison({
    original,
    replay
}) {


    if(!original || !replay){
        return null;
    }



    function parse(value){

        if(!value){
            return {};
        }


        if(typeof value==="object"){
            return value;
        }


        try{
            return JSON.parse(value);
        }
        catch{
            return {};
        }

    }




    const originalOutput =
        parse(original.result);



    const replayOutput =
        parse(replay.result);





    const rows=[

        {
            metric:"Execution ID",
            original:
                original.execution_id ?? "-",
            replay:
                replay.execution_id ?? "-"
        },


        {
            metric:"Model",
            original:
                originalOutput.model
                ??
                original.model
                ??
                "N/A",

            replay:
                replay.model
                ??
                replayOutput.model
                ??
                "N/A"
        },


        {
            metric:"Agent",
            original:
                original.agent
                ??
                "N/A",

            replay:
                replay.agent
                ??
                "N/A"
        },


        {
            metric:"Trust Score",
            original:
                Number(
                    original.trust_score ?? 0
                ).toFixed(2),

            replay:
                Number(
                    replay.trust_score ?? 0
                ).toFixed(2)
        },


        {
            metric:"Decision",
            original:
                original.decision,

            replay:
                replay.decision
        },


        {
            metric:"Risk Score",
            original:
                original.risk_score ?? 0,

            replay:
                replay.risk_score ?? 0
        },


        {
            metric:"Quality Score",
            original:

                originalOutput.quality_score_qt
                ??
                originalOutput.trace?.output?.quality_score
                ??
                original.telemetry?.quality_score
                ??
                0,


            replay:

                replay.quality_score
                ??
                replayOutput.quality_score_qt
                ??
                replay.telemetry?.quality_score
                ??
                0
        },


        {
            metric:"Runtime",

            original:

                originalOutput.latency_ms
                ??
                original.runtime_ms
                ??
                0,

            replay:

                replay.runtime_ms
                ??
                replay.telemetry?.latency_ms
                ??
                0
        }


    ];





    return (

        <div className="comparison-card">


            <h2>
                🔁 Execution Comparison
            </h2>



            <table>


                <thead>

                    <tr>

                        <th>
                            Metric
                        </th>

                        <th>
                            Original
                        </th>

                        <th>
                            Replay
                        </th>


                    </tr>

                </thead>



                <tbody>


                {
                    rows.map(
                        (row,index)=>(

                        <tr key={index}>

                            <td>
                                {row.metric}
                            </td>


                            <td>
                                {String(row.original)}
                            </td>


                            <td>
                                {String(row.replay)}
                            </td>


                        </tr>

                        )
                    )
                }


                </tbody>


            </table>



        </div>

    );

}