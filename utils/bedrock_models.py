from enum import Enum

class BedrockModel(Enum):

    # Amazon Nova
    AMAZON_NOVA_PRO = "amazon.nova-pro-v1:0"
    AMAZON_NOVA_MICRO = "amazon.nova-micro-v1:0"
    AMAZON_NOVA_LITE = "amazon.nova-lite-v1:0"

    # Anthropic Claude 3.0
    CLAUDE_3_HAIKU_1_0 = "anthropic.claude-3-haiku-20240307-v1:0"
    CLAUDE_3_SONNET_1_0 = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_3_OPUS_1_0 = "anthropic.claude-3-opus-20240229-v1:0"

    # Anthropic Claude 3.5
    CLAUDE_3_5_SONNET_1_0 = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    CLAUDE_3_5_SONNET_2_0 = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    CLAUDE_3_5_HAIKU_1_0 = "anthropic.claude-3-5-haiku-20241022-v1:0"
