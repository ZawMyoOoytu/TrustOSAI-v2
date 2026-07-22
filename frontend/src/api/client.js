const BASE_URL = "http://127.0.0.1:8000";



// =====================================================
// GENERIC REQUEST HANDLER
// =====================================================

async function apiRequest(
    url,
    options = {}
) {

    const response = await fetch(

        `${BASE_URL}${url}`,

        {
            headers: {

                "Content-Type": "application/json"

            },

            ...options

        }

    );


    if (!response.ok) {

        const error = await response.text();

        throw new Error(error || "API Request Failed");

    }


    return await response.json();

}





// =====================================================
// DASHBOARD STATISTICS
// =====================================================


export async function getStats() {


    return apiRequest(

        "/stats/"

    );


}






// =====================================================
// EXECUTIONS
// =====================================================


export async function getExecutions() {


    return apiRequest(

        "/executions/"

    );


}






export async function getExecution(id) {


    return apiRequest(

        `/executions/${id}`

    );


}






export async function deleteExecution(id) {


    return apiRequest(

        `/executions/${id}`,

        {

            method:"DELETE"

        }

    );


}






export async function deleteAllExecutions() {


    return apiRequest(

        "/executions/",

        {

            method:"DELETE"

        }

    );


}






// =====================================================
// EXECUTION RUN
// =====================================================


export async function executeTask(data) {


    return apiRequest(

        "/api/execution/",

        {

            method:"POST",

            body:JSON.stringify(data)

        }

    );


}






// =====================================================
// AGENT REGISTRY
// =====================================================



export async function getAgents() {


    return apiRequest(

        "/api/agents/"

    );


}








export async function getAgent(id) {


    return apiRequest(

        `/api/agents/${id}`

    );


}








export async function createAgent(agentData) {


    return apiRequest(

        "/api/agents/",

        {

            method:"POST",

            body:JSON.stringify(agentData)

        }

    );


}








export async function updateAgent(

    id,

    agentData

) {


    return apiRequest(

        `/api/agents/${id}`,

        {

            method:"PATCH",

            body:JSON.stringify(agentData)

        }

    );


}








export async function disableAgent(id) {


    return apiRequest(

        `/api/agents/${id}/disable`,

        {

            method:"PATCH"

        }

    );


}








export async function enableAgent(id) {


    return apiRequest(

        `/api/agents/${id}/enable`,

        {

            method:"PATCH"

        }

    );


}








export async function getAgentStats(id) {


    return apiRequest(

        `/api/agents/${id}/stats`

    );


}







// =====================================================
// POLICY
// =====================================================


export async function getPolicy() {


    return apiRequest(

        "/policy/"

    );


}







// =====================================================
// TRUST EXPLANATION
// =====================================================


export async function getTrustExplanation(id) {


    return apiRequest(

        `/trust/explanation/${id}`

    );


}







// =====================================================
// DECISION REASONING
// =====================================================


export async function getReasoning(id) {


    return apiRequest(

        `/reasoning/${id}`

    );


}







// =====================================================
// HEALTH
// =====================================================


export async function getHealth() {


    return apiRequest(

        "/health/"

    );


}






// =====================================================
// ROOT
// =====================================================


export async function getRoot() {


    return apiRequest(

        "/"

    );


}