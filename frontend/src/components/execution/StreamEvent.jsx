export default function StreamEvent({
event
}){


return (


<div className="stream-event">



<div className="event-icon">


✓


</div>




<div className="event-content">


<h4>

{
event.stage
}


</h4>



<p>

{
event.message
}

</p>



<span>

{
event.timestamp
}

</span>


</div>





</div>


);


}