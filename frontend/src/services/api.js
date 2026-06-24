import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
});

// Request interceptor to add the auth token to headers
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh on 401
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const res = await axios.post("http://127.0.0.1:8000/api/accounts/token/refresh/", { refresh: refreshToken });
                    const newAccess = res.data.access;
                    localStorage.setItem('access_token', newAccess);
                    // update header and retry
                    originalRequest.headers.Authorization = `Bearer ${newAccess}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    console.error("Token refresh failed", refreshError);
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/login';
                }
            } else {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;