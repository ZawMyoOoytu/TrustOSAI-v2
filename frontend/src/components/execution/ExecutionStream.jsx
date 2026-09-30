import useExecutionStream
from "../../hooks/useExecutionStream";



import StreamEvent
from "./StreamEvent";



import "../../styles/ExecutionStream.css";






export default function ExecutionStream({
executionId
}){


const {

events,

status

}=useExecutionStream(
    executionId
);






return (


<div className="stream-card">



<h2>

⚡ Live Execution Stream

</h2>





<div className="stream-status">


Status:

<strong>

{
status
}

</strong>


</div>








{

events.length===0

?

<p>

Waiting for execution events...

</p>


:

events.map(
(event,index)=>(


<StreamEvent

key={index}

event={event}

/>


)

)



}



</div>


);


}