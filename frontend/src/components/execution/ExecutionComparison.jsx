export default function ExecutionComparison({

    original,

    replay

}) {



    if(!original || !replay){

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


    const originalResult =

        parse(

            original.result

        );





    const replayResult =


        parse(

            replay.result

        );








    const originalTrace =


        originalResult.trace

        ??

        {};





    const replayTrace =


        replayResult.trace

        ??

        {};








    // =====================================
    // METRIC HELPERS
    // =====================================


    function score(value){


        return Number(

            value ?? 0

        )

        .toFixed(2);


    }






    function runtime(data,result){


        return (

            data.runtime_ms

            ??

            data.latency_ms

            ??

            result.runtime_ms

            ??

            result.latency_ms

            ??

            data.telemetry?.latency_ms

            ??

            0

        );


    }








    function quality(data,result){


        return (

            data.quality_score

            ??

            result.quality_score

            ??

            result.quality_score_qt

            ??

            data.telemetry?.quality_score

            ??

            0

        );


    }









    function tokens(data,result){


        const token =


            data.token_telemetry

            ??

            result.token_telemetry

            ??

            {};



        return (

            token.total_tokens

            ??

            (

                (token.prompt_tokens ?? 0)

                +

                (token.completion_tokens ?? 0)

            )

        );


    }









    // =====================================
    // COMPARISON ROWS
    // =====================================


    const rows = [



        {

            metric:"Execution ID",

            original:

                original.execution_id

                ??

                original.id

                ??

                "-",


            replay:

                replay.execution_id

                ??

                replay.id

                ??

                "-"

        },






        {

            metric:"Execution Type",

            original:

                original.execution_type

                ??

                "NORMAL",


            replay:

                replay.execution_type

                ??

                "REPLAY"

        },







        {

            metric:"Model",

            original:


                original.model

                ??

                originalResult.model

                ??

                originalTrace.output?.model

                ??

                "unknown",




            replay:


                replay.model

                ??

                replayResult.model

                ??

                replayTrace.output?.model

                ??

                "unknown"

        },








        {

            metric:"Agent",

            original:


                original.agent

                ??

                "unknown",




            replay:


                replay.agent

                ??

                "unknown"

        },









        {

            metric:"Provider",

            original:


                original.provider

                ??

                "local",




            replay:


                replay.provider

                ??

                "local"

        },










        {

            metric:"Trust Score",

            original:


                score(

                    original.trust_score

                ),




            replay:


                score(

                    replay.trust_score

                )

        },









        {

            metric:"Decision",

            original:


                original.decision

                ??

                "UNKNOWN",




            replay:


                replay.decision

                ??

                "UNKNOWN"

        },









        {

            metric:"Risk Score",

            original:


                score(

                    original.risk_score

                ),




            replay:


                score(

                    replay.risk_score

                )

        },









        {

            metric:"Quality Score",

            original:


                score(

                    quality(

                        original,

                        originalResult

                    )

                ),





            replay:


                score(

                    quality(

                        replay,

                        replayResult

                    )

                )

        },









        {

            metric:"Runtime (ms)",

            original:


                runtime(

                    original,

                    originalResult

                ),





            replay:


                runtime(

                    replay,

                    replayResult

                )

        },









        {

            metric:"Total Tokens",

            original:


                tokens(

                    original,

                    originalResult

                ),





            replay:


                tokens(

                    replay,

                    replayResult

                )

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


                            <tr

                                key={index}

                            >



                                <td>

                                    {row.metric}

                                </td>





                                <td>

                                    {

                                        String(

                                            row.original

                                        )

                                    }

                                </td>





                                <td>

                                    {

                                        String(

                                            row.replay

                                        )

                                    }

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