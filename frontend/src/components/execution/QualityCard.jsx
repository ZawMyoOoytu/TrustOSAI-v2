export default function QualityCard({
    score
}){


const percent =
Math.round(
(score || 0)*100
);



return (

<div className="execution-card">


<h2>
⭐ Quality Score
</h2>



<div className="progress-box">


<div
className="progress-fill"
style={{
width:`${percent}%`
}}
>

</div>


</div>



<h1>

{percent}%

</h1>



</div>


);


}