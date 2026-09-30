import api from "./client";


// =====================================================
// DASHBOARD STATISTICS
// =====================================================

export async function getStats(){

    const response = await api.get(
        "/api/stats/"
    );


    return response.data;

}