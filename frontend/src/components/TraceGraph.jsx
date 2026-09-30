export default function TraceGraph(){


const nodes=[

"Request",

"Policy",

"Trust",

"Risk",

"Decision",

"Agent",

"Audit"

];


return(

<div className="trace-graph">


{

nodes.map((node,index)=>(


<div

key={node}

className="trace-node"


>


<div>

✓

</div>


<span>

{node}

</span>



{

index !== nodes.length-1 &&

<div className="arrow">

↓

</div>


}



</div>


))


}


</div>


);


}