export default function TrustGauge({

    score

}){

    let status="CRITICAL";

    if(score>=80){

        status="EXCELLENT";

    }

    else if(score>=60){

        status="GOOD";

    }

    else if(score>=40){

        status="MEDIUM";

    }

    return(

        <div className="trust-gauge">

            <div className="trust-score">

                {

                    Math.round(score)

                }

            </div>

            <div>

                Average Trust Score

            </div>

            <div className="trust-status">

                {status}

            </div>

        </div>

    );

}