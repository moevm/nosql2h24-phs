<script setup>
import { onMounted, ref, watch } from 'vue';
import { getPsychologists } from '../../api/index.js';

const search = ref('');
const consultants = ref([]);

const fetchConsultants = async () => {
	try {
		const { data } = await getPsychologists(search.value);
		consultants.value = data;
	} catch (e) {
		console.log(e);
	}
};

watch([search], fetchConsultants);

onMounted(fetchConsultants);
</script>

<template>
	<v-container>
		<v-col>
			<v-row>
				<v-text-field v-model="search" label="Search"/>
			</v-row>


			<v-row v-if="consultants.length">
				<v-virtual-scroll
					:height="300"
					:items="consultants"
				>
					<template v-slot:default="{ item }">
						<v-card :title="item.name"></v-card>

						<br/>
					</template>
				</v-virtual-scroll>
			</v-row>
		</v-col>
	</v-container>
</template>

<style scoped>

</style>