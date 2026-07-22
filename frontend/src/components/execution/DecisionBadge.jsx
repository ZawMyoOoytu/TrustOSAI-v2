export default function DecisionBadge({
    decision
}){


let style =
"";


if(decision==="APPROVED" ||
   decision==="ALLOW")
{

style="approved";

}


else if(decision==="REVIEW")
{

style="review";

}


else if(decision==="BLOCK")
{

style="blocked";

}



return (

<span

className={`decision-badge ${style}`}

>

{decision}

</span>


);


}