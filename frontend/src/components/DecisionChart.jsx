export default function DecisionChart({

    approved,
    review,
    blocked

}){


    const total =
    approved + review + blocked;



    function percent(value){

        if(total===0)
            return 0;


        return Math.round(
            (value / total) * 100
        );

    }



    return (

        <div className="panel">


            <h2>
                ⚖ Governance Decision Distribution
            </h2>



            <ChartRow

                label="APPROVED"

                value={approved}

                percent={
                    percent(approved)
                }

            />



            <ChartRow

                label="REVIEW"

                value={review}

                percent={
                    percent(review)
                }

            />



            <ChartRow

                label="BLOCK"

                value={blocked}

                percent={
                    percent(blocked)
                }

            />


        </div>

    );

}





function ChartRow({

    label,

    value,

    percent

}){


    return (

        <div className="chart-row">


            <div className="chart-title">


                <span>
                    {label}
                </span>


                <strong>
                    {value}
                </strong>


            </div>



            <div className="bar">


                <div

                className="fill"

                style={{

                    width:
                    `${percent}%`

                }}

                >

                </div>


            </div>



            <small>

                {percent}%

            </small>



        </div>

    );

}