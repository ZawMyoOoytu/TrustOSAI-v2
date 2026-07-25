const BASE_URL = "http://127.0.0.1:8000";



// =====================================================
// GENERIC REQUEST
// =====================================================

async function request(
    endpoint,
    options={}
){

    const response = await fetch(

        `${BASE_URL}${endpoint}`,

        {

            headers:{

                "Content-Type":
                "application/json"

            },

            ...options

        }

    );



    if(!response.ok){

        const error =
            await response.text();


        throw new Error(
            error || "API Request Failed"
        );

    }



    return await response.json();

}





// =====================================================
// DEFAULT API CLIENT
// execution.js အတွက်
// =====================================================


const api = {


    get(endpoint){

        return request(endpoint)
        .then(data=>({

            data

        }));

    },



    post(endpoint,body){

        return request(

            endpoint,

            {

                method:"POST",

                body:
                JSON.stringify(body)

            }

        )
        .then(data=>({

            data

        }));

    },



    patch(endpoint,body={}){

        return request(

            endpoint,

            {

                method:"PATCH",

                body:
                JSON.stringify(body)

            }

        )
        .then(data=>({

            data

        }));

    },



    delete(endpoint){

        return request(

            endpoint,

            {

                method:"DELETE"

            }

        )
        .then(data=>({

            data

        }));

    }


};



export default api;






// =====================================================
// DASHBOARD
// =====================================================

export async function getStats(){

    return request(
        "/api/stats/"
    );

}






// =====================================================
// AGENTS
// =====================================================


export async function getAgents(){

    return request(
        "/api/agents/"
    );

}




export async function getAgent(id){

    return request(
        `/api/agents/${id}`
    );

}




export async function createAgent(data){

    return request(

        "/api/agents/",

        {

            method:"POST",

            body:
            JSON.stringify(data)

        }

    );

}




export async function updateAgent(
    id,
    data
){

    return request(

        `/api/agents/${id}`,

        {

            method:"PATCH",

            body:
            JSON.stringify(data)

        }

    );

}





export async function enableAgent(id){

    return request(

        `/api/agents/${id}/enable`,

        {

            method:"PATCH"

        }

    );

}





export async function disableAgent(id){

    return request(

        `/api/agents/${id}/disable`,

        {

            method:"PATCH"

        }

    );

}





export async function getAgentStats(id){

    return request(

        `/api/agents/${id}/stats`

    );

}






// =====================================================
// POLICY
// =====================================================

export async function getPolicy(){

    return request(
        "/api/policy/"
    );

}





// =====================================================
// HEALTH
// =====================================================

export async function getHealth(){

    return request(
        "/api/health/"
    );

}





// =====================================================
// ROOT
// =====================================================

export async function getRoot(){

    return request(
        "/"
    );

}