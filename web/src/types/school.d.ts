import { ChatMessage } from "./chat";

export interface School {
  code: string;
  name: string;
  f985: string;
  f211: string;
  p: string;
  c: string;
  qj: string;
  answerurl: string;
  dual_class: string;
  level: string;
}

export interface Professional {
  id: string;
  school_id: string;
  special_id: string;
  nation_feature: string;
  province_feature: string;
  is_important: string;
  limit_year: string;
  year: string;
  level3_weight: string;
  nation_first_class: string;
  xueke_rank_score: string;
  is_video: number;
  special_name: string;
  special_type: string;
  type_name: string;
  level3_name: string;
  level3_code: string;
  level2_name: string;
  level2_id: string;
  level2_code: string;
  code: string;
}

interface ChatRequest {
  limit: boolean;
  chat_type: string;
  model: string;
  max_tokens: number;
  school_code: number;
  professional_code: number;
  uuid: string;
  messages: Array<ChatMessage>;
}
