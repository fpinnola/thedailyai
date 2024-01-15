import axios from "axios";

const baseURL = 'http://localhost:5000';

export async function getNews(preferences: any) {
    let reqURL = baseURL + '/getNews';

    return new Promise((resolve, reject) => {
        axios.post(reqURL, preferences)
        .then((res) => {
            resolve(res.data);
        })
        .catch((err) => {
            console.log(`Error getting news: ${JSON.stringify(err)}`);
            resolve(null);
        });
    })
}