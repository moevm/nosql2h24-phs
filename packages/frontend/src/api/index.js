import axios from 'axios';

export const buildQueryString = (params)=> {
	const esc = encodeURIComponent;
	return Object.keys(params)
		.filter(k => params[k] !== null && params[k] !== undefined && params[k] !== "")
		.map(k => esc(k) + "=" + esc(params[k]))
		.join("&");
};

export const api = axios.create({
	baseURL: 'http://localhost:8000',
});

export const register = (body) => {
	return api.post('/register', body);
}

export const login = (body) => {
	return api.post('/login', body);
}

export const getPsychologists = (query) => {
	const queryString = buildQueryString(query)
	return api.get(`/psychologists?${queryString}`);
}

export const getDetailPsychologist = (id) => {
	return api.get(`/psychologists/${id}`);
}

export const importData = (form) => {
	return api.post(`/import`, form);
}