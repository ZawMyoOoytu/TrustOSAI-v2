export default function DecisionBar({

    label,

    value,

    total

}){

    const percent=

    total>0

    ?

    Math.round(

        value/total*100

    )

    :

    0;

    return(

        <div className="decision-row">

            <div className="decision-header">

                <span>

                    {label}

                </span>

                <strong>

                    {value}

                </strong>

            </div>

            <div className="progress">

                <div

                    className="progress-fill"

                    style={{

                        width:`${percent}%`

                    }}

                />

            </div>

            <small>

                {percent}%

            </small>

        </div>

    );

}