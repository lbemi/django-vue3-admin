interface ChatData {
  chat_type: string;
  school_code: number;
  professional_code: number;
  uuid: string;
  question: string;
  answer: string;
  history: {
    uuid: string;
    school_code: number;
    professional_code: number;
    question: Array<string>;
    answer: Array<string>;
  };
}

export interface ChatMessage {
  question: string;
  role: "user" | "assistant";
  content: string;
  is_error: boolean
}

export interface ChatHistory {
  id: string;
  school_code: string;
  professional_code: string;
  history: Array<ChatMessage>;
}
