import {useState} from "react";


export default function JsonViewer({

data

}){


const [copied,setCopied]=useState(false);



function copyJSON(){


navigator.clipboard.writeText(

JSON.stringify(
data,
null,
4
)

);


setCopied(true);


setTimeout(()=>{

setCopied(false);

},2000);


}



return (

<div className="json-container">


<div className="json-header">


<h3>

📄 Agent Output

</h3>


<button

onClick={copyJSON}

>

{

copied

?

"Copied ✓"

:

"Copy JSON"

}


</button>


</div>



<pre>


{

JSON.stringify(

data,

null,

4

)

}



</pre>


</div>


);


}