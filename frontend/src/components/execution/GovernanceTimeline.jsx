export default function GovernanceTimeline({
    execution
}){


const steps=[

    "Request Received",

    "Policy Evaluation Completed",

    "Trust Score Generated",

    `Decision: ${execution.decision}`,

    "Agent Execution Completed",

    "Audit Stored"

];



return (

<div className="timeline">


<h2>
🧠 Governance Timeline
</h2>



{
steps.map(
(step,index)=>(


<div

className="timeline-item"

key={index}

>


<span>

✓

</span>


{" "}


{step}



</div>


)

)

}



</div>


);


}