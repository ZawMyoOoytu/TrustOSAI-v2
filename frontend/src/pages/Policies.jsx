import "./Policies.css";



export default function Policies(){



const policies=[


{

name:"Minimum Trust Score",

value:"60",

status:"ACTIVE"

},



{

name:"High Risk Blocking",

value:"Risk > 80",

status:"ACTIVE"

},



{

name:"Human Review Threshold",

value:"Trust < 70",

status:"ACTIVE"

},



{

name:"Token Budget Control",

value:"5000 tokens",

status:"ACTIVE"

}



];





return (



<div className="policies-page">






<div className="page-title">


<h1>

⚖ Governance Policies

</h1>


<p>

AI safety enforcement rules

</p>


</div>







<div className="policy-grid">



{


policies.map(
(policy,index)=>(


<div

className="policy-card"

key={index}

>


<h2>

{policy.name}

</h2>



<div className="policy-value">

{policy.value}

</div>



<span>

🟢 {policy.status}

</span>



</div>



)

)


}



</div>







</div>



);



}