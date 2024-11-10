<script setup>
import { reactive } from 'vue';

const user = reactive({
	lastName: '',
	firstName: '',
	email: '',
	password: ''
});

const handleSubmit = () => {
};
</script>

<template>
	<v-sheet width="400px">
		<v-form @submit.prevent="handleSubmit">
			<v-container>
				<v-col>
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