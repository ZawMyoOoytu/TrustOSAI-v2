import {
    useEffect,
    useState
}
from "react";



export default function useExecutionStream(
    executionId
){


const [
    events,
    setEvents
]=useState([]);



const [
    status,
    setStatus
]=useState(
    "CONNECTING"
);





useEffect(()=>{



if(!executionId)
return;




const socket =
new WebSocket(

`ws://localhost:8000/ws/execution/${executionId}`

);





socket.onopen=()=>{


setStatus(
    "CONNECTED"
);


};







socket.onmessage=(message)=>{


const data =
JSON.parse(
    message.data
);




setEvents(prev=>[

...prev,

data

]);



};







socket.onerror=()=>{


setStatus(
    "ERROR"
);


};







socket.onclose=()=>{


setStatus(
    "CLOSED"
);


};






return ()=>{


socket.close();


};



},[executionId]);





return {

events,

status


};



}