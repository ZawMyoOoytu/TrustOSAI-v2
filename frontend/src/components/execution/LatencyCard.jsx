export default function LatencyCard({
latency
}){


let status="FAST";


if(latency>500){

status="SLOW";

}



return (

<div className="execution-card">


<h2>
⚡ Latency
</h2>


<h1>

{Number(latency).toFixed(2)}

ms

</h1>



<p>

Status:

<strong>

{status}

</strong>

</p>



</div>


);


}