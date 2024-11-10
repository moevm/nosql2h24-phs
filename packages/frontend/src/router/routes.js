const RegistrationView = () => import('../views/RegistrationView/RegistrationView.vue');
const LoginView = () => import('../views/LoginView/LoginView.vue');
const ConsultantsView = () => import('../views/ConsultantsView/ConsultantsView.vue');

export const routes = [
	{ path: '/registration', component: RegistrationView },
	{ path: '/login', component: LoginView },
	{ path: '/consultant', component: ConsultantsView },
];