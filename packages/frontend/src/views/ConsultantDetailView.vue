<script setup>
import { computed, onMounted, ref } from 'vue';
import { getDetailPsychologist } from '../api/index.js';
import { useRoute } from 'vue-router';

const route = useRoute();

const id = computed(() => route.params.id);

const consultant = ref();

const fetchConsultant = async () => {
	try {
		const { data } = await getDetailPsychologist(id.value);
		consultant.value = data;
	} catch (e) {
		console.log(e);
	}
};

onMounted(fetchConsultant);
</script>

<template>
	<v-card v-if='consultant'>
		<v-list lines="one">
			<v-list-item
				v-for="[key, value] in Object.entries(consultant)"
				:key="key"
				:title="key"
				:subtitle="value"
			></v-list-item>
		</v-list>
	</v-card>
</template>

<style scoped>

</style>