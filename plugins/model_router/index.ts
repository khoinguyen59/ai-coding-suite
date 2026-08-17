import { classifyPrompt, RouteDecision } from './router_logic';

export interface MultiModelConfig {
  endpoints: {
    [key: string]: {
      name: string;
      baseUrl: string;
      apiKey?: string;
    };
  };
}

export class DeepSeekHarnessModelRouter {
  private config: MultiModelConfig;

  constructor(config: MultiModelConfig) {
    this.config = config;
  }

  public route(userPrompt: string): { endpointUrl: string; modelName: string; decision: RouteDecision } {
    const decision = classifyPrompt(userPrompt);
    const targetEndpoint = this.config.endpoints[decision.endpointKey] || this.config.endpoints['coding'];

    return {
      endpointUrl: targetEndpoint.baseUrl,
      modelName: targetEndpoint.name,
      decision,
    };
  }
}
