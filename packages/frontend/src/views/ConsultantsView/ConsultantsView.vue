<script setup>
import { ref } from 'vue';

const search = ref('');

const fetchConsultants = () => {
};


const page = ref(1);
const items = Array.from({ length: 15 }, (k, v) => ({
	title: 'Item ' + (v + 1),
	text: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi, ratione debitis quis est labore voluptatibus! Eaque cupiditate minima, at placeat totam, magni doloremque veniam neque porro libero rerum unde voluptatem!',
}));
</script>

<template>
	<v-container>
		<v-col>
			<v-row>
				<v-text-field v-model="search" label="Search"/>
			</v-row>

			<v-row>
				<v-data-iterator :items="items" :page="page">
					<template v-slot:default="{ items }">
						<template v-for="(item, i) in items" :key="i">
							<v-card v-bind="item.raw"></v-card>

							<br/>
						</template>
					</template>


					<template v-slot:footer="{ pageCount }">
						<v-pagination v-model="page" :length="pageCount"></v-pagination>
					</template>
				</v-data-iterator>
			</v-row>
		</v-col>
	</v-container>
</template>

<style scoped>

</style>