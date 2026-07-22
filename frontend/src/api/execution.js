import api from "./client";


export async function getStats(){

    const response = await api.get("/stats/");


    console.log(
        "API DATA:",
        response.data
    );


    return response.data;

}