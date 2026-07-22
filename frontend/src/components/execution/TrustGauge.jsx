export default function TrustGauge({
    score
}){


const value =
Number(score || 0);



let level="LOW";


if(value >=80){

    level="HIGH";

}
else if(value >=60){

    level="MEDIUM";

}



return (

<div className="execution-card">


<h2>
🛡 Trust Score
</h2>



<div className="trust-circle">


<div className="trust-number">

{value.toFixed(0)}

</div>


<p>

Trust Level:

<strong>

{level}

</strong>

</p>


</div>



</div>


);


}