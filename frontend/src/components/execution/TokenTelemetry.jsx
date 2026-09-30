export default function TokenTelemetry({

    data

}){


    if(!data){

        return null;

    }





    // =====================================
    // Normalize Token Structure
    // =====================================


    const tokens =


        data.token_telemetry

        ??

        data.result?.token_telemetry

        ??

        data.result?.result?.token_telemetry

        ??

        data;









    return (

        <div className="trace-card">



            <h2>

                📊 Token Telemetry

            </h2>








            <div className="telemetry-grid">





                <div>


                    <span>
                        Prompt Tokens
                    </span>



                    <strong>

                    {

                        tokens.prompt_tokens

                        ??

                        0

                    }

                    </strong>


                </div>








                <div>


                    <span>
                        Completion Tokens
                    </span>



                    <strong>

                    {

                        tokens.completion_tokens

                        ??

                        0

                    }

                    </strong>


                </div>








                <div>


                    <span>
                        Total Tokens
                    </span>



                    <strong>

                    {

                        tokens.total_tokens

                        ??

                        (

                            (tokens.prompt_tokens ?? 0)

                            +

                            (tokens.completion_tokens ?? 0)

                        )

                    }


                    </strong>


                </div>









                {

                    tokens.context_window &&


                    <div>


                        <span>
                            Context Window
                        </span>


                        <strong>

                            {
                                tokens.context_window
                            }

                        </strong>


                    </div>


                }





            </div>






        </div>


    );


}