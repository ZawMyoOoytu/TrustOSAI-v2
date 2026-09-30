export default function TracePanel({
data
}){


return (

<div className="trace-panel">


<h3>

🔍 Runtime Trace

</h3>


<p>

Engine:

{data.engine}

</p>


<p>

Status:

{data.output.status}

</p>


<p>

Model:

{data.output.model}

</p>



</div>


);


}