import axios from "axios";
import { BE_BASE_URL } from "../config";

const baseURL = BE_BASE_URL || 'http://127.0.0.1:5000';

export async function getNews(preferences: any): Promise<any[]> {
    let reqURL = baseURL + '/getNews';
    console.log(`preferences: ${JSON.stringify(preferences)}`);

    return new Promise((resolve, reject) => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            // TODO: Send user to login!
            console.log(`Error: user token on longer valid`);
            resolve([]);
            return;
        }
        axios.post(reqURL, preferences, {headers: { Authorization: `Bearer ${JSON.parse(token)}` }})
        .then((res) => {
            resolve(res.data);
        })
        .catch((err) => {
            console.log(`Error getting news: ${JSON.stringify(err)}`);
            if (err.status === 403) {
                reject("unauthorized");
            }
            reject("failed");
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

export async function signupUser(email: string, password: string): Promise<object> {
    let reqURL = baseURL + '/signup';
    // console.log(`preferences: ${JSON.stringify(preferences)}`);

    return new Promise((resolve, reject) => {
        axios.post(reqURL, {
            username: email,
            password: password
        })
        .then((res) => {
            console.log(`Received data: ${JSON.stringify(res.data)}`)
            resolve(res.data);
        })
        .catch((err) => {
            console.log(`Error getting podcast: ${JSON.stringify(err)}`);
            reject(err);
        });
    })
}

export async function login(email: string, password: string): Promise<object> {
    let reqURL = baseURL + '/login';
    // console.log(`preferences: ${JSON.stringify(preferences)}`);

    return new Promise((resolve, reject) => {
        axios.post(reqURL, {
            username: email,
            password: password
        })
        .then((res) => {
            console.log(`Received data: ${JSON.stringify(res.data)}`)
            resolve(res.data);
        })
        .catch((err) => {
            console.log(`Error getting podcast: ${JSON.stringify(err)}`);
            reject(err);
        });
    })
}