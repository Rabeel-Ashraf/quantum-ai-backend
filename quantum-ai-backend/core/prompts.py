from config.prompts import SYSTEM_PROMPT_RULES, AGENT_PROMPTS

def apply_system_prompts(base_prompt: str, agent_type: str = None) -> str:
    """
    Apply all system prompt rules to a base prompt
    """
    rules_text = "\n".join([f"- {rule}" for rule in SYSTEM_PROMPT_RULES.values()])
    
    prompt = f"""
    {base_prompt}
    
    You must always follow these system rules:
    {rules_text}
    """
    
    if agent_type and agent_type in AGENT_PROMPTS:
        prompt = f"""
        {AGENT_PROMPTS[agent_type]}
        
        {prompt}
        """
    
    return prompt.strip()

def get_agent_prompt(agent_type: str) -> str:
    """
    Get the base prompt for a specific agent type
    """
    if agent_type in AGENT_PROMPTS:
        return apply_system_prompts(AGENT_PROMPTS[agent_type], agent_type)
    return apply_system_prompts("You are a helpful AI assistant.")
