<script setup>
import { importData } from '../api/index.js';

const importD = async (file) => {
	try {
		const form = new FormData();
		form.append('file', file)
		await importData(form);
	} catch (e) {
		console.log(e);
	}
}
</script>

<template>
	<v-card>
		<a href="http://0.0.0.0:8000/export" download>export</a>
		<v-file-input @update:model-value="importD" label="File input"></v-file-input>
	</v-card>
</template>

<style scoped>

</style>