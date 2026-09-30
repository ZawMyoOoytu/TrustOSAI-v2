export default function MetricCard({

    title,

    value,

    icon

}){


return (

<div className="metric-card">


    <div className="metric-title">

        {icon}

        {" "}

        {title}

    </div>



    <div className="metric-value">

        {value}

    </div>


</div>


);


}