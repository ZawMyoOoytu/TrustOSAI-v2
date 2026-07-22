export default function MetadataPanel({
execution
}){


return (

<div className="metadata-panel">


<h3>

📌 Execution Metadata

</h3>


<p>

Execution ID:

{execution.execution_id}

</p>


<p>

Agent:

{execution.agent}

</p>


<p>

Created:

{execution.created_at}

</p>


<p>

Runtime Engine:

ExecutionEngine

</p>


</div>


);


}