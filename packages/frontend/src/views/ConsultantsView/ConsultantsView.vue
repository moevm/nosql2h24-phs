<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { getPsychologists } from '../../api/index.js';

const headers = [
	{ title: 'Name', key: 'name' },
	{ title: 'Surname', key: 'surname' },
	{ title: 'Email', key: 'email' },
	{ title: 'Price', key: 'price' },
	{ title: 'Address', key: 'address' },
	{ title: 'Meeting_format', key: 'meeting_format' },
	{ title: 'Language', key: 'language' },
];

const filterState = reactive({
	search: '',
	meetingFormat: '',
	email: '',
	minPrice: '',
	maxPrice: '',
	language: ''
});
const consultants = ref([]);

const fetchConsultants = async () => {
	try {
		const { data } = await getPsychologists({
			search: filterState.search,
			price_min: filterState.minPrice,
			price_max: filterState.maxPrice,
			meeting_format: filterState.meetingFormat,
			email: filterState.email,
			language: filterState.language
		});
		consultants.value = data;
	} catch (e) {
		console.log(e);
	}
};

const resetFilterState = () => {
	filterState.meetingFormat = '';
	filterState.search = '';
	filterState.meetingFormat = '';
	filterState.email = '';
	filterState.minPrice = '';
	filterState.maxPrice = '';
	filterState.language = '';
};

watch([filterState], fetchConsultants, { deep: true });

onMounted(fetchConsultants);
</script>

<template>
	<v-container>
		<v-col>
			<v-row>
				<v-text-field v-model="filterState.search" label="Search"/>
			</v-row>
			<v-row>
				<v-text-field v-model="filterState.minPrice" label="от Price" type="number"/>
				<v-text-field v-model="filterState.maxPrice" label="до Price" type="number"/>
			</v-row>
			<v-row>
				<v-text-field v-model="filterState.email" label="Email"/>
			</v-row>
			<v-row>
				<v-select
					v-model="filterState.meetingFormat"
					label="Meeting format"
					:items="['online', 'offline']"
				></v-select>
			</v-row>
			<v-row>
				<v-select
					v-model="filterState.language"
					label="Language"
					:items="['English', 'Russian']"
				></v-select>
			</v-row>
			<v-row>
				<v-btn text="Сбросить" @click="resetFilterState"></v-btn>
			</v-row>


			<v-row v-if="consultants.length">
				<v-data-table :headers="headers" :items="consultants">
					<template v-slot:item.name="{ value, item }">
						<router-link :to="`/consultant/${item.id}`">
							{{ value }}
						</router-link>
					</template>
				</v-data-table>
			</v-row>
		</v-col>
	</v-container>
</template>

<style scoped>

</style>