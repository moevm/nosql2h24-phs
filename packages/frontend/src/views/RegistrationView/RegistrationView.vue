<script setup>
import { reactive } from 'vue';
import { register } from '../../api/index.js';
import { useRouter } from 'vue-router';

const router = useRouter();

const user = reactive({
	lastName: '',
	firstName: '',
	email: '',
	password: ''
});

const handleSubmit = async () => {
	try {
		await register({ email: user.email, password: user.password, lastName: user.lastName, firstName: user.firstName });
		router.push('/consultant');
	} catch (e) {
		console.log(e);
	}
};
</script>

<template>
	<v-sheet width="400px" class="mx-auto">
		<v-form @submit.prevent="handleSubmit">
			<v-container>
				<v-col>
					<v-row justify="center">
						<h3 class="text-h3">Регистрация</h3>
					</v-row>

					<v-row>
						<v-text-field
							v-model="user.firstName"
							label="First name"
							required
						></v-text-field>
					</v-row>

					<v-row>
						<v-text-field
							v-model="user.lastName"
							label="Last name"
							required
						></v-text-field>
					</v-row>

					<v-row>
						<v-text-field
							v-model="user.email"
							label="E-mail"
							required
						></v-text-field>
					</v-row>

					<v-row>
						<v-text-field
							v-model="user.password"
							label="Password"
							required
						></v-text-field>
					</v-row>

					<v-row justify="center">
						<v-btn type="submit">
							Зарегистрироваться
						</v-btn>
					</v-row>

					<v-row justify="center">
					<span class="text-subtitle-1">
						Уже есть аккаунт?
					<router-link to="/login">Авторизоваться</router-link>
					</span>
					</v-row>
				</v-col>
			</v-container>
		</v-form>
	</v-sheet>
</template>

<style scoped>

</style>