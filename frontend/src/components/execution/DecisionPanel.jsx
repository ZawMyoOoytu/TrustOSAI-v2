export default function DecisionPanel({

    execution

}){


if(!execution){

    return null;

}




function getDecisionInfo(){


const decision =
execution.decision;



switch(decision){


case "APPROVED":

return {

title:"APPROVED",

color:"approved",

reason:
"Execution passed governance policy validation.",

action:
"Execute normally"

};



case "ALLOW_WITH_MONITORING":

return {

title:"ALLOW WITH MONITORING",

color:"monitor",

reason:
"Trust score acceptable. Continuous agent monitoring enabled.",

action:
"Execute with telemetry tracking"

};



case "BLOCK":

return {

title:"BLOCKED",

color:"blocked",

reason:
"Risk threshold exceeded. Execution denied.",

action:
"Stop execution"

};



default:

return {

title:decision || "UNKNOWN",

color:"unknown",

reason:
"No governance explanation available.",

action:
"Manual review required"

};


}


}



const info =
getDecisionInfo();




return (

<div className="execution-card decision-panel">


<h2>
⚖ Governance Decision
</h2>




<div

className={

`decision-large ${info.color}`

}

>

{info.title}


</div>





<div className="decision-row">


<span>
Reason
</span>


<strong>
{info.reason}
</strong>


</div>





<div className="decision-row">


<span>
Recommended Action
</span>


<strong>
{info.action}
</strong>


</div>





<div className="decision-row">


<span>
Trust Score
</span>


<strong>
{
Number(
execution.trust_score
)
.toFixed(2)
}
</strong>


</div>





<div className="decision-row">


<span>
Risk Score
</span>


<strong>
{
execution.risk_score ?? 0
}
</strong>


</div>



</div>


);


}