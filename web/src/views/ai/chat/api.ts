import { getBaseURL } from '/@/utils/baseUrl';
import { request } from '/@/utils/service';
import { Session } from '/@/utils/storage';

interface schoolQuery {
	name?: string;
}

/**
 * 获取学校信息
 *
 * @param query 学校查询参数
 * @returns 返回学校信息
 */
export function GetSchool(query: schoolQuery) {
	return request({
		url: 'api/education/school/',
		method: 'get',
		params: query,
	});
}

interface ProfessionalQuery {
	profession_name?: string;
	school_id: string;
}
/**
 * 获取专业列表
 *
 * @param query 专业查询参数
 * @returns 返回专家列表
 */
export function GetProfessionals(query: ProfessionalQuery) {
	return request({
		url: 'api/education/professional/',
		method: 'get',
		params: query,
	});
}

interface ChatData {
	message?: string;
	school_id: string;
	professional_id: string;
	uuid: string;
}

/**
 * AI聊天函数
 *
 * @param data 聊天数据
 * @returns 返回一个请求对象
 */

export async function AiChat(data: ChatData) {
	try {
		const url = getBaseURL() + 'api/ai/chat';
		const token = Session.get('token');
		const result = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `JWT ${token}`,
			},
			body: JSON.stringify(data),
		});
		return result;
	} catch (error) {
		return error;
	}
}
