import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ChatHistory } from '/@/types/chat';

export const useChatStore = defineStore(
	'chat_history',
	() => {
		const chatHistory = ref<Array<ChatHistory>>([]);
		return { chatHistory };
	},
	{
		persist: {
			enabled: true,
		},
	}
);
