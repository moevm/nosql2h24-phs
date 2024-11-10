<script setup>
import { reactive } from 'vue';

const user = reactive({
	email: '',
	password: ''
});

const handleSubmit = () => {
};
</script>

<template>
	<v-sheet width="400px" class="mx-auto">
		<v-form @submit.prevent="handleSubmit">
			<v-container>
				<v-col>
					<v-row justify="center">
						<h3 class="text-h3">Вход</h3>
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
							Авторизоваться
						</v-btn>
					</v-row>

					<v-row justify="center">
					<span class="text-subtitle-1">
						Уже нет аккаунта?
					<router-link to="/registration">Зарегистрироваться</router-link>
					</span>
					</v-row>
				</v-col>
			</v-container>
		</v-form>
	</v-sheet>
</template>

<style scoped>

</style>