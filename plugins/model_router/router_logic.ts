export type TaskType = 'reasoning' | 'coding' | 'review';

export interface RouteDecision {
  taskType: TaskType;
  endpointKey: string;
  reason: string;
}

export function classifyPrompt(prompt: string): RouteDecision {
  const lower = prompt.toLowerCase();

  // 1. Phân loại tác vụ Suy luận / Thiết kế kiến trúc / Giải thuật khó
  const reasoningKeywords = [
    'kiến trúc', 'thiết kế', 'giải thuật', 'thuật toán', 'chứng minh',
    'phân tích logic', 'tối ưu độ phức tạp', 'architect', 'design pattern',
    'algorithm', 'reasoning', 'think step by step', 'math', 'prove', 'complexity'
  ];
  if (reasoningKeywords.some(kw => lower.includes(kw))) {
    return {
      taskType: 'reasoning',
      endpointKey: 'reasoning',
      reason: 'Phát hiện yêu cầu tư duy thuật toán/kiến trúc hệ thống -> Sử dụng DeepSeek-R1 Distill'
    };
  }

  // 2. Phân loại tác vụ Review / Bảo mật / Audit mã nguồn
  const reviewKeywords = [
    'review', 'kiểm tra lỗi', 'bảo mật', 'vulnerability', 'audit',
    'viết unit test', 'test case', 'edge case', 'kiểm thử', 'leak', 'xss', 'sql injection'
  ];
  if (reviewKeywords.some(kw => lower.includes(kw))) {
    return {
      taskType: 'review',
      endpointKey: 'review',
      reason: 'Phát hiện yêu cầu kiểm tra mã/bảo mật/test cases -> Sử dụng DeepSeek-Coder-V2'
    };
  }

  // 3. Mặc định: Sinh mã nguồn / Refactor / Viết hàm
  return {
    taskType: 'coding',
    endpointKey: 'coding',
    reason: 'Phát hiện tác vụ viết code/refactor/triển khai -> Sử dụng Qwen2.5-Coder'
  };
}
