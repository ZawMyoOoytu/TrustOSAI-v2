export default function TrustExplanation({
    data
}) {


    if(!data){
        return null;
    }


    return (

        <div className="trust-explanation">


            <h2>
                🔍 Trust Explanation
            </h2>



            <div className="trust-recommendation">

                <strong>
                    Recommendation:
                </strong>

                <p>
                    {data.recommendation}
                </p>

            </div>




            <div className="trust-factors">


                {
                    data.factors?.map(
                        (factor,index)=>(

                        <div
                            className="factor-card"
                            key={index}
                        >


                            <div className="factor-header">

                                <span>
                                    {factor.name}
                                </span>


                                <span>
                                    {
                                      Math.round(
                                        factor.score
                                      )
                                    }%
                                </span>

                            </div>



                            <div className="progress">

                                <div

                                className="progress-bar"

                                style={{
                                    width:
                                    `${factor.score}%`
                                }}

                                />

                            </div>



                            <p>
                                {factor.description}
                            </p>



                        </div>


                        )
                    )
                }


            </div>


        </div>

    );

}