import axios from "axios";

const baseURL = 'http://127.0.0.1:5000';

export async function getNews(preferences: any): Promise<any[]> {
    let reqURL = baseURL + '/getNews';
    console.log(`preferences: ${JSON.stringify(preferences)}`);

    return new Promise((resolve, reject) => {
        axios.post(reqURL, preferences)
        .then((res) => {
            resolve(res.data);
        })
        .catch((err) => {
            console.log(`Error getting news: ${JSON.stringify(err)}`);
            resolve([]);
        });
    })
}