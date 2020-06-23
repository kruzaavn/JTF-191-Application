import axios from 'axios'

let host = location.host

export async function postAPI(endpoint, data) {

    return axios.post(`http://${host}${endpoint}`, data).then(response => {return response.data})

}

export async function getAPI(endpoint, queryparams) {

    return axios.get(`http://${host}${endpoint}`, queryparams).then(response => {return response.data})

}