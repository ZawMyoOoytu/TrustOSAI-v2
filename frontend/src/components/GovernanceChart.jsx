import {
 PieChart,
 Pie,
 Cell,
 Tooltip
} from "recharts";


import "./GovernanceChart.css";



export default function GovernanceChart({

approved=0,
review=0,
blocked=0

}){


const data=[

{
name:"APPROVED",
value:approved
},

{
name:"REVIEW",
value:review
},

{
name:"BLOCK",
value:blocked
}

];



return (

<div className="governance-card">


<h3>
⚖ Governance Decision
</h3>



<PieChart
width={300}
height={250}
>


<Pie

data={data}

dataKey="value"

cx="50%"

cy="50%"

outerRadius={90}

label

>


{
data.map(
(entry,index)=>(

<Cell
key={index}
/>

)
)
}



</Pie>


<Tooltip/>


</PieChart>



</div>

)

}