const RegistrationView = () => import('../views/RegistrationView/RegistrationView.vue');
const LoginView = () => import('../views/LoginView/LoginView.vue');

export const routes = [
	{ path: '/registration', component: RegistrationView },
	{ path: '/login', component: LoginView },
];