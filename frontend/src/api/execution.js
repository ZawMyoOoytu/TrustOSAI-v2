import api from "./client";


export async function getExecutions(){

    const response = await api.get(
        "/api/executions/"
    );

    return response.data;

}


export async function getExecution(id){

    const response = await api.get(
        `/api/executions/${id}`
    );

    return response.data;

}


export async function deleteExecution(id){

    const response = await api.delete(
        `/api/executions/${id}`
    );

    return response.data;

}