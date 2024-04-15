<template>
	<div style="margin: 20px">
		<el-row :gutter="20">
			<el-col :span="17" class="container">
				<el-card style="overflow-y: auto; overflow-x: hidden" class="layout-padding-auto">
					<template #header>
						<div class="card-header">
							<el-form :inline="true">
								<el-form-item label="学校:">
									<el-select
										v-model="state.active_school"
										filterable
										remote
										reserve-keyword
										placeholder="选择学校"
										style="width: 200px"
										:remote-method="search_school"
										@change="list_professional_by_school()"
									>
										<el-option id="school" v-for="item in state.school_list" :key="item.code" :label="item.name" :value="item.code" />
									</el-select>
								</el-form-item>
								<el-form-item label="专业:">
									<el-select v-model="state.active_professional" filterable placeholder="选择专业" style="width: 140px" @change="init()">
										<el-option id="professional" v-for="item in state.professional_list" :key="item.id" :label="item.special_name" :value="item.id" />
									</el-select>
								</el-form-item>
								<el-form-item label-width="120px">
									<el-button type="primary" @click="chat">咨询</el-button>
								</el-form-item>
								<el-form-item label-width="120px" label="限制:">
									<el-switch v-model="state.limit" />
								</el-form-item>
							</el-form>
						</div>
					</template>
					<el-scrollbar>
						<el-form v-if="state.history.length > 0" label-width="auto">
							<div v-for="(item, index) in state.history" :key="index">
								<div v-if="item.role == 'assistant'">
									<el-form-item label="AI助手:" v-if="item.content != ''">
										<div>
											<div>
												<h3>{{ state.platform }}</h3>
											</div>
											<div>
												<v-md-preview
													v-loading="state.loading"
													class="content"
													preview-class="vuepress-markdown-body"
													:text="item.content"
												></v-md-preview>
											</div>
										</div>
									</el-form-item>
								</div>
								<div v-else>
									<el-form-item label="我:">
										<div>
											<div>你</div>
											<div>
												<span>{{ item.question }}</span>
											</div>
										</div>
									</el-form-item>
									<el-form-item label="AI助手">
										<div>
											<div>
												<h3>{{ state.platform }}</h3>
											</div>
											<div>
												<v-md-preview v-loading="state.loading" class="content" :text="item.content"></v-md-preview>
											</div>
										</div>
									</el-form-item>
								</div>
							</div>
						</el-form>
					</el-scrollbar>

					<template #footer>
						<div style="display: flex; align-items: center">
							<el-input v-model="state.question" type="textarea" :rows="2" placeholder="输入需要咨询的内容"> </el-input>
							<el-button plain type="primary" @click="chat" style="margin-left: 20px" :icon="Promotion"></el-button>
						</div>
					</template>
				</el-card>
			</el-col>
			<el-col :span="6">
				<el-card style="height: 95%; margin-bottom: 20px">
					<el-form label-position="top" label-width="auto" style="max-width: 600px">
						<el-form-item label="平台">
							<el-select v-model="state.platform" @change="modelList">
								<el-option v-for="item in platForm" :label="item.type" :value="item.value" :key="item.value" />
							</el-select>
						</el-form-item>
						<el-form-item label="模型">
							<el-select v-model="state.model">
								<el-option v-for="item in state.modelData" :label="item.name" :value="item.value" :key="item.value" />
							</el-select>
						</el-form-item>
						<el-form-item label="max_token">
							<el-slider v-model="state.max_tokens" show-input :min="1024" :max="40960" :step="1024" />
						</el-form-item>
						<el-form-item label="历史记录">
							<el-input />
						</el-form-item>
						<el-form-item label="输入预设">
							<el-input type="textarea" :rows="3" placeholder="输入系统人社,例如: 你是一个AI助手" />
						</el-form-item>
					</el-form>
					<el-button type="primary" plain @click="clearCache">清理当前缓存</el-button>
					<el-button type="primary" plain @click="clearAllCache">清理全部缓存</el-button>
				</el-card>
			</el-col>
		</el-row>
	</div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue';
import { GetSchool, GetProfessionals, AiChat } from './api';
import { School, Professional } from '/@/types/school';
import { v4 as uuidv4 } from 'uuid';
import { useChatStore } from '/@/stores/chat';
import { ChatMessage } from '/@/types/chat';
import { Promotion } from '@element-plus/icons-vue';

const historyStore = useChatStore();

const state = reactive({
	limit: true,
	platform: 'qianfan',
	model: '',
	max_tokens: 1024,
	school_list: [] as Array<School>,
	active_school: '',
	professional_list: [] as Array<Professional>,
	active_professional: '',
	question: '',
	loading: false,
	history: [] as Array<ChatMessage>,
	active_history: '',
	modelData: [] as Array<Model>,
});

interface Model {
	name: string;
	value: string;
}
const modelList = () => {
	state.model = '';
	let modelData = [] as Array<Model>;
	platForm.forEach((item) => {
		if (item.value === state.platform) {
			modelData = item.model;
		}
	});
	state.model = modelData[0].value;
	state.modelData = modelData;
};

onMounted(() => {
	// list_school();
	modelList();
});

const init = () => {
	state.history = [];
	let is_found = false;
	historyStore.chatHistory.forEach((item) => {
		if (item.professional_code === state.active_professional && item.school_code === state.active_school) {
			state.history = item.history;
			state.active_history = item.id;
			is_found = true;
		}
	});
	if (!is_found) {
		historyStore.chatHistory.push({
			id: uuidv4(),
			professional_code: state.active_professional,
			school_code: state.active_school,
			history: state.history,
		});
		state.active_history = historyStore.chatHistory[0].id;
	}
	console.log('是否找到缓存:' + is_found);
};

const search_school = async (query: string) => {
	if (query == '') {
		return;
	}
	await GetSchool({ name: query }).then((res: any) => {
		state.school_list = res.data;
	});
};

const list_professional_by_school = async () => {
	await GetProfessionals({
		school_id: state.active_school,
	}).then((res: any) => {
		state.professional_list = res.data;
	});
};

const deleteErrorData = () => {
	let h = [] as Array<ChatMessage>;

	state.history.filter((item) => {
		if (!item.is_error) {
			h.push(item);
		}
	});
	if (h.length === 0) {
		h.push({
			role: 'assistant',
			content: '',
			question: '',
			is_error: false,
		});
	}
	return h;
};
const chat = async () => {
	const question = (state.question = state.question.trim());
	state.question = '';

	if (question != '') {
		state.history.push({
			role: 'user',
			content: '',
			question: question,
			is_error: false,
		});
	} else if (question.length === 0) {
		state.history.push({
			role: 'assistant',
			content: '',
			question: '',
			is_error: false,
		});
	}

	const { body, status } = await AiChat({
		school_id: state.active_school,
		professional_id: state.active_professional,
		uuid: state.active_history,
	});

	if (body) {
		const reader = body.getReader();
		if (state.history[state.history.length - 1].content != '') {
			state.history.push({
				question: '',
				role: 'assistant',
				content: '',
				is_error: false,
			});
		}
		await readStream(reader, status);
	}
};
const decoder = new TextDecoder('utf-8');
const readStream = async (reader: ReadableStreamDefaultReader<Uint8Array>, status: number) => {
	while (true) {
		const { value, done } = await reader.read();
		if (done) {
			saveHistory(state.active_history);
			break;
		}
		const decodedText = decoder.decode(value, { stream: true });
		if (status !== 200) {
			const code = JSON.parse(decodedText);
			state.history[state.history.length - 1].content += code.message;
			state.history[state.history.length - 1].is_error = true;
			saveHistory(state.active_history);
			break;
		}

		if (decodedText.startsWith('{"code":')) {
			const code = JSON.parse(decodedText);
			if (code.code != 200) {
				state.history[state.history.length - 1].content += code.message;
				state.history[state.history.length - 1].is_error = true;
				saveHistory(state.active_history);
				break;
			}
			break;
		}
		appendLastMessageContent(decodedText);
	}
};

const appendLastMessageContent = (content: string) => {
	state.history[state.history.length - 1].content += content;
};

const saveHistory = (id: string) => {
	historyStore.chatHistory.forEach((item) => {
		if (item.id === id) {
			item.history = state.history;
		}
	});
};

const platForm = [
	{
		type: '千帆',
		value: 'qianfan',
		model: [
			{
				name: 'ERNIE-Bot-turbo',
				value: 'ERNIE-Bot-turbo',
			},
			{
				name: 'ERNIE-Bot-turbo-AI',
				value: 'ERNIE-Bot-turbo-AI',
			},
			{
				name: 'Qianfan-Chinese-Llama-2-13B',
				value: 'Qianfan-Chinese-Llama-2-13B',
			},
			{
				name: 'Llama-2-13b-chat',
				value: 'Llama-2-13b-chat',
			},
		],
	},
	{
		type: 'chatGPT',
		value: 'chatgpt',
		model: [
			{
				name: 'gpt-3.5-turbo',
				value: 'gpt-3.5-turbo',
			},
			{
				name: 'GPT-4 Turbo',
				value: 'gpt-4',
			},
		],
	},
	{
		type: '月之暗面',
		value: 'moonshot',
		model: [
			{
				name: 'moonshot-v1-8k',
				value: 'moonshot-v1-8k',
			},
		],
	},
];
const clearCache = () => {
	state.history = [];
	saveHistory(state.active_history);
};
const clearAllCache = () => {
	state.history = [];
	historyStore.chatHistory = [];
	init();
};
</script>

<style scoped lang="scss">
.el-card__body {
	padding: 0;
}
.content {
	overflow-x: hidden;
	border: 1px solid rgba(155, 9, 9, 0.96);
	border-radius: 4px;
	margin-right: 10px;
	width: 100%;
}

.container {
	:deep(.el-card__body) {
		//position : absolute;
		display: flex;
		flex-direction: column;
		flex: 1;
		overflow: auto;
		height: 60vh;
		.el-table {
			flex: 1;
		}
	}
}
</style>
