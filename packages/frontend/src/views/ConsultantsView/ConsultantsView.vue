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
	price: '',
	language: ''
});
const consultants = ref([]);

const fetchConsultants = async () => {
	try {
		const { data } = await getPsychologists({
			search: filterState.search,
			meetingFormat: filterState.meetingFormat,
			email: filterState.email,
			price: filterState.price,
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
	filterState.price = '';
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
				<v-text-field v-model="filterState.price" label="Price"/>
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