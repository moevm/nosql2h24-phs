import axios from 'axios';

export const api = axios.create({
	baseURL: 'http://localhost:8000',
});

export const register = (body) => {
	return api.post('/register', body);
}

export const login = (body) => {
	return api.post('/login', body);
}

export const getPsychologists = (search) => {
	return api.get(`/psychologists?search=${search}`);
}