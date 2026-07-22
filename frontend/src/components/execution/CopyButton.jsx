import {useState} from "react";


export default function CopyButton({data}){


const [copied,setCopied]=useState(false);



async function copyJSON(){


await navigator.clipboard.writeText(

JSON.stringify(
data,
null,
2
)

);



setCopied(true);



setTimeout(()=>{

setCopied(false);

},2000);



}



return (

<button

className="copy-btn"

onClick={copyJSON}

>

{

copied

?

"✓ Copied"

:

"📋 Copy JSON"

}


</button>


);


}