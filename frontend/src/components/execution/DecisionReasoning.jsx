export default function DecisionReasoning({
    data
}) {


    if(!data){
        return null;
    }



    return (

        <div className="decision-reasoning">


            <h2>
                🧠 Governance Decision Reasoning
            </h2>




            <div className="decision-box">


                <span>
                    Decision:
                </span>


                <strong>
                    {data.decision}
                </strong>


            </div>





            <div className="reasoning-section">


                <h3>
                    Why?
                </h3>



                <ul>

                    {
                        data.reasoning?.map(
                            (item,index)=>(

                                <li key={index}>
                                    ✓ {item}
                                </li>

                            )
                        )
                    }

                </ul>


            </div>







            <div className="action-section">


                <h3>
                    Actions
                </h3>



                <ul>

                    {
                        data.actions?.map(
                            (item,index)=>(

                                <li key={index}>
                                    ▶ {item}
                                </li>

                            )
                        )
                    }

                </ul>


            </div>








            <div className="confidence">


                Confidence:

                <strong>
                    {
                        Math.round(
                            data.confidence * 100
                        )
                    }%
                </strong>


            </div>



        </div>

    );

}