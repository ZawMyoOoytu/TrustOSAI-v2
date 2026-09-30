import {

useEffect,

useState

}

from "react";



export default function Analytics(){



const [data,setData]=useState(null);




useEffect(()=>{


fetch(

"http://127.0.0.1:8000/api/analytics"

)

.then(

r=>r.json()

)

.then(

setData

);



},[]);





if(!data)

return <h2>

Loading Analytics...

</h2>;




return (

<div className="dashboard">


<h1>

📊 TrustOSAI Analytics

</h1>



<div className="cards">



<div className="card">

<h3>

Average Trust

</h3>

<h1>

{data.average_trust}

</h1>

</div>



<div className="card">

<h3>

Average Latency

</h3>

<h1>

{data.average_latency}

ms

</h1>

</div>




<div className="card">

<h3>

Quality Score

</h3>

<h1>

{data.quality}

</h1>

</div>




</div>



</div>

);


}