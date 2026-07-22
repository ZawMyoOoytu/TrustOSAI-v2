export default function TokenTelemetry({
    data
}){


if(!data){

return null;

}



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
data.prompt_tokens ?? 0
}
</strong>


</div>





<div>

<span>
Completion Tokens
</span>

<strong>
{
data.completion_tokens ?? 0
}
</strong>


</div>



</div>



</div>


);


}