# Project: tests

## Directory Structure

```
📁 tests
├── 📁 e2e
│   ├── 📁 multimodal
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 image_server.py
│   │   ├── 📄 sample.pdf
│   │   └── 📄 test_multimodal_images.py
│   ├── 📁 prompts-resources
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 fastagent.jsonl
│   │   ├── 📄 multiturn.md
│   │   ├── 📄 sample.pdf
│   │   ├── 📄 simple.txt
│   │   ├── 📄 style.css
│   │   ├── 📄 test_prompts.py
│   │   ├── 📄 test_resources.py
│   │   ├── 📄 with_attachment.md
│   │   └── 📄 with_attachment_css.md
│   ├── 📁 sampling
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 fastagent.jsonl
│   │   ├── 📄 sampling_resource_server.py
│   │   └── 📄 test_sampling_e2e.py
│   ├── 📁 smoke
│   │   ├── 📁 base
│   │   │   ├── 📄 fastagent.config.yaml
│   │   │   ├── 📄 index.js.TEST_ONLY
│   │   │   ├── 📄 test_e2e_smoke.py
│   │   │   └── 📄 test_server.py
│   │   └── 📁 tensorzero
│   │       ├── 📄 test_agent_interaction.py
│   │       ├── 📄 test_image_demo.py
│   │       └── 📄 test_simple_agent_interaction.py
│   ├── 📁 structured
│   │   ├── 📄 fastagent.config.yaml
│   │   └── 📄 test_structured_outputs.py
│   ├── 📁 workflow
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 test_router_agent_e2e.py
│   │   └── 📄 test_routing_server.py
│   └── 📄 conftest.py
├── 📁 integration
│   ├── 📁 api
│   │   ├── 📄 fastagent.config.markup.yaml
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 fastagent.secrets.yaml
│   │   ├── 📄 integration_agent.py
│   │   ├── 📄 mcp_dynamic_tools.py
│   │   ├── 📄 mcp_tools_server.py
│   │   ├── 📄 playback.md
│   │   ├── 📄 prompt.txt
│   │   ├── 📄 stderr_test_script.py
│   │   ├── 📄 test_api.py
│   │   ├── 📄 test_cli_and_mcp_server.py
│   │   ├── 📄 test_describe_a2a.py
│   │   ├── 📄 test_hyphens_in_name.py
│   │   ├── 📄 test_logger_textio.py
│   │   ├── 📄 test_markup_config.py
│   │   ├── 📄 test_prompt_commands.py
│   │   ├── 📄 test_prompt_listing.py
│   │   ├── 📄 test_provider_keys.py
│   │   └── 📄 test_tool_list_change.py
│   ├── 📁 elicitation
│   │   ├── 📄 elicitation_test_server.py
│   │   ├── 📄 elicitation_test_server_advanced.py
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 manual_advanced.py
│   │   ├── 📄 manual_test.py
│   │   ├── 📄 test_config_modes.py
│   │   ├── 📄 test_config_modes_simplified.py
│   │   ├── 📄 test_elicitation_handler.py
│   │   ├── 📄 test_elicitation_integration.py
│   │   └── 📄 testing_handlers.py
│   ├── 📁 prompt-server
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 multi.txt
│   │   ├── 📄 multi_sub.txt
│   │   ├── 📄 multipart.json
│   │   ├── 📄 simple.txt
│   │   ├── 📄 simple_sub.txt
│   │   └── 📄 test_prompt_server_integration.py
│   ├── 📁 prompt-state
│   │   ├── 📄 conv1_simple.md
│   │   ├── 📄 conv2_attach.md
│   │   ├── 📄 conv2_css.css
│   │   ├── 📄 conv2_text.txt
│   │   ├── 📄 fastagent.config.yaml
│   │   └── 📄 test_load_prompt_templates.py
│   ├── 📁 resources
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 prompt1.txt
│   │   ├── 📄 prompt2.txt
│   │   ├── 📄 r1file1.txt
│   │   ├── 📄 r1file2.txt
│   │   ├── 📄 r2file1.txt
│   │   ├── 📄 r2file2.txt
│   │   └── 📄 test_resource_api.py
│   ├── 📁 roots
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 fastagent.jsonl
│   │   ├── 📄 live.py
│   │   ├── 📄 root_client.py
│   │   ├── 📄 root_test_server.py
│   │   └── 📄 test_roots.py
│   ├── 📁 sampling
│   │   ├── 📄 fastagent.config.auto_sampling_off.yaml
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 live.py
│   │   ├── 📄 sampling_test_server.py
│   │   └── 📄 test_sampling_integration.py
│   ├── 📁 workflow
│   │   ├── 📁 chain
│   │   │   ├── 📄 fastagent.config.yaml
│   │   │   ├── 📄 test_chain.py
│   │   │   └── 📄 test_chain_passthrough.py
│   │   ├── 📁 evaluator_optimizer
│   │   │   ├── 📄 fastagent.config.yaml
│   │   │   └── 📄 test_evaluator_optimizer.py
│   │   ├── 📁 mixed
│   │   │   ├── 📄 fastagent.config.yaml
│   │   │   └── 📄 test_mixed_workflow.py
│   │   ├── 📁 orchestrator
│   │   │   ├── 📄 fastagent.config.yaml
│   │   │   └── 📄 test_orchestrator.py
│   │   ├── 📁 parallel
│   │   │   ├── 📄 fastagent.config.yaml
│   │   │   └── 📄 test_parallel_agent.py
│   │   └── 📁 router
│   │       ├── 📄 fastagent.config.yaml
│   │       ├── 📄 router_script.txt
│   │       └── 📄 test_router_agent.py
│   └── 📄 conftest.py
└── 📁 unit
    ├── 📁 mcp_agent
    │   ├── 📁 agents
    │   │   ├── 📁 workflow
    │   │   │   ├── 📄 test_orchestrator_agent.py
    │   │   │   └── 📄 test_router_unit.py
    │   │   └── 📄 test_agent_types.py
    │   ├── 📁 cli
    │   │   └── 📁 commands
    │   │       ├── 📄 test_check_config.py
    │   │       ├── 📄 test_check_config_hf.py
    │   │       ├── 📄 test_config_env_var.py
    │   │       ├── 📄 test_url_parser.py
    │   │       └── 📄 test_url_parser_hf_auth.py
    │   ├── 📁 core
    │   │   ├── 📄 test_mcp_content.py
    │   │   └── 📄 test_prompt.py
    │   ├── 📁 llm
    │   │   ├── 📁 providers
    │   │   │   ├── 📄 test_augmented_llm_anthropic_caching.py
    │   │   │   ├── 📄 test_augmented_llm_azure.py
    │   │   │   ├── 📄 test_augmented_llm_tensorzero_unit.py
    │   │   │   ├── 📄 test_multipart_converter_anthropic.py
    │   │   │   ├── 📄 test_multipart_converter_google.py
    │   │   │   ├── 📄 test_multipart_converter_openai.py
    │   │   │   ├── 📄 test_multipart_converter_tensorzero.py
    │   │   │   ├── 📄 test_sampling_converter_anthropic.py
    │   │   │   └── 📄 test_sampling_converter_openai.py
    │   │   ├── 📄 test_cache_control_application.py
    │   │   ├── 📄 test_cache_walking_real_messages.py
    │   │   ├── 📄 test_display_input_tokens.py
    │   │   ├── 📄 test_model_database.py
    │   │   ├── 📄 test_model_factory.py
    │   │   ├── 📄 test_passthrough.py
    │   │   ├── 📄 test_playback.py
    │   │   ├── 📄 test_prepare_arguments.py
    │   │   ├── 📄 test_provider_key_manager_hf.py
    │   │   ├── 📄 test_sampling_converter.py
    │   │   ├── 📄 test_structured.py
    │   │   ├── 📄 test_usage_tracking.py
    │   │   └── 📄 test_usage_tracking_cache_billing.py
    │   ├── 📁 mcp
    │   │   ├── 📁 prompts
    │   │   │   ├── 📄 test_prompt_helpers.py
    │   │   │   ├── 📄 test_prompt_template.py
    │   │   │   └── 📄 test_template_multipart_integration.py
    │   │   ├── 📄 test_hf_auth.py
    │   │   ├── 📄 test_mime_utils.py
    │   │   ├── 📄 test_prompt_format_utils.py
    │   │   ├── 📄 test_prompt_message_multipart.py
    │   │   ├── 📄 test_prompt_multipart.py
    │   │   ├── 📄 test_prompt_multipart_conversion.py
    │   │   ├── 📄 test_prompt_render.py
    │   │   ├── 📄 test_prompt_serialization.py
    │   │   ├── 📄 test_resource_utils.py
    │   │   └── 📄 test_sampling.py
    │   └── 📁 mcp_agent
    │       ├── 📁 fixture
    │       │   ├── 📄 expected_output.txt
    │       │   ├── 📄 mcp-basic-agent-2025-02-17.jsonl
    │       │   └── 📄 README.md
    │       └── 📄 test_event_progress.py
    └── 📄 test_elicitation_format_validation.py
```

------------------------------------------------------------

## File Contents

