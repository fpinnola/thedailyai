import axios from "axios";

const baseURL = 'http://127.0.0.1:5000';

export async function getNews(preferences: any): Promise<any[]> {
    let reqURL = baseURL + '/getNews';
    console.log(`preferences: ${JSON.stringify(preferences)}`);

    return new Promise((resolve) => {
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

export async function getPodcast(preferences: any): Promise<string> {
    let reqURL = baseURL + '/getAudio';
    console.log(`preferences: ${JSON.stringify(preferences)}`);

    return new Promise((resolve) => {
        axios.post(reqURL, preferences)
        .then((res) => {
            console.log(`Received data: ${JSON.stringify(res.data)}`)
            resolve(res.data.audio_url);
        })
        .catch((err) => {
            console.log(`Error getting podcast: ${JSON.stringify(err)}`);
            resolve('');
        });
    })
}