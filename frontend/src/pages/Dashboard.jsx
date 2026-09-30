import "./Dashboard.css";
import {
    useEffect,
    useState
}
from "react";


import {
    getStats
}
from "../api/client";



export default function Dashboard(){


const [stats,setStats] = useState({

    total_executions:0,

    allowed:0,

    blocked:0,

    review:0,

    success_rate:0,

    average_trust_score:0,

    runtime_ms:0

});



const [loading,setLoading] =
useState(true);



const [error,setError] =
useState(null);



const [lastUpdate,setLastUpdate] =
useState(null);





// =====================================
// LOAD DATA
// =====================================


async function loadDashboard(){


try{


setLoading(true);



const data =
await getStats();



setStats({

    total_executions:
    data.total_executions ?? 0,


    allowed:
    data.allowed ?? 0,


    blocked:
    data.blocked ?? 0,


    review:
    data.review ?? 0,


    success_rate:
    data.success_rate ?? 0,


    average_trust_score:
    data.average_trust_score ?? 0,


    runtime_ms:
    data.runtime_ms ?? 0


});



setLastUpdate(
    new Date()
);



setError(null);



}

catch(err){


console.error(err);


setError(
    err.message
);


}


finally{


setLoading(false);


}



}






// =====================================
// AUTO REFRESH
// =====================================


useEffect(()=>{


loadDashboard();



const interval =

setInterval(

loadDashboard,

30000

);



return ()=>clearInterval(interval);



},[]);






if(loading){


return (

<div className="dashboard">

<h1>
⚡ TrustOSAI Developer Control Plane
</h1>


<p>
Loading governance intelligence...
</p>


</div>


);


}






if(error){


return (

<div className="dashboard">


<h1>
⚡ TrustOSAI Developer Control Plane
</h1>


<p>
❌ {error}
</p>


</div>


);


}







return (



<div className="dashboard">



{/* HEADER */}

<div className="dashboard-header">


<h1>
⚡ TrustOSAI Developer Control Plane
</h1>


<p>

AI Governance Dashboard

</p>



{
lastUpdate &&

<small>

Last Sync:

{" "}

{
lastUpdate.toLocaleTimeString()
}

</small>

}



</div>









{/* KPI */}

<div className="cards">



<StatCard

title="Total Executions"

value={
stats.total_executions
}

/>



<StatCard

title="Allowed"

value={
stats.allowed
}

/>



<StatCard

title="Blocked"

value={
stats.blocked
}

/>



<StatCard

title="Success Rate"

value={
`${stats.success_rate}%`
}

/>


</div>









<div className="dashboard-grid">







{/* TRUST */}

<section className="panel">


<h2>

🧠 Trust Intelligence

</h2>



<div className="trust-circle">


{

Math.round(
stats.average_trust_score
)

}


</div>



<p>

Average Trust Score

</p>



<TrustStatus

score={
stats.average_trust_score
}

/>



</section>









{/* GOVERNANCE */}


<section className="panel">


<h2>

⚖ Governance Decision

</h2>



<DecisionBar

label="APPROVED"

value={
stats.allowed
}

total={
stats.total_executions
}

/>




<DecisionBar

label="REVIEW"

value={
stats.review
}

total={
stats.total_executions
}

/>




<DecisionBar

label="BLOCK"

value={
stats.blocked
}

total={
stats.total_executions
}

/>



</section>









{/* RUNTIME */}


<section className="panel">


<h2>

🖥 Runtime Health

</h2>



<HealthItem

name="API Gateway"

/>



<HealthItem

name="Database"

/>



<HealthItem

name="Policy Engine"

/>



<HealthItem

name="Memory Engine"

/>



<div className="runtime">

⚡ Runtime

{" "}

{
stats.runtime_ms || 0
}

ms

</div>



</section>






</div>



</div>



);


}









// =====================================
// CARD
// =====================================


function StatCard({

title,

value

}){


return (

<div className="card">


<h3>

{title}

</h3>


<h1>

{value}

</h1>


</div>


);


}









// =====================================
// TRUST STATUS
// =====================================


function TrustStatus({

score

}){


let status="CRITICAL";



if(score>=80)

status="EXCELLENT";


else if(score>=60)

status="GOOD";


else if(score>=40)

status="MEDIUM";




return (

<div>


Status:

{" "}

<strong>

{status}

</strong>


</div>


);



}









// =====================================
// DECISION BAR
// =====================================


function DecisionBar({

label,

value,

total

}){


const percent =

total

?

Math.round(

(value/total)*100

)

:

0;




return (

<div className="decision-box">


<div>


<span>

{label}

</span>


<strong>

{value}

</strong>


</div>



<div className="progress">


<div

className="progress-fill"

style={{

width:`${percent}%`

}}


/>


</div>



<small>

{percent}%

</small>



</div>


);


}









// =====================================
// HEALTH
// =====================================


function HealthItem({

name

}){


return (

<div className="health-item">

🟢

{" "}

{name}

{" "}

ONLINE


</div>


);


}