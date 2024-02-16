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
            console.log(`Error: user token no longer valid`);
            reject("failed");
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

export async function updateUserPreferences(preferences: any): Promise<object> {
    let reqURL = baseURL + '/user/prefs';
    // console.log(`preferences: ${JSON.stringify(preferences)}`);

    return new Promise((resolve, reject) => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            // TODO: Send user to login!
            console.log(`Error: user token no longer valid`);
            reject("failed");
            return;
        }
        axios.post(reqURL, {
            preferences: preferences
        }, {headers: { Authorization: `Bearer ${JSON.parse(token)}` }})
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
            const { access_token, refresh_token } = res.data;
            localStorage.setItem('access_token', JSON.stringify(access_token));
            localStorage.setItem('refresh_token', JSON.stringify(refresh_token));

            resolve(res.data);
        })
        .catch((err) => {
            console.log(`Error getting podcast: ${JSON.stringify(err)}`);
            reject(err);
        });
    })
}

async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
        throw new Error('No refresh token available');
    }
    try {
        const response = await axios.post(`${baseURL}/token/refresh`, {}, {
            headers: { Authorization: `Bearer ${JSON.parse(refreshToken)}`}
        });
        const { access_token } = response.data;
        localStorage.setItem('access_token', JSON.stringify(access_token));
        return access_token;
    } catch (err) {
        console.error(`Error refreshing token:`, err);
        throw err;
    }
}

export function setupAxiosInterceptors() {
    axios.interceptors.response.use(
        response => response, // Return the response if it's successful without changes
        async error => {
          const originalRequest = error.config;
          if (error.response.status === 401 && !originalRequest._retry) {
            // Mark this request as already tried
            originalRequest._retry = true;
            try {
              // Attempt to get a new token
              console.log("Refreshing token");
              const newAccessToken = await refreshToken();
              console.log(`New Access token: ${newAccessToken}`)
              // Update the authorization header and retry the original request
              originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
              return axios(originalRequest);
            } catch (refreshError) {
              return Promise.reject(refreshError);
            }
          }
          return Promise.reject(error);
        }
      );
}